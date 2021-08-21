#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract frames from video input.

You can adjust the interval of the frame captures, the start and stop position
of the capture process, wether to write the frames to the disk as image files,
where to store them and in which format.

TODO:
    - Instead of writing the frames as image files, implement a version
    of the function that keeps the frames in-memory for faster
    processing (Like keep the images in an array)
"""
import os
import sys
import cv2


def extract_frames(
    video_path: str, start: int = 0, stop: int = -1, interval: int = 1
) -> tuple:
    """Extract frames from a video source using VideoReader

    Args:
        video_path: Path to the video file.
        start: Timestamp (in seconds) when to start extracting
        stop: Timestamp (in seconds) when to stop extracting
        interval: Seconds how far between each saved frame is

    Returns:
        Tuple, containing the path to the directory and count of
        frames extracted.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File '{video_path}' not found.")
    img_count = 0
    video_dir, video_name = os.path.split(video_path)
    frames_dir = f"{video_dir}/frames_{video_name[:-4]}"
    os.makedirs(frames_dir, exist_ok=False)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if stop <= start:
        stop = cap.get(cv2.CAP_PROP_FRAME_COUNT) // fps
    for sec in range(start, stop, interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, (sec * 25))
        ret, frame = cap.read()
        if not ret:
            raise cv2.error(f"Failed to retrieve frame at {sec * 25:.1f} sec.")
        cv2.imwrite(f"{frames_dir}/{sec}.jpg", frame)
        img_count += 1
    return (frames_dir, img_count)


def save_images(dir_path: str, frames: list) -> int:
    """Takes an array of images and saves them to a directory.

    Args:
        dir_path (str): Path to the directory where to save the images.
        frames (list): List of cv2 frame captures.

    Returns:
        int: Count of images saved.
    """
    try:
        os.makedirs(dir_path, exists_ok=False)
        count = 1
        for img in frames:
            cv2.imwrite(f"{dir_path}/{count}.jpg", img)
            count += 1
        return count
    except FileExistsError as e:
        print(f"Error in creating the frame directory: {e}")
        return 0



def quicksave(video_path: str, stop: int) -> None:
    """Exract frames from a video file and save them to a directory.

    Wrapper for extract_frames with less arguments to pass.

    Args:
        video_path (str): Path to the video file.
        stop (int): Time (in seconds) where to stop extracting sceenshots.
    """
    try:
        dir_path, img_count = extract_frames(video_path, 1, stop, 1)
        print(f"Succesfully retrieved {img_count} frames to {dir_path}!")
    except FileNotFoundError as e:
        print(f'Error in the video file: {e}')
    except FileExistsError as e:
        print(f'Error in creating the frame directory: {e}')
    except cv2.error as e:
        print(f"Frame extraction error: {e}")


if __name__ == '__main__':
    quicksave(sys.argv[1], int(sys.argv[2]))
