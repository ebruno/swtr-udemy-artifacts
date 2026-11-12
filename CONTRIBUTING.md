# Contributing an entry

This project is an **index**, not a build. Nothing here produces a container; it
records what other projects have published to `registry.brunoe.net` and renders
that as `README.md`.

## The rule that governs everything

**`README.md` is generated. `catalog/` is the source.** If the two disagree, CI
fails — that is the entire mechanism, and it only works if nothing else writes
the README.

**A publishing project owns its own words.** Everything under
`catalog/<project>/` — the `title`, the `about.md` prose, the rows — is written by
the project that publishes the artifact, and the index renders it verbatim. This
repository never authors or edits another project's description; if the wording
is wrong, the fix belongs in that project's pipeline, not here.

**Links must be public.** `source` and `docs` have to be `https://github.com/…`.
The public face of this repository is its **GitHub mirror**, so a
`gitlab01.brunoe.net` link is a dead link for nearly every reader. A project needs
a GitHub mirror *before* it can be listed — that is enforced, not advised.

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

Access is a **deploy key with write on this repository, and nothing else**. There
is one writer at a time (single-user instance, sequential releases), so there is
no locking and no conflict protocol: one `pull --rebase` before the push, and a
retry if the push is rejected.

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

## What does not belong here

- **No internal links.** `source` and `docs` are rendered into a page read on
  GitHub; a `gitlab01.brunoe.net` URL is refused at validation for that reason.
- **No registry credentials.** This repo never pulls, pushes or queries the
  registry in CI.
- **No scraping the registry to discover artifacts.** Enumeration tells you what
  exists; the entries say what each thing is *for*. That distinction is why this
  repo exists at all.
- **No entries for internal images.** A project's test-matrix flavours, executor
  images and probe repositories stay out unless they have a reason to be pulled
  by someone outside the project.

## Where the images are addressed

**The public reference is GitHub Container Registry**:
`ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>` — the same account
that hosts this repository on GitHub. Every pull command in the generated README
points there, and the internal registry host is **not named on the page at all**,
for the same reason a gitlab01 link is refused: a reader arriving from GitHub
cannot reach it.

The host lives in exactly one place, [`tools/readme/header.md`](tools/readme/header.md).
An entry's `repository` stays registry-relative (`c2go-assess/student`), so
changing the public host is a one-line edit and never a sweep through `catalog/`.

**The SWTR packages are public** (owner, 2026-11-12), and that is a decision rather
than a default. GitHub creates every package **private** on first publish, so a new
`swtr-udemy-artifacts/…` package has to be flipped to public after its first push —
and the docs are explicit that **public is a one-way door: it cannot be made private
again**. Only for the Container registry do public packages allow anonymous pulls,
which is the whole point here: a student should not need a GitHub account to run
the assessment.

**`softwaretrace-ostools/archlinux` is private on purpose** (owner, 2026-11-12) — not
an oversight and not the pattern to copy. Two namespaces, two access models: that
package is private, `swtr-udemy-artifacts` is public. Do not "tidy" one to match
the other, and do not carry an assumption about visibility from one to the next.

**State at 2026-11-12**, read with the GitHub admin token from 1Password
(`Infrastructure`, item `v3yx3gtsvennk5pizrmrvzwnxq`):

- That package's **nested name** matches the `<project>/<image>` path shape this
  page uses.
- **`ebruno/swtr-udemy-artifacts` and `ebruno/c2go-assess` do not exist on GitHub
  yet**, which is why the page's `source` and `docs` links 404, and no SWTR package
  exists on ghcr — so neither the links nor the pulls resolve today.
- The token expires **2027-10-20** and carries `repo` and `write:packages`, so it
  can create the mirrors and push to ghcr. It is a person's admin token, not a
  narrow machine credential: if CI ever needs it, mint something scoped to the
  package instead of handing a pipeline this.

A companion check belongs with it, and is not built: resolve each listed
`repository:tag` at the public host and fail when one is missing — the registry half
of what `--check` does for the file. It cannot live in the commit-triggered job,
for the reason in `tools/build_catalog.py`: a check whose answer changes without a
commit gets switched off.
