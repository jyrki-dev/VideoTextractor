#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class for invidual video files.

Contains parameters for the located directory, video name, fps, possible
new name, and basic methods like get, set and in addition method to
rename the current file.
"""
import os


class Video:
    """Class for a video file."""
    def __init__(self, dir: str, name: str) -> None:
        """Initialize a new Video object.

        Args:
            dir (str): Directory where the file can be found.
            name (str): Filename of the video file.
        """
        self.directory = dir
        self.name = name
        self.new_name = ""


    @classmethod
    def frompath(self, path: str):
        video_dir, file_name = os.path.split(path)
        """Initialize a Video class from just a file path."""
        return self(video_dir, file_name)

    def set_new_name(cls, new_name: str):
        cls.new_name = new_name

    def rename(self):
        self.name = self.new_name
