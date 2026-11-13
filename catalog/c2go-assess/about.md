Runs the `c2go-assess` suite without installing Python or clang: the student image
carries both, and it is the only image in that project with a stability promise.

Pull `c2go-assess/student` and you get the architecture your host needs. The
per-architecture images are listed separately only for pinning — pin a version tag, or
name the digest, when the result has to be reproducible.
