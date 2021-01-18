# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Extract frames from video input.

You can adjust the interval of the frame captures, the start and stop position
of the capture process, wether to write the frames to the disk as image files,
where to store them and in which format.

TODO:
    - Instead of writing the frames as image files, implement a version
    of the function that keeps the frames in-memory for faster
    processing.
    - Implement the faster method for sets with lower interval
"""
import os
import cv2
import numpy as np
from decord import VideoReader
from decord import cpu


def extract_frames(video_path: str,
                   frames_dir: str,
                   start: int = 0,
                   stop: int = -1,
                   interval: int = 5) -> int:
    """Extract frames from a video source using VideoReader

    Args:
        video_path: Path to the video file.
        frames_dir: Directory to save the frames to.
        start: Timestamp (in seconds) when to start extracting
        stop: Timestamp (in seconds) when to stop extracting
        interval: Seconds how far between each saved frame is

    Returns:
        Int of how many images were saved.
    """
    video_dir, video_filename = os.path.split(video_path)
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Unable to find {video_file}!")
    vr = VideoReader(video_path, ctx=cpu(0))
    if stop < 0:
        stop = len(vr)  # Stops at last frame, if not specified
    fps = int(vr.get_avg_fps())  # int floors possible float
    interval = interval * fps
    start = start * fps
    stop = stop * fps
    frames_idx = list(range(start, stop, interval))
    img_count = 0
    if len(frames_idx) < 1000:  # To not overflow the memory
        frames = vr.get_batch(frames_idx).asnumpy()
        for index, frame in zip(frames_idx, frames):
            if img_count > 1000:
                raise Exception("Stuck in a loop")
                break
            save_path = os.path.join(frames_dir, video_filename,
                                     f"{index}.jpg")
            cv2.imwrite(save_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            img_count += 1
    return img_count


def video_to_frames(video_path: str,
                    frames_dir: str,
                    start: int = 0,
                    stop: int = -1,
                    interval: int = 5) -> str:
    """Extract frames from a video with the given parameters.

    Args:
        video_path: Path to the video file
        frames_dir: Directory to save the frames as images to
        interval: Time between each saved frame (in seconds)

    Returns:
        Path to the directory where the frames were written to, None if fails.
    """
    video_path = os.path.normpath(video_path)
    frames_dir = os.path.normpath(frames_dir)
    video_dir, video_filename = os.path.split(video_path)
    os.makedirs(os.path.join(frames_dir, video_filename), exist_ok=True)
    print(f"Extracting frames from {video_filename}...")
    extract_frames(video_path,
                   frames_dir,
                   start=start,
                   stop=stop,
                   interval=interval)
    return os.path.join(frames_dir, video_filename)


if __name__ == '__main__':
    video_to_frames('../data/CarsOnHighway_1080p.mp4',
                    "../data/frametesti",
                    start=0,
                    stop=20,
                    interval=5)
