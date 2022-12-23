#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class for invidual video files.

Contains parameters for the located directory, video name, fps, possible
new name, and basic methods like get, set and in addition method to
rename the current file.

TODO:
    - Create methods for handling changes directly in the filesystem.
"""
import os

from numpy import ndarray


class Video:
    """Class for a video file."""
    def __init__(self, directory: str, name: str) -> None:
        """Initialize a new Video object.

        Args:
            dir (str): Directory where the file can be found.
            name (str): Filename of the video file.
        """
        self.directory = directory
        self.name = name
        self.new_name = name
        self.frames = []  # Store here for for easy access?

    @classmethod
    def frompath(cls, path: str):
        video_dir, file_name = os.path.split(path)
        """Initialize a Video class from just a file path."""
        return cls(video_dir, file_name)

    def __str__(self):
        return f"Video file: {self.name}\n \
                 Directory: {self.directory}\n \
                 Proposed name: {self.new_name}"

    def __repr__(self):
        return (f"Video(name={self.name}, directory={self.directory} ,"
                f"new name = {self.new_name}")

    def set_new_name(self, new_name: str):
        self.new_name = new_name

    def rename(self):
        self.name = self.new_name
