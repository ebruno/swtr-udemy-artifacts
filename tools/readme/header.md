# SWTR Udemy course artifacts

What this project publishes — and nothing else. No build recipes, no source: each
section below is written by the project that publishes the artifact, and is
indexed from the file that project owns.

> **Where the images are published.** To **GitHub Container Registry**, under
> `{{registry_host}}/`. The packages are **public**, so pulls
> work anonymously — no GitHub account and no `docker login`, on any of the three
> clients below.

Pull by tag, and pin by digest when it matters. Docker, Podman and Apple's
`container` all take the same reference; only the command differs:

```shell
# Docker
docker pull {{registry_host}}/<project>/<image>:<tag>

# Podman — same reference, nothing to log in to
podman pull {{registry_host}}/<project>/<image>:<tag>

# Apple `container` (macOS): the pull verb lives under `image`, there is no
# top-level `container pull`.
container image pull {{registry_host}}/<project>/<image>:<tag>
container run --rm -it {{registry_host}}/<project>/<image>:<tag>
```

A digest is the immutable identity of a tag **as recorded when it was published**.
A tag can be moved to new content; a digest cannot, so it is what a reproducible
build should name.
