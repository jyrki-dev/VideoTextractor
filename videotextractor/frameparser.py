#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract frames from video input.

You can adjust the interval of the frame captures, the start and stop position
of the capture process, wether to write the frames to the disk as image files,
where to store them and in which format.

TODO:
    - Rework to work without decord
    - Instead of writing the frames as image files, implement a version
    of the function that keeps the frames in-memory for faster
    processing.
    - Implement the faster method for sets with lower interval
"""
import os
import cv2


def extract_frames(
    video_path: str, start: int = 0, stop: int = -1, interval: int = 1
) -> int:
    """Extract frames from a video source using VideoReader

    Args:
        video_path: Path to the video file.
        start: Timestamp (in seconds) when to start extracting
        stop: Timestamp (in seconds) when to stop extracting
        interval: Seconds how far between each saved frame is

    Returns:
        Int of how many images were saved.
    """
    # TODO: Frame based selection, proper error handling
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Unable to find {video_path}!")
    img_count = 0
    video_dir, video_name = os.path.split(video_path)
    frames_dir = f"{video_dir}/frames_{video_name}"
    os.makedirs(frames_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if stop <= start:
        stop = cap.get(cv2.CAP_PROP_FRAME_COUNT) // cap.get(cv2.CAP_PROP_FPS)
    for sec in range(start, stop, interval):
        cap.set(cv2.CAP_PROP_POS_MSEC, (sec * 1000))
        ret, frame = cap.read()
        if not ret:
            print(
                f"Failed to retrieve frame at {sec:.1f} seconds"
            )  # Replace with proper raise Exception
            continue
        cv2.imwrite(f"{frames_dir}/{video_name}{sec}.jpg", frame)
        img_count += 1
    return img_count


if __name__ == '__main__':
    n_frames = extract_frames('data/ANP1090.mp4', 0, 15, 1)
    print(f"Extracted and saved {n_frames} from the video file.")
