#!/usr/bin/env python3
"""Procedure to institute BRANCH symlinks.

BRANCH symlinks (in /.branch/) point agnostically to the locations of datalad siblings
across my BRANCH file structure. For the root dataset, the BRANCH symlinks must be manually
configured. However, by using this script when creating subdatasets, their BRANCH symlinks
utilize the root's to point directly to the sibling under the same hierarchy in another location.

Obviously this only works if the dataset hierarchy is the same in all places. For my project-
to-archive pipeline, this is true for the (B)ases and (H)istory BRANCHes. As of now, the
(R)outines and (A)toms BRANCHes may be of use to the root dataset, and as text-based branches
are unlikely to involve datasets. Finally, (N)exes and (C)ontent may use core subdatasets in
various other hierarchies, not following a predictable pattern, so they also aren't
included here.

For complete compatibility, also ensure subdirectories leading to the root of the BRANCH
folder structure include a `.vault-root` symlink pointing upward in a chain to the BRANCH
root. This facilitates the manual addition of symlinks to the root dataset so that their
structure is roughly (1-Bases -> ../.vault-root/1-Bases/A/B/Sibling). Then, this script's
symlinks of form (1-Bases -> ../.branch/1-Bases/SubSibling) combines in chain with other
.branch symlinks to reprorduce the dataset hierarchy.
"""

import sys
import os.path as op
from os import mkdir

from datalad.distribution.dataset import require_dataset
from datalad.utils import create_tree

ds = require_dataset(sys.argv[1], check_installed=True, purpose="BRANCH Symlink setup")

ds_name = op.basename(sys.argv[1])

to_modify = {
    ds.pathobj / ".branch" / "1-Bases": f"../../.branch/1-Bases/{ds_name}",
    ds.pathobj / ".branch" / "6-History": f"../../.branch/6-History/{ds_name}",
}

dirty = [
    s
    for s in ds.status(
        list(to_modify.keys()),
        result_renderer="disabled",
        return_type="generator",
    )
    if s["state"] != "clean"
]

if dirty:
    raise RuntimeError(
        "Stopping, because to be modified dataset "
        "content was found dirty: {}".format([s["path"] for s in dirty])
    )

###################################################################
# actually dump everything into the dataset
mkdir(ds.pathobj / ".branch")
for src, dest in to_modify.items():
    src.symlink_to(dest)

# leave clean
ds.save(
    path=to_modify,
    message="""Apply BRANCH dataset setup.

Insert symlinks in `/.branch/` pointing to parent datasets' to create
link chain to facilitate adding remotes.""",
    result_renderer="disabled",
)
