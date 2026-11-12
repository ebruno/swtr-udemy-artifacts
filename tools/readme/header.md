# SWTR course artifacts

What this project publishes in its own container registry — and nothing else. No
build recipes, no source: each section below is written by the project that
publishes the artifact, and is indexed from the file that project owns.

> **Where the images live.** The registry is `registry.brunoe.net`, on the course
> LAN. This index is mirrored to GitHub for readability, but the pull commands
> only work from a host that can reach that registry and has been given access —
> **the images are not anonymously pullable**. Reading this from outside the
> course, the links that will work for you are `source` and `docs`.

Pull by tag, and pin by digest when it matters:

```shell
docker pull registry.brunoe.net/ebruno/swtr-udemy-artifacts/<project>/<image>:<tag>
```

A digest is the immutable identity of a tag **as recorded when it was published**.
A tag can be moved to new content; a digest cannot, so it is what a reproducible
build should name.
