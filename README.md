# SWTR Udemy course artifacts

What this project publishes — and nothing else. No build recipes, no source: each
section below is written by the project that publishes the artifact, and is
indexed from the file that project owns.

> **Where the images are published.** To **GitHub Container Registry**, under
> `ghcr.io/ebruno/swtr-udemy-artifacts/`. The packages are **public**, so pulls
> work anonymously — no GitHub account and no `docker login`, on any of the three
> clients below.

Pull by tag, and pin by digest when it matters. Docker, Podman and Apple's
`container` all take the same reference; only the command differs:

```shell
# Docker
docker pull ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>

# Podman — same reference, nothing to log in to
podman pull ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>

# Apple `container` (macOS): the pull verb lives under `image`, there is no
# top-level `container pull`.
container image pull ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>
container run --rm -it ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>
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

**This repository is a synchronized copy.** It is published from another source
repository, and each push from there overwrites what is here — branches included.
Any change made on GitHub, on `main` or on a branch of your own, will be
overwritten, and a pull request based on one has nothing to merge into.
