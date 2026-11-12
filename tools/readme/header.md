# SWTR Udemy course artifacts

What this project publishes — and nothing else. No build recipes, no source: each
section below is written by the project that publishes the artifact, and is
indexed from the file that project owns.

> **Where the images are published.** To **GitHub Container Registry**, under
> `ghcr.io/ebruno/swtr-udemy-artifacts/`. If a package is private you need access
> to it and a login first (`docker login ghcr.io`, `podman login ghcr.io`,
> `container registry login ghcr.io`); the commands below assume you have that.

Pull by tag, and pin by digest when it matters. Docker, Podman and Apple's
`container` all take the same reference; only the command differs:

```shell
# Docker
docker pull ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>

# Podman — same reference, same registry login (`podman login ghcr.io`)
podman pull ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>

# Apple `container` (macOS): the pull verb lives under `image`, there is no
# top-level `container pull`. Authenticate first with
# `container registry login ghcr.io`.
container image pull ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>
container run --rm -it ghcr.io/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>
```

A digest is the immutable identity of a tag **as recorded when it was published**.
A tag can be moved to new content; a digest cannot, so it is what a reproducible
build should name.
