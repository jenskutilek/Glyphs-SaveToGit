# encoding: utf-8

from __future__ import division, print_function, unicode_literals

import objc

import subprocess

from os import remove
from os.path import basename, dirname, join

from AppKit import NSClassFromString, NSMenuItem
from GlyphsApp import FILE_MENU, Glyphs, Message
from GlyphsApp.plugins import GeneralPlugin


GSCompareFonts = NSClassFromString("GSCompareFonts")


class SaveToGit(GeneralPlugin):
    @objc.python_method
    def settings(self):
        self.name = Glyphs.localize(
            {"en": "Save to Git", "de": "In Git sichern"}
        )

    @objc.python_method
    def start(self):
        # Set menu item so that it will call the validateMenuItem_ method
        saveAndCommitMenuItem = NSMenuItem.new()
        saveAndCommitMenuItem.setTitle_(self.name)
        saveAndCommitMenuItem.setTarget_(self)
        saveAndCommitMenuItem.setAction_(self.saveAndCommit_)
        Glyphs.menu[FILE_MENU].append(saveAndCommitMenuItem)

    def validateMenuItem_(self, menuItem):
        return Glyphs.font is not None

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
        glyphs = []
        for name in new_font.glyphs.keys():
            # Glyph has been added
            if name not in old_font.glyphs:
                glyphs.append(name)
                continue

            # Glyph comparison
            old_glyph = old_font.glyphs[name]
            new_glyph = new_font.glyphs[name]
            glyph_cmp = GSCompareFonts.compareGlyph_andGlyph_(
                old_font.glyphs[name], new_font.glyphs[name]
            )
            if glyph_cmp:
                glyphs.append(name)
                continue

            # Layer comparison
            num_old_layers = len(old_glyph.layers)
            num_new_layers = len(new_glyph.layers)
            if num_old_layers != num_new_layers:
                continue
            for i in range(num_old_layers):
                layer_cmp = GSCompareFonts.compareLayer_andLayer_(
                    old_glyph.layers[i], new_glyph.layers[i]
                )
                if layer_cmp:
                    glyphs.append(name)
        if glyphs:
            msg += ": " + ", ".join(sorted(set(glyphs)))
        return msg

    def saveAndCommit_(self, sender):
        font = Glyphs.font
        if font is None:
            return

        font_path = font.filepath
        if font_path is None:
            Message(
                message="Please save your Glyphs file once before using Save to Git.",
                title="Save to Git"
            )
            return

        fontdir = dirname(font_path)
        fontfile = basename(font_path)
        font.save()

        # Compare with last revision

        # Get previous version of the file
        old_data = self.run_git_cmd(
            ["git", "show", "HEAD:./%s" % fontfile], fontdir
        )
        if old_data is None:
            # Font probably is new in repository
            msg = "Add %s" % (new_font.familyName)
        else:
            # Save to a temp file and open it for comparison
            tmp_file_path = join(fontdir, ".de.kutilek.SaveToGit.%s" % fontfile)
            with open(tmp_file_path, "wb") as old_file:
                old_file.write(old_data)
                old_font = Glyphs.open(old_file.name, showInterface=False)
            msg = self.build_commit_msg(old_font, font)
            old_font.close()
            remove(tmp_file_path)

        # Add changed file to index
        self.run_git_cmd(["git", "add", fontfile], fontdir)

        # Commit changes
        self.run_git_cmd(["git", "commit", "-m", msg], fontdir)
        Glyphs.showNotification(self.name, msg)

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
