#!/bin/bash
python main.py | ffplay -f rawvideo -pixel_format rgba -video_size 256x512 -framerate 30 -i -
