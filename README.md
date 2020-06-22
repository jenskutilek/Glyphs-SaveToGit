# Save to Git

A plugin for Glyphs.app that saves your font and commits the changes to a git repository. Well suited if you just want to keep track of your changes.

If you collaborate with others on a font through Git, you will definitely need another tool, as the need to compare and merge different revisions will probably arise. _Save to Git_ doesn't handle this. Maybe try [MergeGlyphs](https://glyphsapp.com/tools/mergeglyphs) and [CommitGlyphs](https://github.com/jenskutilek/SmartTypography-Extension/tree/safari/assets).

## Usage

Instead of using the normal Save command, use `File > Save to Git`. This will save your file and commit the changes to the git repository the current file is part of.

## Known Issues

- The `git` command line utility must be installed on your system (see below for instructions).
- The git repository must already be set up, and the Glyphs file must have been saved and committed.
- Set your own shortcut via system preferences.

## Git Installation

If you don't have the `git` command line utility installed, you can do so by opening the Terminal app and entering this command:

```bash
xcode-select --install
```
