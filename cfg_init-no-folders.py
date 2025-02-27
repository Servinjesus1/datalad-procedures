#!/usr/bin/env python3
"""Procedure to initiate my datasets.

Based on txt2git, this adds lines to the .gitattribute file to track text in git
and most everything else in git-annex.

Author: Spencer Fretwell
Date: 2025-02-24
Version: 0.1
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
    ]
)

modfiles = [
    op.join(ds.path, ".gitattributes"),
    op.join(ds.path, ".gitignore"),
]
ds.save(
    modfiles,
    message="Set up a generic repo per convention\n\ninitNoFoldersVersion:: 0.1",
    result_renderer="disabled",
)
