#!/usr/bin/env python3
"""Read-only archive verifier; input contract in references/retention-and-references.md."""
import codecs
import errno
import hashlib
import json
import os
import re
import stat
import sys
import unicodedata
from contextlib import contextmanager

CHUNK = 1024 * 1024
MANIFEST_LIMIT = 1024 * 1024


class Invalid(Exception):
    pass


class CheckFailed(Exception):
    pass


ROOT_HINT = "allowed root or manifest directory has a symlink component or is not a directory; pass the real absolute path (macOS /tmp and /var are symlinks to /private)"


def classify_os_error(error):
    """Map a platform OSError to a fixed code and constant message; never output raw errno text or paths."""
    if isinstance(error, FileNotFoundError):
        return "missing_file", "file or its parent directory does not exist"
    if getattr(error, "errno", None) in (errno.ELOOP, errno.ENOTDIR):
        return "symlink_or_boundary", "a path component is a symlink or not a directory; symlinks are not followed and the allowed root is never left"
    if isinstance(error, PermissionError):
        return "permission_denied", "no permission to read this file or directory"
    return "file_unreadable", "file cannot be read safely"


def require(condition, message):
    if not condition:
        raise Invalid(message)


def obj(value, required, optional=()):
    require(type(value) is dict, "expected a JSON object; null is not accepted")
    require(set(required) <= value.keys() and value.keys() <= set(required) | set(optional),
            "object has missing or unknown fields")


def string(value):
    require(type(value) is str and 0 < len(value) <= 4096 and "\x00" not in value,
            "expected a non-empty string of at most 4096 characters without NUL")
    return value


def relative(value):
    string(value)
    require(not value.startswith("/") and "\\" not in value
            and all(x not in ("", ".", "..") for x in value.split("/")),
            "file locator must be a canonical relative path; dot segments, path traversal and backslashes are forbidden")
    return value


def stamp(st):
    return (st.st_dev, st.st_ino, st.st_mode, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON contains duplicate fields")
        result[key] = value
    return result


def reject_constant(value):
    raise Invalid("JSON forbids NaN or Infinity: " + value)


def validate_utf8_strings(value):
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, str):
            try:
                item.encode("utf-8")
            except UnicodeError:
                raise Invalid("JSON string contains a lone surrogate not encodable as UTF-8") from None
        elif isinstance(item, dict):
            pending.extend(item.keys())
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)


def positions(haystack, needle):
    position = haystack.find(needle)
    while position >= 0:
        yield position
        position = haystack.find(needle, position + 1)


@contextmanager
def open_absolute_directory(path):
    string(path)
    require(path.startswith("/") and path != "/" and "\\" not in path
            and all(x not in ("", ".", "..") for x in path[1:].split("/")),
            "allowed root must be a canonical absolute directory, not the file-system root and without dot segments")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path[1:].split("/"):
            try:
                new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            except FileNotFoundError:
                raise Invalid("allowed root or manifest directory does not exist") from None
            except OSError as error:
                if error.errno in (errno.ELOOP, errno.ENOTDIR):
                    raise Invalid(ROOT_HINT) from None
                raise
            os.close(fd)
            fd = new
        yield fd
    finally:
        os.close(fd)


class Reader:
    def __init__(self, roots):
        self.roots = roots
        self.observed = {}
        self.root_stamps = {}
        for name, path in roots.items():
            with open_absolute_directory(path) as fd:
                st = os.fstat(fd)
                self.root_stamps[name] = (st.st_dev, st.st_ino)

    def locator(self, value):
        obj(value, ("root", "path"))
        require(type(value["root"]) is str and value["root"] in self.roots, "file references an unknown allowed root")
        relative(value["path"])
        return os.path.join(self.roots[value["root"]], value["path"])

    @contextmanager
    def parent(self, loc, allow_missing=False):
        self.locator(loc)
        with open_absolute_directory(self.roots[loc["root"]]) as root_fd:
            st = os.fstat(root_fd)
            if (st.st_dev, st.st_ino) != self.root_stamps[loc["root"]]:
                raise CheckFailed("allowed root was replaced during reading")
            fd = os.dup(root_fd)
            try:
                parts = loc["path"].split("/")
                for part in parts[:-1]:
                    try:
                        new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                    except FileNotFoundError:
                        if allow_missing:
                            yield None, parts[-1]
                            return
                        raise
                    os.close(fd)
                    fd = new
                yield fd, parts[-1]
            finally:
                os.close(fd)

    @contextmanager
    def file(self, loc):
        with self.parent(loc) as (parent_fd, name):
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
            try:
                before = os.fstat(fd)
                if not stat.S_ISREG(before.st_mode):
                    raise CheckFailed("only regular files are allowed")
                yield fd, stamp(before)
                if stamp(os.fstat(fd)) != stamp(before):
                    raise CheckFailed("file changed during reading")
            finally:
                os.close(fd)

    def absent(self, loc):
        with self.parent(loc, allow_missing=True) as (fd, name):
            if fd is None:
                return True
            try:
                os.stat(name, dir_fd=fd, follow_symlinks=False)
            except FileNotFoundError:
                return True
            return False

    def digest(self, loc, needles=(), text=False, protected=()):
        digest = hashlib.sha256()
        counts = {n: 0 for n in needles}
        uncovered = {n: 0 for n in needles}
        encoded = {n: n.encode("utf-8") for n in needles}
        shields = tuple(n.encode("utf-8") for n in protected)
        longest = max((len(n) for n in (*encoded.values(), *shields)), default=1)
        tail, total, committed = b"", 0, 0
        decoder = codecs.getincrementaldecoder("utf-8")("strict") if text else None
        with self.file(loc) as (fd, before):
            while True:
                block = os.read(fd, CHUNK)
                digest.update(block)
                if decoder:
                    decoder.decode(block)
                window = tail + block
                base = total - len(tail)
                total += len(block)
                # Delay commit until the longest path on the right is complete; keep left context of the same length.
                # Coverage is judged per occurrence position; repeated/nested literals are not handled by subtracting counts.
                end = total if not block else max(0, total - longest + 1)
                for label, needle in encoded.items():
                    for position in positions(window, needle):
                        if not committed <= base + position < end:
                            continue
                        counts[label] += 1
                        covered = any(
                            position >= offset and window.startswith(shield, position - offset)
                            for shield in shields for offset in positions(shield, needle))
                        if not covered:
                            uncovered[label] += 1
                committed = end
                if not block:
                    break
                keep_from = max(0, committed - longest + 1)
                tail = window[keep_from - base:]
            if decoder:
                decoder.decode(b"", final=True)
            if total != before[3]:
                raise CheckFailed("bytes read do not match file size")
        path = self.locator(loc)
        previous = self.observed.get(path)
        if previous and previous[1] != before:
            raise CheckFailed("file changed between two reads")
        self.observed[path] = (loc, before)
        self.check_one(loc, before)
        return {"size": total, "sha256": digest.hexdigest(), "counts": counts,
                "uncovered": uncovered, "inode": before[:2]}

    def check_one(self, loc, expected):
        with self.file(loc) as (_, current):
            if current != expected:
                raise CheckFailed("file content or path identity changed after reading")

    def final_check(self):
        for loc, expected in self.observed.values():
            self.check_one(loc, expected)
        for name, path in self.roots.items():
            with open_absolute_directory(path) as fd:
                st = os.fstat(fd)
                if (st.st_dev, st.st_ino) != self.root_stamps[name]:
                    raise CheckFailed("allowed root was replaced before the check finished")

    def same_bytes(self, left, right):
        with self.file(left) as (a, sa), self.file(right) as (b, sb):
            if sa[:2] == sb[:2]:
                raise CheckFailed("restored copy and archive are the same file or hard links")
            while True:
                x, y = os.read(a, CHUNK), os.read(b, CHUNK)
                if x != y:
                    raise CheckFailed("restored copy and archive differ in actual bytes")
                if not x:
                    break


def load_manifest(path):
    string(path)
    require(".." not in path.split("/") and "\\" not in path, "manifest path must not traverse")
    absolute = os.path.abspath(path)
    directory, name = os.path.split(absolute)
    with open_absolute_directory(directory) as parent_fd:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
        try:
            before = os.fstat(fd)
            require(stat.S_ISREG(before.st_mode) and before.st_size <= MANIFEST_LIMIT,
                    "manifest must be a regular file of at most 1 MiB")
            data = bytearray()
            while len(data) <= MANIFEST_LIMIT:
                part = os.read(fd, min(CHUNK, MANIFEST_LIMIT + 1 - len(data)))
                if not part:
                    break
                data.extend(part)
            require(len(data) <= MANIFEST_LIMIT and stamp(os.fstat(fd)) == stamp(before),
                    "manifest too large or changed while reading")
            require(stamp(os.stat(name, dir_fd=parent_fd, follow_symlinks=False)) == stamp(before),
                    "manifest path changed while reading")
        finally:
            os.close(fd)
    result = json.loads(data, object_pairs_hook=no_duplicates, parse_constant=reject_constant)
    validate_utf8_strings(result)
    return result


def validate(data):
    obj(data, ("schema_version", "phase", "roots", "entries", "scan_files", "references"))
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "schema_version must be the integer 1")
    require(type(data["phase"]) is str and data["phase"] in ("precopy", "verify", "restore"), "unknown phase")
    require(type(data["roots"]) is dict and 0 < len(data["roots"]) <= 32, "roots must contain 1 to 32 allowed roots")
    for name, value in data["roots"].items():
        require(re.fullmatch(r"[a-z][a-z0-9_-]{0,31}", name) is not None, "invalid root name format")
        string(value)
    reader = Reader(data["roots"])
    for field in ("entries", "scan_files", "references"):
        require(type(data[field]) is list and len(data[field]) <= 4096, field + " must be an array of at most 4096 items")
    require(data["entries"], "entries must not be empty")
    ids, paths = {}, {}
    for entry in data["entries"]:
        obj(entry, ("id", "source", "archive", "size", "sha256", "state", "retain_source"), ("restore",))
        identity = string(entry["id"])
        require(identity not in ids, "duplicate entry ID")
        ids[identity] = entry
        require(type(entry["size"]) is int and entry["size"] >= 0, "size must be a non-negative integer")
        require(type(entry["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]), "sha256 must be 64 lowercase hex characters")
        require(type(entry["state"]) is str and entry["state"] in ("closed", "active", "unknown"), "unknown activity state")
        require(type(entry["retain_source"]) is bool, "retain_source must be a boolean")
        require(data["phase"] != "restore" or "restore" in entry, "restore mode requires an actual restored file for every entry")
        for role in ("source", "archive", "restore"):
            if role not in entry:
                continue
            path = reader.locator(entry[role])
            key = unicodedata.normalize("NFC", path).casefold()
            require(key not in paths, "manifest paths collide or overlap (including case/Unicode-equivalent names)")
            paths[key] = (identity, role)
    scans = {}
    for loc in data["scan_files"]:
        path = reader.locator(loc)
        require(path not in scans, "duplicate scan file")
        scans[path] = loc
    ref_keys = set()
    for ref in data["references"]:
        obj(ref, ("file", "entry", "kind", "literal", "historical", "reason"))
        path = reader.locator(ref["file"])
        require(path in scans, "explicit reference file must be listed in scan_files")
        require(type(ref["entry"]) is str and ref["entry"] in ids, "reference to an unknown entry")
        require(type(ref["kind"]) is str and ref["kind"] in ("source", "archive", "restore"), "invalid reference kind")
        require(ref["kind"] in ids[ref["entry"]], "reference target file is not declared")
        literal = string(ref["literal"])
        require(not any(x in literal for x in ("\\", "\n", "\r", "#", "?", "%", ":")),
                "references support only unencoded file paths; URLs, anchors, queries and backslashes are not supported")
        expected = reader.locator(ids[ref["entry"]][ref["kind"]])
        resolved = os.path.normpath(os.path.join(os.path.dirname(path), literal))
        require(resolved == expected, "reference literal path does not match the declared target or leaves the allowed scope")
        # Relative references may contain .., but must resolve exactly to a verified target inside an allowed root; never via a symlinked directory.
        require(literal == expected or literal == os.path.relpath(expected, os.path.dirname(path)),
                "reference path must be the target absolute path or canonical relative path")
        require(type(ref["historical"]) is bool and type(ref["reason"]) is str, "historical must be a boolean and reason must be a string")
        require(not ref["historical"] or ref["reason"].strip(), "a deliberately kept historical reference requires a reason")
        key = (path, literal)
        require(key not in ref_keys, "same text reference declared more than once")
        ref_keys.add(key)
    return reader, ids, scans


def verify(data):
    reader, ids, scans = validate(data)
    phase, issues, files, recovered = data["phase"], [], [], []
    verified = set()

    def issue(code, context, error, severity="error"):
        issues.append({"code": code, "context": context, "message": str(error), "severity": severity})

    def os_issue(error, context):
        code, message = classify_os_error(error)
        return code, context, message

    for identity, entry in ids.items():
        if entry["state"] != "closed":
            issue("active_or_unknown", identity, "active or unknown-state files must not be archived or signed off as restored")
            continue
        roles = ("source",) if phase == "precopy" else (("source", "archive") if phase == "verify" else ("archive", "restore"))
        observations = {}
        for role in roles:
            try:
                observed = reader.digest(entry[role])
                observations[role] = observed
                files.append({"entry": identity, "role": role, "size": observed["size"], "sha256": observed["sha256"]})
                if observed["size"] != entry["size"] or observed["sha256"] != entry["sha256"]:
                    raise CheckFailed("actual size or SHA-256 does not match the pinned manifest")
                verified.add((identity, role))
            except OSError as error:
                issue(*os_issue(error, identity + ":" + role))
            except UnicodeError:
                issue("file_verification", identity + ":" + role, "file is not valid UTF-8")
            except CheckFailed as error:
                issue("file_verification", identity + ":" + role, error)
        try:
            if phase == "precopy" and not reader.absent(entry["archive"]):
                raise CheckFailed("archive target already exists; must not be overwritten even with identical bytes")
            if phase == "verify" and len(observations) == 2:
                if observations["source"]["inode"] == observations["archive"]["inode"]:
                    raise CheckFailed("source and archive are the same file or hard links, not an independent copy")
            if phase == "restore" and all((identity, role) in verified for role in roles):
                reader.same_bytes(entry["archive"], entry["restore"])
                recovered.append(identity)
        except OSError as error:
            issue(*os_issue(error, identity))
        except CheckFailed as error:
            issue("target_or_recovery", identity, error)

    for path, loc in scans.items():
        explicit = [r for r in data["references"] if reader.locator(r["file"]) == path]
        needles = {r["literal"] for r in explicit}
        old = {}
        for identity, entry in ids.items():
            source = reader.locator(entry["source"])
            for literal in (source, os.path.relpath(source, os.path.dirname(path))):
                needles.add(literal)
                old.setdefault(literal, []).append(identity)
        try:
            protected = {r["literal"] for r in explicit
                         if r["kind"] in ("archive", "restore") and (r["entry"], r["kind"]) in verified}
            result = reader.digest(loc, needles, text=True, protected=protected)
            files.append({"scan": path, "size": result["size"], "sha256": result["sha256"],
                          "matches": result["counts"], "uncovered_matches": result["uncovered"]})
            for ref in explicit:
                if not result["counts"][ref["literal"]]:
                    issue("reference_absent", path, "explicit reference literal not found: " + ref["literal"])
                identity, kind = ref["entry"], ref["kind"]
                if (identity, kind) not in verified:
                    if kind == "source" and phase == "restore" and ids[identity]["retain_source"]:
                        try:
                            observed = reader.digest(ids[identity]["source"])
                            if observed["size"] != ids[identity]["size"] or observed["sha256"] != ids[identity]["sha256"]:
                                raise CheckFailed("retained source does not match the manifest")
                            verified.add((identity, kind))
                        except OSError as error:
                            issue(*os_issue(error, path))
                        except CheckFailed as error:
                            issue("reference_target", path, error)
                    else:
                        issue("reference_target", path, "reference target did not pass this phase's actual file verification")
            for literal, identities in old.items():
                if not result["uncovered"][literal]:
                    continue
                for identity in identities:
                    preserved = ids[identity]["retain_source"] and any(
                        r["entry"] == identity and r["literal"] == literal and r["kind"] == "source"
                        and r["historical"] for r in explicit)
                    if not preserved:
                        issue("old_source_reference", path, "old source path still present: " + literal,
                              "warning" if phase == "precopy" else "error")
        except OSError as error:
            issue(*os_issue(error, path))
        except UnicodeError:
            issue("text_scan", path, "scan file is not valid UTF-8")
        except CheckFailed as error:
            issue("text_scan", path, error)
    try:
        reader.final_check()
    except OSError as error:
        issue("changed_during_run", "final_check", classify_os_error(error)[1])
    except CheckFailed as error:
        issue("changed_during_run", "final_check", error)
    success = not any(x["severity"] == "error" for x in issues)
    bytes_by_role = {}
    for item in files:
        if "role" in item:
            bytes_by_role[item["role"]] = bytes_by_role.get(item["role"], 0) + item["size"]
    return {"schema_version": 1, "ok": success, "phase": phase, "status": "passed" if success else "noncompliant",
            "summary": {"entries": len(ids), "scan_files": len(scans), "explicit_references": len(data["references"]),
                        "restored_byte_comparisons": len(recovered), "errors": sum(x["severity"] == "error" for x in issues),
                        "bytes_by_role": bytes_by_role},
            "coverage": "declared manifest only; full-text UTF-8 literal scan and explicit path verification; Markdown/dynamic links not parsed; not a move-out authorisation",
            "files": files, "recovered": recovered, "issues": issues}, 0 if success else 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        require(len(argv) == 1 and argv[0] not in ("-h", "--help"), "usage: python3 archive-verify.py manifest.json")
        require(all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK")), "host lacks safe read-only open capabilities")
        data = load_manifest(argv[0])
        result, code = verify(data)
    except (Invalid, CheckFailed) as error:
        result, code = {"schema_version": 1, "ok": False, "status": "invalid_input",
                        "issues": [{"code": "invalid_input", "message": str(error)}]}, 2
    except json.JSONDecodeError:
        result, code = {"schema_version": 1, "ok": False, "status": "invalid_input",
                        "issues": [{"code": "invalid_input", "message": "manifest is not valid JSON"}]}, 2
    except OSError as error:
        result, code = {"schema_version": 1, "ok": False, "status": "invalid_input",
                        "issues": [{"code": classify_os_error(error)[0], "message": classify_os_error(error)[1]}]}, 2
    except (ValueError, UnicodeError, RecursionError):
        result, code = {"schema_version": 1, "ok": False, "status": "invalid_input",
                        "issues": [{"code": "invalid_input", "message": "manifest encoding, structure or numbers cannot be parsed"}]}, 2
    except Exception as error:
        result, code = {"schema_version": 1, "ok": False, "status": "internal_error",
                        "issues": [{"code": "internal_error", "message": type(error).__name__}]}, 2
    result["exit_code"] = code
    print(json.dumps(result, ensure_ascii=True, allow_nan=False, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
