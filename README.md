# Save to Git

A plugin for Glyphs.app that saves your font and commits the changes to a git repository.

## Usage

Instead of using the normal Save command, use `File > Save to Git`. This will save your file and commit the changes to the git repository the current file is part of.

## Known Issues

- The `git` command line utility must be installed on your system (see below for instructions).
- The git repository must already be set up, and the Glyphs file must have been saved.
- The commit message just says "Updated <Family Name> <First Master Name>", maybe more detailed change reports can be generated in the future.
- Set your own shortcut via system preferences.

## Git Installation

If you don't have the `git` command line utility installed, you can do so by opening the Terminal app and entering this command:

```bash
xcode-select --install
```
