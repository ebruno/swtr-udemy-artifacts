# SWTR Udemy course artifacts

What this project publishes in its own container registry — and nothing else. No
build recipes, no source: each section below is written by the project that
publishes the artifact, and is indexed from the file that project owns.

> **Where the images live.** The registry is `registry.brunoe.net`, on the course
> LAN. This page is generated from the GitLab repository and published from its
> GitHub mirror, but the pull commands only work from a host that can reach the
> registry and has been given access — **the images are not anonymously
> pullable**. Reading this from outside the course, the links that will work for
> you are `source` and `docs`.

Pull by tag, and pin by digest when it matters. Docker, Podman and Apple's
`container` all take the same reference; only the command differs:

```shell
# Docker
docker pull registry.brunoe.net/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>

# Podman — same reference, same registry login (`podman login registry.brunoe.net`)
podman pull registry.brunoe.net/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>

# Apple `container` (macOS): the pull verb lives under `image`, there is no
# top-level `container pull`. Authenticate first with
# `container registry login registry.brunoe.net`.
container image pull registry.brunoe.net/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>
container run --rm -it registry.brunoe.net/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>
```

A digest is the immutable identity of a tag **as recorded when it was published**.
A tag can be moved to new content; a digest cannot, so it is what a reproducible
build should name.

## c2go-assess — student runtime image

Runs the `c2go-assess` suite without installing Python or clang: the student image
carries both, and it is the only image in that project with a stability promise.

Pull `c2go-assess/student` and you get the right architecture for your host. The
per-architecture images are listed separately only for pinning — and note that
**their `latest` tags are not the current release**: pin a version tag, or name
the digest, when the result has to be reproducible.

*BSD-3-Clause · maintained by ebruno · [source](https://github.com/ebruno/c2go-assess) · [docs](https://github.com/ebruno/c2go-assess/blob/main/containers/README.md) · published from `0.5.2`*

| image | tag | digest | size |
|---|---|---|---|
| `c2go-assess/student` | `latest` | `sha256:554f1e60c5b3…` | — |
| `c2go-assess/student` | `0.5.2` | `sha256:554f1e60c5b3…` | — |
| `c2go-assess/student-amd64` | `latest` | `sha256:10614c4ccbfc…` | 215 MB |
| `c2go-assess/student-amd64` | `0.5.2` | `sha256:d9ef28fb1488…` | 215 MB |
| `c2go-assess/student-arm64` | `latest` | `sha256:929fb05b75ef…` | 210 MB |
| `c2go-assess/student-arm64` | `0.5.2` | `sha256:0fc860eafbb7…` | 210 MB |

- `c2go-assess/student` — multi-arch index — pull this one and you get the architecture your host needs (no size: a manifest index carries no layers of its own)
- `c2go-assess/student-amd64` — `latest` here is **not** the 0.5.2 release — it is the 0.5.0 content and has not moved since 2026-11-06. Pin `0.5.2`, or pull the multi-arch index above
- `c2go-assess/student-arm64` — same caveat as amd64: `latest` is the 0.5.0 content, not 0.5.2

---

**This file is generated.** `README.md` is the output of
[`tools/build_catalog.py`](tools/build_catalog.py) over
[`catalog/`](catalog/). Do not edit it by hand and do not add a section to it:
CI fails when this file is not byte-for-byte what the catalog produces, so a hand
edit is a red pipeline rather than a quiet divergence.

To publish or change an entry, see [`CONTRIBUTING.md`](CONTRIBUTING.md).
