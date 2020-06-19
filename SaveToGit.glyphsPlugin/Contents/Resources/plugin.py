# encoding: utf-8

from __future__ import division, print_function, unicode_literals

import objc

import subprocess
import tempfile

from os.path import basename, dirname

from AppKit import NSMenuItem
from GlyphsApp import FILE_MENU, Glyphs
from GlyphsApp.plugins import GeneralPlugin


class SaveToGit(GeneralPlugin):
    @objc.python_method
    def settings(self):
        self.name = Glyphs.localize(
            {"en": "Save to Git", "de": "In Git sichern"}
        )

    @objc.python_method
    def start(self):
        newMenuItem = NSMenuItem(self.name, self.saveAndCommit)
        Glyphs.menu[FILE_MENU].append(newMenuItem)

    @objc.python_method
    def run_git_cmd(self, args, working_dir=None):
        result = None
        # result = subprocess.run(cmd, capture_output=True)
        try:
            result = subprocess.check_output(
                args, stderr=subprocess.STDOUT, cwd=working_dir, shell=False
            )
        except subprocess.CalledProcessError as e:
            Glyphs.showNotification(self.name, "Error: %s" % e.output)
        return result

    @objc.python_method
    def build_commit_msg(self, old_font, new_font):
        msg = "Update %s %s" % (new_font.familyName, new_font.masters[0].name)
        return msg

    @objc.python_method
    def saveAndCommit(self, sender):
        font = Glyphs.font
        font_path = font.filepath
        fontdir = dirname(font_path)
        fontfile = basename(font_path)
        font.save()

        # Compare with last revision

        # Get previous version of the file
        old_data = self.run_git_cmd(
            ["git", "show", "HEAD:./%s" % fontfile], fontdir
        )

        # Save to a temp file and open it for comparison
        with tempfile.NamedTemporaryFile(suffix=".glyphs") as old_file:
            old_file.write(old_data)
            old_font = Glyphs.open(old_file.name, showInterface=False)
        msg = self.build_commit_msg(old_font, font)
        old_font.close()

        # Add changed file to index
        self.run_git_cmd(["git", "add", fontfile], fontdir)

        # Commit changes
        result = self.run_git_cmd(["git", "commit", "-m", msg], fontdir)
        Glyphs.showNotification(self.name, str(result))

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
