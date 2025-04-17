# Custom Datalad Procedures

`init` - Initialize a new Project dataset

I basically only use this one procedure. It initializes the dataset with the desired attributes to ensure desired annexing of files. It also opinionates the hierearchy of the dataset (`in` and `out` directories for now).

## Archive

`BRANCH` - Project to Archive Pipeline via Symlinks

The idea here was to use symlinks to connect dataset siblings in the Project and Archive folders (and other places). This way, all data is stored in the Archive sibling while only relevant copies are stored in the Project and Resource siblings (note I am confounding PARA and BRANCH nomenclature here: P=Bases, R=Content, A=History). However, this adds too much complexity by requiring the management of two to three siblings per project on each machine. Instead, I am testing out storage of all repos in Content or History indefinitely, with Project-like repos being stored in History and more Area-like repos stored in Content. Further, I am moving away from storing export in Content unless it's published and in PDF form. Instead, anything of interest made in Project repos will be linked to in Nexes or Atom notes (which should be used in the creation of export anyway, ergo the Project to Publication pipeline is maintained).

For now it is a useful example of writing a dl procedure, and a reminder that symlinks can be chained to create a network.

## Changelog: Init

- v0.6 (2025-05-06)
  - No `refs/` - too many submodules. Use git-annex.
- v0.5 (2025-04-21)
  - Changed `src/` to `bin/` and made all `bin` binaries.
  - Note this is motivated by Excalidraw/Obsidian since symlinks to `out` would NOT work in this case. Thus all attachments go in a `bin` subfolder. Still use a `.root` symlink and path to `out` rather than `code/../out` etc.
- v0.4
  - Deprecate `annexDir.gitattributes`. Put all in root `.gitattributes`.