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
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `latest` | `sha256:c2e682ac31e8…` | — |
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `0.5.2` | `sha256:c2e682ac31e8…` | — |
| [`c2go-assess/student`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student) | `v0.5.14` | `sha256:c2e682ac31e8…` | — |
| [`c2go-assess/student-amd64`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-amd64) | `0.5.2` | `sha256:668b7f8a0a36…` | 214.8 MB |
| [`c2go-assess/student-arm64`](https://ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-arm64) | `0.5.2` | `sha256:3a4bcc98296a…` | 210.2 MB |

Pin by digest — the digest is what the registry accepted, so it cannot be moved:

```shell
ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:latest@sha256:c2e682ac31e8d634cf3b845c3900e85da0729db2bc56fc14b9bc1b5432067fb3

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:0.5.2@sha256:c2e682ac31e8d634cf3b845c3900e85da0729db2bc56fc14b9bc1b5432067fb3

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student:v0.5.14@sha256:c2e682ac31e8d634cf3b845c3900e85da0729db2bc56fc14b9bc1b5432067fb3

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-amd64:0.5.2@sha256:668b7f8a0a364815f7b90984a154c59e1a1d6255e8524c26c00b6d3c3cba6412

ghcr.io/ebruno/swtr-udemy-artifacts/c2go-assess/student-arm64:0.5.2@sha256:3a4bcc98296a1bc160bff09cdc5499e0bf8e1a88fb16a919513f7947ec1b1eb6
```

---

**This repository is a synchronized copy.** It is published from another source
repository, and each push from there overwrites what is here — branches included.
Any change made on GitHub, on `main` or on a branch of your own, will be
overwritten, and a pull request based on one has nothing to merge into.
