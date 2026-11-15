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

Use the URL below for `container`, `docker` or `podman` commands.

[`ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:latest`](ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:latest)

| image | tag | digest | size |
|---|---|---|---|
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `latest` | `sha256:ff7560f165b2…` | — |
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `0.5.2` | `sha256:ff7560f165b2…` | — |
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `v0.5.16` | `sha256:ff7560f165b2…` | — |
| [`c2go-assess/student-amd64`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-amd64) | `0.5.2` | `sha256:1ecc5d87b57a…` | 214.8 MB |
| [`c2go-assess/student-arm64`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-arm64) | `0.5.2` | `sha256:9258e9308ba6…` | 210.2 MB |

Pin by digest — the digest is what the registry accepted, so it cannot be moved:

```shell
ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:latest@sha256:ff7560f165b2c7f4e6310ecb2f46ee9d93dca0ac99466cea3c9671684c95a278

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:0.5.2@sha256:ff7560f165b2c7f4e6310ecb2f46ee9d93dca0ac99466cea3c9671684c95a278

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:v0.5.16@sha256:ff7560f165b2c7f4e6310ecb2f46ee9d93dca0ac99466cea3c9671684c95a278

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-amd64:0.5.2@sha256:1ecc5d87b57afbf03dd8520d01f0f97132f2f2c84fd7fe11c2d06d75efee958c

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-arm64:0.5.2@sha256:9258e9308ba6531fa9a5e06f1a138d1c79b02e3c7cef0988d37f099edf475409
```

---

**This repository is a synchronized copy.** It is published from another source
repository, and each push from there overwrites what is here — branches included.
Any change made on GitHub, on `main` or on a branch of your own, will be
overwritten, and a pull request based on one has nothing to merge into.
