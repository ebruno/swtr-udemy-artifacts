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

Pull `c2go-assess/student` and you get the architecture your host needs. The
per-architecture images are listed separately only for pinning — pin a version tag, or
name the digest, when the result has to be reproducible.

*BSD-3-Clause · maintained by ebruno · published from `0.5.2`*

| image | tag | digest | size |
|---|---|---|---|
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `latest` | `sha256:c9f9036aaa3c…` | — |
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `0.5.2` | `sha256:c9f9036aaa3c…` | — |
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `v0.5.15` | `sha256:c9f9036aaa3c…` | — |
| [`c2go-assess/student-amd64`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-amd64) | `0.5.2` | `sha256:5d246b5e8e9b…` | 214.8 MB |
| [`c2go-assess/student-arm64`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-arm64) | `0.5.2` | `sha256:52fec58ac89e…` | 210.2 MB |

Pin by digest — the digest is what the registry accepted, so it cannot be moved:

```shell
ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:latest@sha256:c9f9036aaa3cfdb68b39a01287da131352e892aa6b9fc14b7e9d461d1c93ea7a

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:0.5.2@sha256:c9f9036aaa3cfdb68b39a01287da131352e892aa6b9fc14b7e9d461d1c93ea7a

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:v0.5.15@sha256:c9f9036aaa3cfdb68b39a01287da131352e892aa6b9fc14b7e9d461d1c93ea7a

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-amd64:0.5.2@sha256:5d246b5e8e9b299b12593d38352d0c3a7c8c58af3658ec8fe22ed06d15d94add

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-arm64:0.5.2@sha256:52fec58ac89eba4846206f7a4d2b6645d6a1575393f099e7ec78725042248e40
```

---

**This repository is a synchronized copy.** It is published from another source
repository, and each push from there overwrites what is here — branches included.
Any change made on GitHub, on `main` or on a branch of your own, will be
overwritten, and a pull request based on one has nothing to merge into.
