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
