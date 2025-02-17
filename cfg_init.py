#!/usr/bin/env python3
"""Procedure to initiate my datasets.

Based on txt2git, this adds lines to the .gitattribute file to track text in git
and most everything else in git-annex.

See [[Project-Naming-Convention]] for rationale involving rules associated with project structure.

The rules are:
- Use MD5E backend (MD5 hash is smaller + file extension (past the FIRST dot lol))
- Binary + larger than 1b (instead of 0: an empty file is always considered binary)
- Larger than 100 kB (typically indicative of a file not wanted in git even if text)
    - Could set to 100 MB to mimic GitHub's limits?

Author: Spencer Fretwell
Date: 2024-10-11
Version: 0.2
"""

import sys
import os.path as op
from os import mkdir

from datalad.distribution.dataset import require_dataset
from datalad.utils import create_tree

ds = require_dataset(sys.argv[1], check_installed=True, purpose="Nonbinary to git")
assert ds.repo is not None, "No datalad repo found"

annex_largefiles = "(((mimeencoding=binary)and(largerthan=1b))or(largerthan=100kb))"
annex_backend = "MD5E"
#: DL's txt2git checks each file literally for its attributes before modifying the file.
#: I am just adding the lines I want directly because I know the (global) setup I am working with.
ds.repo.set_gitattributes(
    [
        ("*", {"annex.largefiles": annex_largefiles}),
        ("*", {"annex.backend": annex_backend}),
        ("in/**", {"annex.largefiles": "anything"}),
        ("out/**", {"annex.largefiles": "anything"}),
    ]
)

#: write the gitattributes file (makes folders if not present)
[
    ds.repo.set_gitattributes(
        [
            ("*", {"annex.largefiles": "anything"}),
        ],
        f"{folder}/.gitattributes",
    )
    for folder in ["in", "out"]
]

git_attributes_file = op.join(ds.path, ".gitattributes")
ds.save(
    git_attributes_file,
    message="Set up a project repo per convention\n\ninitVersion:: 0.2\nprojectConventionVersion:: 0.1",
    result_renderer="disabled",
)
