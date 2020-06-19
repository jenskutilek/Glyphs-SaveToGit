# encoding: utf-8

from __future__ import division, print_function, unicode_literals

import objc

import subprocess

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
    def saveAndCommit(self, sender):
        font = Glyphs.font
        font_path = font.filepath
        fontdir = dirname(font_path)
        fontfile = basename(font_path)

        # Add changed file to index

        font.save()

        cmd = ["git", "add", font_path]

        result = None
        # result = subprocess.run(cmd, capture_output=True)
        try:
            result = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, cwd=fontdir, shell=False
            )
        except subprocess.CalledProcessError as e:
            Glyphs.showNotification(
                self.name, "Error adding changes: %s" % e.output
            )

        # Commit changes

        cmd = ["git", "commit", "-m", "Update %s" % fontfile]

        # result = subprocess.run(cmd, capture_output=True)
        try:
            result = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, cwd=fontdir, shell=False
            )
        except subprocess.CalledProcessError as e:
            Glyphs.showNotification(
                self.name, "Error committing changes: %s" % e.output
            )
            return
        Glyphs.showNotification(self.name, str(result))

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
