#!/bin/bash
python main.py | ffmpeg -f rawvideo -pixel_format rgba -video_size 256x512 -framerate 60 -i - -y output.mp4
