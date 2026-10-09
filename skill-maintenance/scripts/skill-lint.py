#!/usr/bin/env python3
"""Read-only Skill check; explicit trusted Markdown parser, restricted YAML; does not prove host behaviour."""

import argparse
import errno
import html
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from urllib.parse import unquote, urlsplit


KNOWN_FIELDS = {
    "name", "description", "license", "compatibility", "metadata", "allowed-tools",
    "argument-hint", "disable-model-invocation", "user-invocable", "model", "context",
    "agent", "hooks",
}
LIMITATIONS = [
    "Restricted YAML subset: two-space-indented mappings, single-line plain/single-quoted/JSON double-quoted scalars; sequences, flow collections, block scalars, anchors, tags and multi-line scalars are not supported.",
    "Unsupported or not reliably decidable YAML syntax exits 2; no claim of full YAML compatibility.",
    "Checks UTF-8 only for Markdown inside the package and Markdown reached via links; other resources are checked only for existence and real-path boundary.",
    "Markdown is parsed by marked; HTML links, remote reachability and fragment anchors are not checked; checked files are never executed.",
    "Does not prove host discovery, optional-field effect or Skill behaviour; the budget uses only an explicit set and the user's measured evidence.",
    "Apart from name/description, types of optional standard fields and host-extension semantics are not validated; verify separately against the target standard/host.",
    "The placeholder check recognises only explicit scaffolding markers; assets consumer templates and code examples are exempt; it does not replace semantic review.",
    "Detects changes to observed paths before/after reads and at the end; does not lock writers and provides no transactional snapshot or post-run stability guarantee.",
]
MARKDOWN_JS = r"""
import { pathToFileURL } from 'node:url';
let source = '';
for await (const chunk of process.stdin) source += chunk;
const { marked } = await import(pathToFileURL(process.argv[1]).href);
const documents = JSON.parse(source);
const result = documents.map(document => {
  const links = [];
  const text = [];
  marked.walkTokens(marked.lexer(document, {gfm: true}), token => {
    if (token.type === 'link' || token.type === 'image') links.push(token.href);
    if (token.type === 'text' && !token.tokens) text.push(token.text || '');
    if (token.type === 'html' && /^<(TODO|TBD|FIXME)>$/i.test(token.raw.trim())) text.push(token.raw);
  });
  return {links, text};
});
process.stdout.write(JSON.stringify(result));
"""


class YamlUnsupported(ValueError):
    pass


class DuplicateKey(ValueError):
    pass


def scalar(raw):
    """Reject unimplemented syntax; never pass off a guessed result as YAML parsing."""
    raw = raw.strip()
    if not raw or raw.startswith("#"):
        return None
    if raw.startswith('"'):
        try:
            value, end = json.JSONDecoder().raw_decode(raw)
        except ValueError as error:
            raise YamlUnsupported("double-quoted scalars support only JSON escapes and single-line form") from error
        if not isinstance(value, str) or (raw[end:].strip() and not raw[end:].lstrip().startswith("#")):
            raise YamlUnsupported("cannot parse trailing content after double-quoted scalar")
        if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise YamlUnsupported("double-quoted scalar contains a lone Unicode surrogate")
        return value
    if raw.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'\s*(?:#.*)?", raw)
        if not match:
            raise YamlUnsupported("cannot parse single-quoted scalar")
        return match.group(1).replace("''", "'")
    if raw[0] in "[]{}>|&*!%@`?,\"" or raw in ("---", "...", "-", ":") or re.match(r"[-:]\s", raw):
        raise YamlUnsupported("contains unsupported YAML structure or indicator")
    value = re.split(r"\s+#", raw, maxsplit=1)[0].rstrip()
    if re.search(r":(?:\s|$)", value) or "\t" in value:
        raise YamlUnsupported("plain scalar contains a mapping separator or tab")
    if value in ("null", "Null", "NULL", "~"):
        return None
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if re.fullmatch(r"[-+]?(?:[0-9].*|\.[0-9].*|\.inf|\.nan)", value, re.I):
        raise YamlUnsupported("quote number- or date-like scalars; this checker does not implement implicit typing")
    return value


def parse_yaml_subset(source):
    def printable(char):
        code = ord(char)
        return (code in (9, 10, 13, 0x85) or 0x20 <= code <= 0x7E
                or 0xA0 <= code <= 0xD7FF or 0xE000 <= code <= 0xFFFD
                or 0x10000 <= code <= 0x10FFFF)

    if not all(printable(char) for char in source):
        raise YamlUnsupported("frontmatter contains control characters forbidden by YAML")
    root = {}
    stack = [(0, root)]
    previous = None
    for number, line in enumerate(source.splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line[:len(line) - len(line.lstrip())]:
            raise YamlUnsupported("line %d: indentation contains a tab" % number)
        match = re.fullmatch(r"( *)([A-Za-z_][A-Za-z0-9_-]*):(?: +(.*))?", line)
        if not match:
            raise YamlUnsupported("line %d: not in the restricted mapping syntax" % number)
        indent, key, raw = len(match[1]), match[2], match[3] or ""
        if indent % 2:
            raise YamlUnsupported("line %d: indentation is not a multiple of two spaces" % number)
        if indent > stack[-1][0]:
            if (indent != stack[-1][0] + 2 or previous is None
                    or previous[0] != stack[-1][0] or not previous[3]):
                raise YamlUnsupported("line %d: cannot parse nested mapping indentation" % number)
            child = {}
            previous[1][previous[2]] = child
            stack.append((indent, child))
        while indent < stack[-1][0]:
            stack.pop()
        if indent != stack[-1][0]:
            raise YamlUnsupported("line %d: cannot parse mapping indentation" % number)
        parent = stack[-1][1]
        if key in parent:
            raise DuplicateKey("line %d: duplicate key: %s" % (number, key))
        parent[key] = scalar(raw)
        previous = (indent, parent, key, not raw.strip() or raw.lstrip().startswith("#"))
    return root


class Checker:
    def __init__(self, args):
        self.args = args
        self.result = {
            "schema_version": 2, "scope": "readonly-supported-subset", "package": str(Path(args.package).absolute()),
            "errors": [], "warnings": [], "input_errors": [], "host_pending": [],
            "markdown_files_checked": 0, "local_links_checked": 0,
            "external_links_skipped": 0, "limitations": LIMITATIONS,
        }
        self.allowed = []
        self.documents = {}
        self.seen_dirs = set()
        self.observed = {}
        self.aliases = {}
        self.directory_entries = {}
        self.host_config = {}
        self.root = None

    @staticmethod
    def signature(info):
        return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
                info.st_mtime_ns, info.st_ctime_ns)

    @staticmethod
    def secure_open(path):
        """Open a resolved absolute path component by component via dir_fd; reject if any component is swapped for a symlink."""
        if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
            raise OSError("no secure open support")
        fd = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
        try:
            parts = path.parts[1:]
            for index, part in enumerate(parts):
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                if index < len(parts) - 1:
                    flags |= os.O_DIRECTORY
                child = os.open(part, flags, dir_fd=fd)
                os.close(fd)
                fd = child
            return fd
        except BaseException:
            os.close(fd)
            raise

    def observe(self, real):
        try:
            fd = self.secure_open(real)
            try:
                current = self.signature(os.fstat(fd))
            finally:
                os.close(fd)
        except OSError:
            self.issue("input_errors", "unstable_or_unreadable", real, "cannot safely read path metadata; permission may be insufficient or the path changed")
            return None
        previous = self.observed.setdefault(real, current)
        if previous != current:
            self.issue("input_errors", "concurrent_change", real, "object content or identity changed during the check")
            return None
        return current

    def read_bytes(self, real):
        """Read a regular file and verify descriptor identity; do not follow path changes after opening."""
        fd = self.secure_open(real)
        try:
            before = self.signature(os.fstat(fd))
            if not stat.S_ISREG(before[2]):
                raise ValueError("not regular")
            if self.observed.setdefault(real, before) != before:
                raise OSError("changed before read")
            with os.fdopen(fd, "rb", closefd=False) as stream:
                raw = stream.read()
            if self.signature(os.fstat(fd)) != before:
                raise OSError("changed during read")
            return raw
        finally:
            os.close(fd)

    def verify_stability(self):
        for alias, original in list(self.aliases.items()):
            try:
                if alias.resolve(strict=True) != original:
                    raise OSError("changed alias")
            except (OSError, RuntimeError):
                self.issue("input_errors", "concurrent_change", alias, "path was deleted or symlink target changed during the check")
        for real in list(self.observed):
            if self.observe(real) is None:
                continue
            if real in self.directory_entries:
                try:
                    fd = self.secure_open(real)
                    try:
                        current = sorted(os.listdir(fd))
                    finally:
                        os.close(fd)
                    if current != self.directory_entries[real]:
                        raise OSError("changed entries")
                except OSError:
                    self.issue("input_errors", "concurrent_change", real, "package directory listing changed during the check")


    def issue(self, group, code, path, message):
        self.result[group].append({"code": code, "path": str(path), "message": message})

    def inside(self, path):
        return any(path == root or root in path.parents for root in self.allowed)

    def resolve(self, path):
        try:
            real = path.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            code = "symlink_cycle" if isinstance(error, RuntimeError) or getattr(error, "errno", None) == errno.ELOOP else "missing_path"
            self.issue("errors", code, path, "path does not exist, is inaccessible or forms a symlink cycle")
            return None
        if not self.inside(real):
            self.issue("errors", "outside_allowed_root", path, "real path is outside the package root and allowed reference roots")
            return None
        absolute = Path(os.path.abspath(path))
        previous = self.aliases.setdefault(absolute, real)
        if previous != real:
            self.issue("input_errors", "concurrent_change", path, "symlink target changed during the check")
            return None
        if self.observe(real) is None:
            return None
        return real

    def markdown(self, path):
        real = self.resolve(path)
        if real is None or real in self.documents:
            return
        try:
            if not stat.S_ISREG(self.observed[real][2]):
                self.issue("errors", "not_regular_file", path, "Markdown target must be a regular file")
                return
            raw = self.read_bytes(real)
            document = raw.decode("utf-8")
        except UnicodeDecodeError:
            self.issue("errors", "invalid_utf8", path, "Markdown is not valid UTF-8")
            return
        except (OSError, ValueError):
            self.issue("input_errors", "read_failed_or_changed", path, "failed to read Markdown or object changed during read")
            return
        if document.startswith("\ufeff"):
            self.issue("warnings", "utf8_bom", path, "UTF-8 BOM present; ignored when parsing, verify host compatibility separately")
            document = document[1:]
        self.documents[real] = document
        self.result["markdown_files_checked"] += 1

    def walk(self, path, ancestors=()):
        real = self.resolve(path)
        if real is None:
            return
        if stat.S_ISDIR(self.observed[real][2]):
            if real in ancestors:
                self.issue("errors", "symlink_cycle", path, "directory symlink forms a cycle")
                return
            if real in self.seen_dirs:
                return
            if path.is_symlink() and real != self.allowed[0] and self.allowed[0] not in real.parents:
                # An allowed reference root is not a traversal authorisation; external directories are only checked for existence, files are read per actual Markdown links.
                return
            self.seen_dirs.add(real)
            try:
                fd = self.secure_open(real)
                try:
                    names = sorted(os.listdir(fd))
                finally:
                    os.close(fd)
                self.directory_entries[real] = names
                children = [real / name for name in names]
            except OSError:
                self.issue("input_errors", "list_failed", path, "cannot list package directory")
                return
            for child in children:
                self.walk(child, ancestors + (real,))
        elif path.suffix.lower() == ".md" or real.suffix.lower() == ".md":
            self.markdown(real)

    def frontmatter(self, root):
        skill = root / "SKILL.md"
        if not skill.is_file():
            self.issue("errors", "missing_skill", skill, "package root lacks a regular SKILL.md file")
            return
        real = self.resolve(skill)
        document = self.documents.get(real)
        if document is None:
            return
        lines = document.splitlines()
        if not lines or lines[0] != "---":
            self.issue("errors", "missing_frontmatter", skill, "SKILL.md must start with --- frontmatter")
            return
        end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
        if end is None:
            self.issue("errors", "unclosed_frontmatter", skill, "frontmatter lacks closing ---")
            return
        self.documents[real] = "\n".join(lines[end + 1:])
        try:
            fields = parse_yaml_subset("\n".join(lines[1:end]))
        except DuplicateKey as error:
            self.issue("errors", "yaml_duplicate_key", skill, str(error))
            return
        except YamlUnsupported as error:
            self.issue("input_errors", "yaml_unsupported_or_invalid", skill, str(error))
            return
        def scalar_values(value):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for child in value.values():
                    yield from scalar_values(child)
        self.placeholders(skill, scalar_values(fields))
        supported = self.host_config.get("supported_fields")
        if supported is not None:
            for key in sorted(set(fields) - set(supported)):
                self.issue("host_pending", "host_field_unconfirmed", skill, "field not declared supported by host: %s; verify in practice" % key)
        for key in sorted(set(fields) - KNOWN_FIELDS):
            self.issue("warnings", "unknown_field", skill, "unrecognised field: %s; not treated as a specification error" % key)
        for key, maximum in (("name", 64), ("description", 1024)):
            value = fields.get(key)
            if not isinstance(value, str) or not value.strip():
                self.issue("errors", "required_field", skill, "%s must be a non-empty string" % key)
            elif len(value) > maximum:
                self.issue("errors", "field_too_long", skill, "%s exceeds %d Unicode characters" % (key, maximum))
        name = fields.get("name")
        if isinstance(name, str) and name.strip():
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                self.issue("errors", "invalid_name", skill, "name allows only lowercase ASCII letters, digits and single separating hyphens")
            if name != root.name:
                self.issue("errors", "name_directory_mismatch", skill, "name does not match the real package root directory name")

    def parse_links(self, texts):
        if not self.args.node or not self.args.marked_module:
            self.issue("input_errors", "markdown_parser_unavailable", "", "explicitly specify installed trusted --node and --marked-module; no automatic install or guessing host paths")
            return None
        node, module = Path(self.args.node).expanduser(), Path(self.args.marked_module).expanduser()
        try:
            node, module = node.resolve(strict=True), module.resolve(strict=True)
            if not node.is_file() or not module.is_file():
                raise OSError("parser_not_regular_file")
            if self.root is not None and any(self.root == path or self.root in path.parents for path in (node, module)):
                self.issue("input_errors", "untrusted_parser_location", module, "parser must not be inside the checked package; checked files are never executed")
                return None
        except (OSError, RuntimeError):
            self.issue("input_errors", "markdown_parser_unavailable", module, "parser path cannot be reliably resolved")
            return None
        env = {key: value for key, value in os.environ.items() if key not in ("NODE_OPTIONS", "NODE_PATH")}
        try:
            run = subprocess.run(
                [str(node), "--input-type=module", "-e", MARKDOWN_JS, str(module)],
                input=json.dumps(texts), text=True, capture_output=True, timeout=20, env=env,
            )
            if run.returncode:
                raise ValueError("parser_failed")
            result = json.loads(run.stdout)
            if not isinstance(result, list) or len(result) != len(texts):
                raise ValueError("parser_shape")
            for item in result:
                if (not isinstance(item, dict) or set(item) != {"links", "text"}
                        or not all(isinstance(item[key], list) and all(isinstance(value, str) for value in item[key]) for key in item)):
                    raise ValueError("parser_shape")
            return result
        except (OSError, ValueError, subprocess.TimeoutExpired):
            self.issue("input_errors", "markdown_parser_failed", module, "local Markdown parser failed or timed out")
            return None

    def links(self):
        processed = set()
        while True:
            paths = sorted(set(self.documents) - processed)
            if not paths:
                return
            links = self.parse_links([self.documents[path] for path in paths])
            if links is None:
                return
            for source, parsed in zip(paths, links):
                processed.add(source)
                self.placeholders(source, parsed["text"])
                for destination in parsed["links"]:
                    try:
                        url = urlsplit(html.unescape(destination))
                    except ValueError:
                        self.issue("errors", "invalid_link", source, "cannot parse Markdown link URL")
                        continue
                    if url.scheme == "file":
                        if url.netloc not in ("", "localhost"):
                            self.issue("input_errors", "unsupported_file_authority", source, "file links with a remote host are not supported")
                            continue
                    elif url.scheme or url.netloc:
                        self.result["external_links_skipped"] += 1
                        continue
                    if not url.path:
                        continue
                    self.result["local_links_checked"] += 1
                    try:
                        decoded = unquote(url.path, errors="strict")
                        if "\0" in decoded:
                            raise ValueError("nul")
                        target = source.parent / decoded
                    except (ValueError, UnicodeError):
                        self.issue("errors", "invalid_link_path", source, "invalid local link path")
                        continue
                    real = self.resolve(target)
                    if real is not None and (target.suffix.lower() == ".md" or real.suffix.lower() == ".md"):
                        self.markdown(real)

    def placeholders(self, path, texts):
        if self.root is not None and path != self.root / "SKILL.md":
            try:
                if path.relative_to(self.root).parts[0] == "assets":
                    return
            except ValueError:
                pass
        pattern = r"(?im)(?:\[(?:TODO|TBD|FIXME)(?::[^\]\n]*)?\]|<(?:TODO|TBD|FIXME)>|^\s*(?:TODO|TBD|FIXME)\s*:)"
        if any(re.search(pattern, value) for value in texts):
            self.issue("errors", "unfinished_placeholder", path, "body or metadata contains an explicit unfinished scaffolding marker; code examples and in-package assets templates are exempt")

    @staticmethod
    def json_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    @staticmethod
    def json_constant(value):
        raise ValueError("non-standard JSON constant: " + value)

    def json_input(self, name):
        if not name:
            return None
        try:
            alias = Path(name).expanduser().absolute()
            real = alias.resolve(strict=True)
            self.aliases[alias] = real
            value = json.loads(self.read_bytes(real).decode("utf-8"),
                               object_pairs_hook=self.json_object, parse_constant=self.json_constant)
            json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
            if not isinstance(value, dict):
                raise ValueError("expected object")
            return value
        except (OSError, RuntimeError, ValueError, UnicodeError):
            self.issue("input_errors", "invalid_json_input", name, "explicit config/set must be a stable, readable UTF-8 JSON object")
            return None

    def load_inputs(self):
        config = self.json_input(self.args.host_config)
        if config is not None:
            supported = config.get("supported_fields")
            if (any(key in config and not isinstance(config[key], str) for key in ("host", "version"))
                    or supported is not None and (not isinstance(supported, list) or not all(isinstance(x, str) for x in supported))):
                self.issue("input_errors", "invalid_host_config", self.args.host_config, "host/version must be strings; supported_fields must be an array of strings")
            else:
                self.host_config = config
                self.result["host"] = {key: config[key] for key in ("host", "version") if key in config}
        description_set = self.json_input(self.args.description_set)
        entries = description_set.get("entries") if description_set is not None else None
        if description_set is not None:
            valid = isinstance(entries, list) and bool(entries)
            names = set()
            if valid:
                for item in entries:
                    if (not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"].strip()
                            or not isinstance(item.get("description"), str) or not item["description"].strip()
                            or item["name"] in names):
                        valid = False
                        break
                    names.add(item["name"])
            if not valid:
                self.issue("input_errors", "invalid_description_set", self.args.description_set, "entries must be non-empty with unique names; name and description must both be non-empty strings")
                entries = None
            else:
                self.result["description_summary"] = {"scope": "explicit-set-descriptions-only", "count": len(entries),
                    "unicode_characters": sum(len(item["description"]) for item in entries), "complete_host_inventory": "unverified"}
        budget = self.host_config.get("description_budget")
        if budget is not None:
            valid = (isinstance(budget, dict) and budget.get("scope") == "descriptions-only"
                     and type(budget.get("limit_characters")) is int and budget["limit_characters"] > 0
                     and all(isinstance(budget.get(key), str) and budget[key].strip() for key in ("evidence", "measured_at")))
            if not valid or entries is None:
                self.issue("input_errors", "unusable_description_budget", self.args.host_config, "budget requires descriptions-only scope, a positive integer character limit, user measurement evidence/date and a valid explicit description set")
            else:
                summary = self.result["description_summary"]
                summary["user_supplied_budget"] = budget
                summary["evidence_independently_verified"] = False
                summary["exceeds_budget"] = summary["unicode_characters"] > budget["limit_characters"]
                if summary["exceeds_budget"]:
                    self.issue("warnings", "description_budget_exceeded", self.args.description_set, "explicit set exceeds the user-supplied description budget; consider trimming or measuring the host listing; not a format error")

    def run(self):
        self.load_inputs()
        try:
            root = Path(self.args.package).expanduser().resolve(strict=True)
            if not root.is_dir():
                raise ValueError("package")
            roots = [Path(value).expanduser().resolve(strict=True) for value in self.args.allow_reference_root]
            if not all(path.is_dir() for path in roots):
                raise ValueError("reference root")
        except (OSError, RuntimeError, ValueError):
            self.issue("input_errors", "invalid_root", self.args.package, "package root and allowed reference roots must be existing, resolvable directories")
        else:
            self.allowed = [root] + roots
            self.root = root
            self.resolve(Path(self.args.package).expanduser().absolute())
            for value in self.args.allow_reference_root:
                self.resolve(Path(value).expanduser().absolute())
            self.result["package"] = str(root)
            self.result["allowed_reference_roots"] = [str(path) for path in roots]
            self.walk(root)
            self.frontmatter(root)
            self.links()
        self.verify_stability()
        return self.finish()

    def finish(self):
        code = 2 if self.result["input_errors"] else 1 if self.result["errors"] else 0
        self.result["exit_code"] = code
        self.result["status"] = {0: "passed", 1: "noncompliant", 2: "incomplete"}[code]
        print(json.dumps(self.result, ensure_ascii=False, indent=2))
        return code


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({"schema_version": 2, "status": "incomplete", "exit_code": 2,
                          "input_errors": [{"code": "invalid_arguments", "message": message}]}, ensure_ascii=False))
        raise SystemExit(2)


def main():
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("package", help="single Skill package directory; a discovery symlink path is allowed")
    parser.add_argument("--allow-reference-root", action="append", default=[], help="extra directory that real references may reach; repeatable; only reached references are read")
    parser.add_argument("--node", help="explicit installed trusted Node executable; not looked up automatically")
    parser.add_argument("--marked-module", help="explicit installed trusted marked module entry; not installed automatically")
    parser.add_argument("--host-config", help="user-supplied JSON with host capabilities and measured description budget")
    parser.add_argument("--description-set", help="explicit description-set JSON; only entries are summed, discovery directories are not scanned")
    return Checker(parser.parse_args()).run()


if __name__ == "__main__":
    sys.exit(main())
