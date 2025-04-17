#!/usr/bin/env python3
"""Procedure to initiate my datasets.

Based on txt2git, this adds lines to the .gitattribute file to track text in git
and most everything else in git-annex.

See [Project Naming Convention](../../../0-Vaults/0-Meta/3STD-Standards/Project-Naming-Convention.md) for rationale involving rules associated with project structure.
See root.gitattributes for an example of the attributes file this produces in root.
See annexDir.gitattributes for an example of the attributes file for annex-only directories (e.g., in, out, src).

The rules are:
- Use MD5E backend (MD5 hash is smaller + file extension (past the FIRST dot lol))
- Binary + larger than 1b (instead of 0: an empty file is always considered binary)
- Larger than 100 kB (typically indicative of a file not wanted in git even if text)
    - Could set to 100 MB to mimic GitHub's limits?

Author: Spencer Fretwell
Date: 2025-05-06
Version: 0.6
"""

import sys
import os.path as op
from os import mkdir

from datalad.distribution.dataset import require_dataset, Dataset
from datalad.utils import create_tree

ds = require_dataset(sys.argv[1], check_installed=True, purpose="Nonbinary to git")
assert isinstance(ds, Dataset), "No dataset found"
assert ds.repo is not None, "No datalad repo found"

annex_largefiles = "(((mimeencoding=binary)and(largerthan=1b))or(largerthan=100kb))"
annex_backend = "MD5E"
#: DL's txt2git checks each file literally for its attributes before modifying the file.
#: I am just adding the lines I want directly because I know the (global) setup I am working with.
ds.repo.set_gitattributes(
    [
        ("*", {"annex.backend": annex_backend}),
        ("*", {"annex.largefiles": annex_largefiles}),
        (".git*", {"annex.largefiles": "nothing"}),
        ("**/.git*", {"annex.largefiles": "nothing"}),
        ("code/**", {"annex.largefiles": "nothing"}),
        ("docs/**", {"annex.largefiles": "nothing"}),
        ("envs/**", {"annex.largefiles": "nothing"}),
        ("in/**", {"annex.largefiles": "anything"}),
        ("out/**", {"annex.largefiles": "anything"}),
        ("bin/**", {"annex.largefiles": "anything"}),
        ("**/bin/**", {"annex.largefiles": "anything"}),
    ]
)

#: write the gitattributes file (makes folders if not present)
# attr_folders = ["in", "out", "bin"]
# [
#     ds.repo.set_gitattributes(
#         [
#             ("*", {"annex.largefiles": "anything"}),
#             (".gitattributes", {"annex.largefiles": "nothing"}),
#         ],
#         f"{folder}/.gitattributes",
#     )
#     for folder in attr_folders
# ]

#: Create remaining folders (if not present)
for folder in ["in", "out", "bin", "code", "docs", "envs"]:
    if not op.exists(op.join(ds.path, folder)):
        mkdir(op.join(ds.path, folder))

#: Ignore anything within the dev folder or that has dev in the name
with open(op.join(ds.path, ".gitignore"), "a+") as f:
    f.write("dev/\n*dev*\n**/dev/\n")

modfiles = [
    op.join(ds.path, ".gitattributes"),
    op.join(ds.path, ".gitignore"),
]
ds.save(
    modfiles,
    message="Set up a project repo per convention\n\ninitVersion:: 0.6\nprojectConventionVersion:: 0.13",
    result_renderer="disabled",
)
