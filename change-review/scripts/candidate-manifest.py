#!/usr/bin/env python3
"""Read only explicit regular files twice; print a scoped candidate identity as JSON."""
import argparse
import errno
import hashlib
import json
import os
from pathlib import PurePosixPath
import stat
import sys

KINDS = {'added', 'modified', 'deleted', 'context', 'generated', 'excluded'}
SENSITIVE = {'.git', '.ssh', '.aws', '.gnupg', '.env', '.npmrc', '.netrc',
             'credentials', 'credentials.json', 'credentials.md', 'secrets',
             'id_rsa', 'id_ed25519'}

class Invalid(Exception):
    pass

class Unstable(Exception):
    pass

def encode(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()

def relpath(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise Invalid('path must be a relative POSIX path')
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in ('', '.', '..') for x in value.split('/')):
        raise Invalid('absolute, empty, dot and parent path components are forbidden')
    return value

def secret(path):
    for part in path.lower().split('/'):
        if (part in SENSITIVE or part.startswith('.env.') or
            part.endswith(('.pem', '.key', '.p12', '.pfx'))):
            return True
    return False

def secure_open(path, directory=False):
    """Walk from / with descriptor-relative no-follow opens for every component."""
    if not os.path.isabs(path):
        path = os.getcwd() + '/' + path
    if path != '/' and (not path.startswith('/') or any(x in ('', '.', '..') for x in path[1:].split('/'))):
        raise Invalid('path is not canonical')
    if '\\' in path or '\x00' in path or any(0xD800 <= ord(c) <= 0xDFFF for c in path):
        raise Invalid('invalid path encoding')
    parts = [] if path == '/' else path[1:].split('/')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for i, part in enumerate(parts):
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            if directory or i < len(parts) - 1:
                flags |= os.O_DIRECTORY
            child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        result, fd = fd, None
        return result
    finally:
        if fd is not None:
            os.close(fd)

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid('duplicate JSON key')
        result[key] = value
    return result

def reject_number(value):
    raise Invalid('non-integer JSON number is not supported')

def bounded_integer(value):
    if len(value) > 20:
        raise Invalid('JSON integer exceeds limit')
    return int(value)

def read_json(path):
    if secret(path):
        raise Invalid('secret-like control path is forbidden')
    try:
        fd = secure_open(path)
    except FileNotFoundError:
        raise Invalid('control input file does not exist')
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            raise Invalid('control input path has a symlink component; use its real path')
        raise
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > 4 * 1024 * 1024:
            raise Invalid('control input must be a bounded regular file')
        data = stream.read(4 * 1024 * 1024 + 1)
        stream.seek(0)
        second = stream.read(4 * 1024 * 1024 + 1)
        after = os.fstat(stream.fileno())
    again = secure_open(path)
    try:
        current = os.fstat(again)
    finally:
        os.close(again)
    if len(data) > 4 * 1024 * 1024 or len(second) > 4 * 1024 * 1024:
        raise Invalid('control input exceeds limit')
    if data != second or identity(before) != identity(after) or identity(after) != identity(current):
        raise Unstable('control input changed while reading')
    value = json.loads(data.decode('utf-8'), object_pairs_hook=unique_object,
                       parse_constant=reject_number, parse_float=reject_number, parse_int=bounded_integer)
    pending = [(value, 0)]
    while pending:
        item, depth = pending.pop()
        if depth > 32:
            raise Invalid('JSON nesting exceeds limit')
        if isinstance(item, str) and any(0xD800 <= ord(c) <= 0xDFFF for c in item):
            raise Invalid('unpaired Unicode surrogate')
        if isinstance(item, dict):
            pending.extend((x, depth + 1) for pair in item.items() for x in pair)
        elif isinstance(item, list):
            pending.extend((x, depth + 1) for x in item)
    return value

def validate(data, max_files):
    if not isinstance(data, dict) or set(data) != {'entries'}:
        raise Invalid('scope must contain only entries')
    entries = data['entries']
    if not isinstance(entries, list) or len(entries) > max_files:
        raise Invalid('entries must be a bounded list')
    seen, clean = set(), []
    for item in entries:
        if not isinstance(item, dict) or set(item) - {'path', 'kind', 'reason', 'sources', 'previous_sha256', 'secret'}:
            raise Invalid('invalid entry fields')
        path, kind = relpath(item.get('path')), item.get('kind')
        if path in seen or not isinstance(kind, str) or kind not in KINDS:
            raise Invalid('duplicate path or unknown kind')
        seen.add(path)
        if 'reason' in item and (not isinstance(item['reason'], str) or not item['reason'].strip()):
            raise Invalid('reason must be nonempty text')
        if 'secret' in item and not isinstance(item['secret'], bool):
            raise Invalid('secret must be boolean')
        if kind == 'excluded' and (not isinstance(item.get('reason'), str) or not item['reason'].strip()):
            raise Invalid('exclusion requires reason')
        if (secret(path) or item.get('secret')) and kind != 'excluded':
            raise Invalid('secret-like or explicitly secret paths must be excluded')
        sources = item.get('sources', [])
        if not isinstance(sources, list) or any(not isinstance(x, str) for x in sources):
            raise Invalid('sources must be relative path strings')
        sources = [relpath(x) for x in sources]
        if kind == 'generated' and not sources:
            raise Invalid('generated output requires explicit sources')
        old = item.get('previous_sha256')
        if old is not None and (not isinstance(old, str) or len(old) != 64 or any(c not in '0123456789abcdef' for c in old)):
            raise Invalid('previous_sha256 must be lowercase SHA256')
        clean.append(dict(item, sources=sources))
    for item in clean:
        if any(x not in seen for x in item['sources']):
            raise Invalid('each generation source needs its own scope entry, including exclusions')
    return sorted(clean, key=lambda x: x['path'])

def identity(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def probe(root_fd, item, byte_limit):
    if item['kind'] == 'excluded':
        return dict(item, sha256=None, deleted=False, observed='not-read'), None
    parts = item['path'].split('/')
    fd = os.dup(root_fd)
    try:
        try:
            for part in parts[:-1]:
                try:
                    child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                except OSError as error:
                    if error.errno in (errno.ELOOP, errno.ENOTDIR):
                        raise Invalid('a candidate parent component is a symlink or not a directory')
                    raise
                os.close(fd)
                fd = child
            info = os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            if item['kind'] != 'deleted':
                raise Invalid('a required candidate file is missing')
            return dict(item, sha256=None, deleted=True, observed='absent'), None
        if item['kind'] == 'deleted':
            raise Invalid('a declared deletion is still present')
        if stat.S_ISLNK(info.st_mode):
            raise Invalid('candidate is a symlink; list the real file instead')
        if not stat.S_ISREG(info.st_mode):
            raise Invalid('candidate must be a regular file, not a directory or special file')
        if info.st_size > byte_limit:
            raise Invalid('candidate exceeds per-file byte limit')
        file_fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(file_fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or identity(before) != identity(info):
                raise Unstable('file changed between inspection and open')
            h, size = hashlib.sha256(), 0
            while True:
                chunk = stream.read(min(1024 * 1024, byte_limit - size + 1))
                if not chunk:
                    break
                size += len(chunk)
                if size > byte_limit:
                    raise Invalid('candidate exceeds per-file byte limit')
                h.update(chunk)
            after = os.fstat(stream.fileno())
        current = os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)
        if identity(before) != identity(after) or identity(after) != identity(current):
            raise Unstable('file changed while reading')
        return dict(item, sha256=h.hexdigest(), bytes=size, deleted=False,
                    observed='regular-file'), identity(after)
    finally:
        os.close(fd)

def snapshot(root, entries, byte_limit):
    if secret(root) or not os.path.isabs(root):
        raise Invalid('root must be an explicit absolute canonical path without symlinks')
    try:
        root_fd = secure_open(root, directory=True)
    except FileNotFoundError:
        raise Invalid('root does not exist')
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            raise Invalid('root must be a real path without symlink components; resolve it first (macOS /tmp and /var are symlinks to /private)')
        raise
    try:
        first = [probe(root_fd, x, byte_limit) for x in entries]
        second = [probe(root_fd, x, byte_limit) for x in entries]
        again = secure_open(root, directory=True)
        try:
            root_now = os.fstat(again)
        finally:
            os.close(again)
        root_open = os.fstat(root_fd)
        if (root_now.st_dev, root_now.st_ino) != (root_open.st_dev, root_open.st_ino):
            raise Unstable('root replaced during capture')
        if first != second:
            raise Unstable('candidate changed between content reads')
    finally:
        os.close(root_fd)
    payload = {'schema': 1, 'root': root, 'scope_sha256': digest(entries),
               'entries': [x[0] for x in second]}
    payload['candidate_sha256'] = digest(payload)
    payload['coverage'] = 'explicit-scope-only'
    payload['stability'] = 'two-content-reads-agree; not an atomic snapshot or a lock'
    return payload

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--scope', required=True, help='explicit known non-secret scope JSON')
    parser.add_argument('--compare', help='previous manifest, never candidate content')
    parser.add_argument('--max-files', type=int, default=1000)
    parser.add_argument('--max-file-bytes', type=int, default=16 * 1024 * 1024)
    args = parser.parse_args()
    try:
        if any(not hasattr(os, x) for x in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK')) or os.open not in os.supports_dir_fd or os.stat not in os.supports_dir_fd:
            raise Invalid('required no-follow descriptor operations unavailable')
        if args.max_files < 1 or args.max_file_bytes < 1:
            raise Invalid('limits must be positive')
        entries = validate(read_json(args.scope), args.max_files)
        result = snapshot(args.root, entries, args.max_file_bytes)
        if args.compare:
            old = read_json(args.compare)
            if not isinstance(old, dict) or type(old.get('schema')) is not int or old.get('schema') != 1:
                raise Invalid('previous manifest schema is invalid')
            required = {'schema', 'root', 'scope_sha256', 'entries'}
            if set(old) - (required | {'candidate_sha256', 'coverage', 'stability', 'comparison', 'status'}):
                raise Invalid('unknown previous manifest fields')
            if not isinstance(old.get('root'), str) or not isinstance(old.get('entries'), list):
                raise Invalid('invalid previous manifest field types')
            base = []
            for entry in old['entries']:
                if not isinstance(entry, dict) or set(entry) - {'path', 'kind', 'reason', 'sources', 'previous_sha256', 'secret', 'sha256', 'bytes', 'deleted', 'observed'}:
                    raise Invalid('invalid previous entry')
                if type(entry.get('deleted')) is not bool or entry.get('observed') not in ('not-read', 'absent', 'regular-file'):
                    raise Invalid('invalid previous observation')
                if 'bytes' in entry and (type(entry['bytes']) is not int or entry['bytes'] < 0):
                    raise Invalid('invalid previous bytes')
                h = entry.get('sha256')
                if h is not None and (not isinstance(h, str) or len(h) != 64 or any(c not in '0123456789abcdef' for c in h)):
                    raise Invalid('invalid previous content hash')
                base.append({k: v for k, v in entry.items() if k not in {'sha256', 'bytes', 'deleted', 'observed'}})
            if digest(validate({'entries': base}, args.max_files)) != old.get('scope_sha256'):
                raise Invalid('previous scope identity invalid')
            for key in ('coverage', 'stability', 'comparison', 'status'):
                if key in old and not isinstance(old[key], str):
                    raise Invalid('invalid previous metadata')
            if not required.issubset(old) or digest({k: old[k] for k in required}) != old.get('candidate_sha256'):
                raise Invalid('previous manifest identity is invalid')
            same = old['candidate_sha256'] == result['candidate_sha256']
            result['comparison'] = 'unchanged' if same else 'changed'
            result['status'] = 'captured' if same else 'changed'
            print(encode(result).decode())
            return 0 if same else 1
        result['status'] = 'captured'
        print(encode(result).decode())
        return 0
    except Unstable as error:
        # Messages are script constants; they never contain paths or file bytes.
        print(encode({'error': str(error), 'status': 'unstable'}).decode(), file=sys.stderr)
        return 2
    except Invalid as error:
        print(encode({'error': str(error), 'status': 'error'}).decode(), file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, KeyError, RecursionError, AttributeError, NotImplementedError, OverflowError):
        # Do not echo file bytes, OS paths or untrusted exception text.
        print('{"error":"invalid input or unreadable candidate; no stable manifest","status":"error"}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
