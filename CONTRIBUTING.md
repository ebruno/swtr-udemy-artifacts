# Contributing an entry

This project is an **index**, not a build. Nothing here produces a container; it
records what other projects have published, and renders that as `README.md`.

## The rule that governs everything

**`README.md` is generated. `catalog/` is the source.** If the two disagree, CI
fails — that is the entire mechanism, and it only works if nothing else writes
the README.

**A publishing project owns its own words.** Everything under
`catalog/<project>/` — the `title`, the `about.md` prose, the rows — is written by
the project that publishes the artifact, and the index renders it verbatim. This
repository never authors or edits another project's description; if the wording
is wrong, the fix belongs in that project's pipeline, not here.

**The page carries no links.** Not to source, not to docs, not to the registry
beyond the pull commands. A publishing project may have no public repository at
all, and a URL that resolves only behind a login is worse than no URL: it looks
like an answer and is not one. Each section states the project, its licence, its
maintainer and the release; anything richer belongs in that project's own
documentation. `source` and `docs` were removed from the schema for this reason,
and adding either back is a validation error rather than a silent no-op.

```
catalog/<project>/entry.toml     # machine: what exists, which tags, digests
catalog/<project>/about.md       # prose: a few lines, plus links
tools/build_catalog.py           # validate + render; never talks to the registry
tools/readme/header.md           # hand-edited intro
tools/readme/footer.md           # hand-edited generated-file notice
README.md                        # GENERATED — do not edit
```

## Publishing project: how to add or update an entry

The publishing pipeline does all of this in one commit, on a branch, then opens a
merge request:

1. Clone this repo, `git pull --rebase` (something else may have committed to
   `main` since you looked).
2. Write or update `catalog/<project>/entry.toml` and `about.md`.
3. Record the digests **you just pushed** — `docker push` prints them, or read
   them back from the registry (`GET /projects/:id/registry/repositories/:rid/tags/:tag`).
4. Run `python3 tools/build_catalog.py --write`. **Commit the regenerated
   `README.md` with the entry, in the same commit** — the branch is then
   reviewable as one change: the entry, the prose, and the row that appears.
5. If the content is unchanged, push nothing. A re-run of the same release must
   not create an empty commit.

You need write access to this repository. Releases are sequential, so there is no
locking and no conflict protocol: one `pull --rebase` before the push, and a retry
if the push is rejected.

## What the generator enforces, and why

| Rule | Reason |
|---|---|
| `project` == its directory name | The directory is the identity; a mismatch means the entry was copied |
| No tag starting `r-` or `sha-` | Both are per-build classes a registry cleanup policy collects. Only `latest` is unconditionally retained, so those tags cannot be promises |
| Every tag needs a digest | A tag can move; the digest is what makes a row reproducible. A tag without one is an unpinnable promise |
| Digests live in `entry.toml`, not fetched at build time | Generation must be a pure function of the commit, so `--check` is meaningful on a branch. Fetching live makes the same commit produce different output on different days |
| `repository` is registry-relative (`c2go-assess/student`, not the full path) | The registry host and project path belong in one place: the template |
| One entry per repository | Two projects claiming one repository is a publishing bug, not an index feature |
| `about.md` ≤ 30 lines (warning) | This is a summary. The project's own docs are the documentation; copying them creates a second source of truth that ages |

## What CI does, and on which refs

| Ref | Behaviour |
|---|---|
| merge request | `--check`: the branch must carry the regenerated `README.md` |
| `main` | `--check`: the merge carried it, so `main` never needs a generated commit |
| tag | `--check` |

There is deliberately **no** scheduled regeneration: it would either rewrite the
file for no reason or produce a diff nobody asked for. Registry drift — a tag
retention collected — is a separate check, and belongs in a job that is allowed
to fail for reasons other than a commit.

## Licence

The **index itself** — this repository's text and tooling — is **BSD-3-Clause**; the
terms are in [`LICENSE`](LICENSE).

That is not the same thing as an artifact's licence. Each entry declares its own in
`entry.toml` (`license = "…"`), and that value is what the page shows beside the
project. Two entries may publish under different terms, and a project may publish
under terms this repository does not use — so read the section, not the repository,
when the question is about what you are pulling.

## What does not belong here

- **No links at all.** The generator renders none, and unknown fields are rejected,
  so a link cannot be slipped in as an extra key.
- **No registry credentials.** This repo never pulls, pushes or queries the
  registry in CI.
- **No scraping the registry to discover artifacts.** Enumeration tells you what
  exists; the entries say what each thing is *for*. That distinction is why this
  repo exists at all.
- **No entries for internal images.** A project's test-matrix flavours, executor
  images and probe repositories stay out unless they have a reason to be pulled
  by someone outside the project.

## Where the images are addressed

Images are published to **GitHub Container Registry**, under
`ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>`. The packages are
**public**, so pulling needs no GitHub account.

The registry host appears in exactly one place,
[`tools/readme/header.md`](tools/readme/header.md). An entry's `repository` stays
registry-relative (`c2go-assess/student`), so changing where artifacts are
addressed is a one-line edit and never a sweep through `catalog/`.
