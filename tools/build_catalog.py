#!/usr/bin/env python3
"""Generate README.md — the index of what is published in this project's registry.

Contract
========

* **`README.md` is generated. Never hand-edit it.** `--check` fails when the file
  is not byte-for-byte the output of this script over `catalog/`, which is what
  makes a hand edit a red pipeline rather than a silent divergence.
* **This script is a pure function of its inputs** — `catalog/**` plus the two
  hand-edited fragments in `tools/readme/`. It never contacts the registry, never
  reads the clock, and never depends on the machine it runs on. Digests are
  resolved by the **publishing project** and recorded in `entry.toml`; that is
  the only way `--check` can run on a branch and mean anything, because a live
  registry read changes without a commit.
* **Verification is a separate concern.** Resolving tags against the registry,
  and catching a tag that retention collected, belongs to a job that is allowed
  to change its answer — not to the one that decides whether a commit is correct.

Modes
=====

    build_catalog.py --check     # default: validate, then diff against README.md
    build_catalog.py --write     # validate, then write README.md
    build_catalog.py --validate  # validate only, no README comparison

Exit codes: 0 ok · 1 README mismatch · 2 validation error.
"""

from __future__ import annotations

import difflib
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
HEADER = ROOT / "tools" / "readme" / "header.md"
FOOTER = ROOT / "tools" / "readme" / "footer.md"
README = ROOT / "README.md"

KINDS = {"container", "pypi", "npm", "file"}
REQUIRED = ("project", "title", "license", "maintainer")
ENTRY_KEYS = set(REQUIRED) | {"summary_file", "published_from", "artifact"}
ARTIFACT_KEYS = {"kind", "repository", "tags", "digests", "sizes", "summary"}
MAX_SUMMARY_LINES = 30

# Tag prefixes this index may never advertise. Both are classes a container
# registry cleanup policy will collect: `sha-` is what a publish job writes for
# every build, and `r-` is a recipe tag written per build and only kept inside
# `keep_n`. Only `latest` is unconditionally retained, so a promise made here has
# to be `latest`, a release tag, or a digest.
FORBIDDEN_TAG_PREFIXES = ("sha-", "r-")

# A digest the index can actually be pinned to.
DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}")

# Where the artifacts are published. Interpolated into the header's prose and into
# every link the page renders, so a host change is one line here rather than a sweep
# through the template and the table.
REGISTRY_HOST = "ghcr.io/ebruno/swtr-udemy-artifacts"

# This index carries **no links**. A publishing project may have no public
# repository, and a URL that only resolves behind a login is worse than no URL at
# all -- so the page names the project, its licence, its maintainer and the
# release. Anything richer belongs in that project's own documentation.


class Invalid(Exception):
    """One or more catalog entries are not publishable."""


def fail(errors: list[str]) -> None:
    if not errors:
        return
    for err in errors:
        print(f"error: {err}", file=sys.stderr)
    raise Invalid(f"{len(errors)} problem(s) in catalog/")


def load_entries() -> list[dict]:
    if not CATALOG.is_dir():
        raise Invalid(f"no catalog/ directory at {CATALOG}")

    errors: list[str] = []
    entries: list[dict] = []
    seen_repos: dict[str, str] = {}

    for path in sorted(CATALOG.glob("*/entry.toml")):
        rel = path.relative_to(ROOT)
        try:
            entry = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"{rel}: not valid TOML — {exc}")
            continue

        entry["_dir"] = path.parent.name
        entry["_path"] = rel

        for field in REQUIRED:
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{rel}: `{field}` is required and must be a non-empty string")

        # Unknown keys are an error, not ignored: a field that renders nothing is
        # indistinguishable from a field that was forgotten, and `source`/`docs`
        # were removed from this schema deliberately. Say so rather than
        # silently dropping what the author wrote.
        for key in sorted(set(entry) - ENTRY_KEYS - {"_dir", "_path", "_summary"}):
            errors.append(
                f"{rel}: unknown field `{key}`"
                + (" — this index carries no links; describe the project in about.md instead"
                   if key in ("source", "docs") else "")
            )

        if entry.get("project") != entry["_dir"]:
            errors.append(
                f"{rel}: `project = {entry.get('project')!r}` does not match its directory "
                f"{entry['_dir']!r} — the directory name is the identity"
            )

        artifacts = entry.get("artifact")
        if not isinstance(artifacts, list) or not artifacts:
            errors.append(f"{rel}: at least one [[artifact]] is required")
            artifacts = []

        for idx, art in enumerate(artifacts, start=1):
            where = f"{rel}: artifact {idx}"
            for key in sorted(set(art) - ARTIFACT_KEYS):
                errors.append(f"{where}: unknown field `{key}`")
            kind = art.get("kind")
            if kind not in KINDS:
                errors.append(f"{where}: `kind` must be one of {sorted(KINDS)}, got {kind!r}")

            repo = art.get("repository")
            if not isinstance(repo, str) or not repo.strip():
                errors.append(f"{where}: `repository` is required")
                continue
            if "://" in repo or repo.startswith("/") or repo.endswith("/"):
                errors.append(
                    f"{where}: `repository` must be registry-relative "
                    f"(e.g. `c2go-assess/student-amd64`), got {repo!r}"
                )
            if repo.startswith("ebruno/swtr-udemy-artifacts/"):
                errors.append(
                    f"{where}: `repository` must be relative to this project, not the full "
                    f"registry path — drop the `ebruno/swtr-udemy-artifacts/` prefix"
                )
            if repo in seen_repos:
                errors.append(
                    f"{where}: `{repo}` is already claimed by {seen_repos[repo]} — "
                    f"one entry per repository"
                )
            else:
                seen_repos[repo] = str(rel)

            tags = art.get("tags")
            if not isinstance(tags, list) or not tags:
                errors.append(f"{where}: `tags` must be a non-empty array")
                tags = []
            for tag in tags:
                if not isinstance(tag, str) or not tag:
                    errors.append(f"{where}: tags must be non-empty strings")
                elif tag.startswith(FORBIDDEN_TAG_PREFIXES):
                    errors.append(
                        f"{where}: tag {tag!r} is a per-build tag — a cleanup policy collects "
                        f"these, so the index may not promise them. Pin `latest`, a release tag, "
                        f"or a digest"
                    )

            digests = art.get("digests")
            if not isinstance(digests, dict):
                errors.append(
                    f"{where}: `digests` is required — the publishing project resolves them at "
                    f"push time, so this script never has to reach the registry"
                )
                digests = {}
            if set(digests) != set(tags):
                missing = sorted(set(tags) - set(digests))
                extra = sorted(set(digests) - set(tags))
                errors.append(
                    f"{where}: `digests` must cover exactly the declared tags"
                    + (f" — missing {missing}" if missing else "")
                    + (f" — not a declared tag: {extra}" if extra else "")
                )
            for tag, digest in digests.items():
                # Full form, not just the prefix: `sha256:` + 64 lowercase hex. A digest
                # that only looks right is unpinnable, and fails at `docker pull` time
                # rather than here — which is the wrong place to find out.
                if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
                    errors.append(
                        f"{where}: digest for {tag!r} must be `sha256:` followed by 64 hex "
                        f"characters, got {digest!r}"
                    )

            sizes = art.get("sizes", {})
            if sizes and not isinstance(sizes, dict):
                errors.append(f"{where}: `sizes`, when present, must be a table of tag = bytes")

        summary = entry.get("summary_file", "about.md")
        if not isinstance(summary, str) or not summary:
            errors.append(f"{rel}: `summary_file` must be a file name")
            summary = "about.md"
        entry["_summary"] = ""
        summary_path = path.parent / summary
        if not summary_path.is_file():
            errors.append(f"{rel}: summary file {summary!r} is missing next to entry.toml")
        else:
            text = summary_path.read_text(encoding="utf-8").strip()
            if not text:
                errors.append(f"{rel}: summary file {summary!r} is empty")
            else:
                entry["_summary"] = text
                lines = text.count("\n") + 1
                if lines > MAX_SUMMARY_LINES:
                    print(
                        f"warning: {rel}: {summary} is {lines} lines — this is a summary, not "
                        f"the project's documentation; link to that instead of copying it",
                        file=sys.stderr,
                    )

        entries.append(entry)

    if not entries and not errors:
        errors.append("catalog/ holds no `*/entry.toml` — an empty index is not a valid state")

    fail(errors)

    for path in (HEADER, FOOTER):
        if not path.is_file():
            raise Invalid(f"missing {path.relative_to(ROOT)}")

    return sorted(entries, key=lambda e: e["project"])


def human_size(n: object) -> str:
    """MB to one decimal, because whole MB hides a 0.8 MB spread between builds.

    Decimal units (1,000,000), not binary: the registry reports bytes, and the two
    conventions disagree by ~5% at this scale — enough to read as a mistake.
    """
    if not isinstance(n, int) or n <= 0:
        return "—"
    mb = n / 1_000_000
    return f"{mb:,.1f} MB" if mb >= 1 else f"{n / 1000:,.1f} kB"


def short_digest(digest: str) -> str:
    return f"{digest[:19]}…"


def ordered_tags(tags: list[str]) -> list[str]:
    """`latest` first, then the rest in a stable order.

    Declared order is a property of the entry, not of the artifact, so sorting
    here keeps the rendered table identical however an entry happens to list its
    tags. Release tags are sorted as strings rather than semver: an entry that
    wants a deliberate order should say so with tags that sort that way.
    """
    rest = sorted(tag for tag in tags if tag != "latest")
    return (["latest"] if "latest" in tags else []) + rest


def render(entries: list[dict]) -> str:
    header = HEADER.read_text(encoding="utf-8").rstrip()
    out: list[str] = [header.replace("{{registry_host}}", REGISTRY_HOST), ""]

    if len(entries) > 1:
        out.append("## Projects\n")
        for entry in entries:
            out.append(f"- {entry['title']}")
        out.append("")

    for entry in entries:
        out.append(f"## {entry['title']}\n")
        out.extend(entry["_summary"].splitlines())
        out.append("")

        # Facts only: licence, maintainer, the release. No links -- see the note
        # beside REQUIRED for why.
        meta = [entry["license"], f"maintained by {entry['maintainer']}"]
        if entry.get("published_from"):
            meta.append(f"published from `{entry['published_from']}`")
        out.append("*" + " · ".join(meta) + "*\n")

        # The image cell is a link: a URL, for opening the registry. The reference a
        # command needs is printed above the table, without a scheme.
        joined = next((a for a in entry.get("artifact", []) if "latest" in a["tags"]), None)
        if joined:
            out.append("Use the URL below for `container`, `docker` or `podman` commands.\n")
            reference = f"{REGISTRY_HOST}/{joined['repository']}:latest"
            out.append(f"[`{reference}`]({reference})\n")
        has_sizes = any(art.get("sizes") for art in entry.get("artifact", []))
        out.append("| image | tag | digest | size |" if has_sizes else "| image | tag | digest |")
        out.append("|---|---|---|---|" if has_sizes else "|---|---|---|")
        for art in entry.get("artifact", []):
            repo = art["repository"]
            cell = f"[`{repo}`](https://{REGISTRY_HOST}/{repo})"
            for tag in ordered_tags(art["tags"]):
                # Plain text: since the reference moved above the table in full, a link
                # here would be a second way to do the same job, and a second thing to keep
                # from disagreeing with the first.
                row = f"| {cell} | `{tag}` | `{short_digest(art['digests'][tag])}` "
                if has_sizes:
                    row += f"| {human_size(art.get('sizes', {}).get(tag))} "
                out.append(row + "|")
        out.append("")

        # Every row above, one line, with the digest written out: the table truncates
        # it, and a truncated digest is not something anyone can pin. One line per
        # declared tag rather than one per repository, so the counts match the table --
        # three tags sharing a digest then *show* that they are one content.
        if entry.get("artifact"):
            out.append(
                "Pin by digest — the digest is what the registry accepted, so it cannot be moved:\n"
            )
            out.append("```shell")
            block = [
                f"{REGISTRY_HOST}/{art['repository']}:{tag}@{art['digests'][tag]}"
                for art in entry.get("artifact", [])
                for tag in ordered_tags(art["tags"])
            ]
            out.append("\n\n".join(block))
            out.append("```\n")

        notes = [
            (art["repository"], (art.get("summary") or "").strip())
            for art in entry.get("artifact", [])
            if (art.get("summary") or "").strip()
        ]
        for repo, summary in notes:
            out.append(f"- `{repo}` — {summary}")
        if notes:
            out.append("")

    out.append(FOOTER.read_text(encoding="utf-8").rstrip())
    out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    mode = "--check"
    for arg in argv[1:]:
        if arg in ("--check", "--write", "--validate"):
            mode = arg
        elif arg in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            print(f"error: unknown argument {arg!r}; try --help", file=sys.stderr)
            return 2

    try:
        entries = load_entries()
    except Invalid as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rendered = render(entries)
    artifacts = sum(len(e.get("artifact", [])) for e in entries)
    print(f"catalog: {len(entries)} project(s), {artifacts} artifact(s)")

    if mode == "--validate":
        print("validate: ok")
        return 0

    if mode == "--write":
        README.write_text(rendered, encoding="utf-8")
        print(f"wrote {README.relative_to(ROOT)} ({len(rendered.splitlines())} lines)")
        return 0

    current = README.read_text(encoding="utf-8") if README.is_file() else ""
    if current == rendered:
        print(f"check: ok — {README.name} matches catalog/")
        return 0

    print(
        f"error: {README.name} is not what catalog/ produces.\n"
        f"       Run `python3 tools/build_catalog.py --write` and commit the result.\n"
        f"       (This file is generated; a hand edit is the failure, not the fix.)",
        file=sys.stderr,
    )
    if current:
        sys.stderr.writelines(
            difflib.unified_diff(
                current.splitlines(keepends=True),
                rendered.splitlines(keepends=True),
                fromfile=f"{README.name} (committed)",
                tofile=f"{README.name} (generated)",
            )
        )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
