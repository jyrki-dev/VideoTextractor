#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract frames from video input.

You can adjust the interval of the frame captures, the start and stop position
of the capture process, wether to write the frames to the disk as image files,
where to store them and in which format.

"""
import os
import sys
import cv2
import numpy as np


def extract_frames(
    video_source: cv2.VideoCapture, start: int, stop: int, interval: int
) -> list[np.ndarray]:
    """Extract frames from a video source and return them as ndarrays stored in
    a list.

    Args:
        video_source (cv2.VideoCapture): Video capture
        start (int): Timestamp (in seconds) when to start extracting
        stop (int): Timestamp (in seconds) when to stop extracting
        interval (int): Seconds how far between each saved frame is

    Returns:
        List of frames stored as np.ndarrays.
    """
    frames = []
    fps = video_source.get(cv2.CAP_PROP_FPS)
    if stop <= start:
        stop = video_source.get(cv2.CAP_PROP_FRAME_COUNT) // fps
    for sec in range(start, stop, interval):
        video_source.set(cv2.CAP_PROP_POS_FRAMES, (sec * fps))
        ret, frame = video_source.read()
        if not ret:
            raise cv2.error(f"Failed to retrieve frame at {sec * 25:.1f} sec.")
        frames.append(frame)
    return frames


def save_images(dir_path: str, frames: list[np.ndarray]) -> bool:
    """Takes a list of images in np.ndarray format and saves them to a directory,
    creating the directory if necessary.

    Args:
        dir_path (str): Path to the directory where to save the images.
        frames (list): List of cv2 frame captures.

    Returns:
        bool: True if succesfull, False if not.
    """
    try:
        os.makedirs(dir_path, exist_ok=False)
        print(f"Created directory '{dir_path}'...")
        count = 1
        for img in frames:
            cv2.imwrite(f"{dir_path}/{count}.jpg", img)
            print(f"Writing image {count}.jpg...")
            count += 1
        print("Success!")
        return True
    except FileExistsError as e:
        print(f"Error in creating the frame directory: {e}")
        return False


def extract_and_save(file_path: str, start: int = 0, stop: int = -1, interval: int = 1):
    """Extract frames and then save them to a directory.

    Args:
        file_path (str): [description]
        start (int, optional): [description]. Defaults to 0.
        stop (int, optional): [description]. Defaults to -1.
        interval (int, optional): [description]. Defaults to 1.
    """
    cap = cv2.VideoCapture(file_path)
    video_dir, video_name = os.path.split(file_path)
    frames_dir = f"{video_dir}/frames_{video_name[:-4]}"
    frames = extract_frames(cap, start, stop, interval)
    save_images(frames_dir, frames)


def quicksave(video_path: str, stop: int) -> None:
    """Exract frames from a video file and save them to a directory.

    Wrapper for extract_frames with less arguments to pass.

    Args:
        video_path (str): Path to the video file.
        stop (int): Time (in seconds) where to stop extracting sceenshots.
    """
    try:
        extract_and_save(video_path, 1, stop, 1)
    except FileNotFoundError as e:
        print(f"Error in the video file: {e}")
    except FileExistsError as e:
        print(f"Error in creating the frame directory: {e}")
    except cv2.error as e:
        print(f"Frame extraction error: {e}")


if __name__ == "__main__":
    quicksave(sys.argv[1], int(sys.argv[2]))
