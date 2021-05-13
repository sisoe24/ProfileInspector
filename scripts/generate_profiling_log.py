# coding: utf-8
from __future__ import print_function, with_statement

import re
import regex
import argparse
from random import randint
import xml.etree.ElementTree as ET

file = 'other/example/report_base.xml'

xml = ET.parse(file)
root = xml.getroot()


def randomize_timings():
    with open(file) as f:
        contents = f.read()
        rx = str(randint(1, 10000))
        sub = regex.sub(
            r'(<(?:callCount|timeTaken.+)+>)(\d+)(</\w+>)',
            r'\1' + rx + r'\3', contents)
        print(sub)


def update_log(num_frames):
    print('update log with %s frames' % num_frames)

    frame_element = root.find('Frame')

    for _ in range(num_frames):
        root.append(frame_element)

    xml.write('log/example_profiling_log.xml')


PARSER = argparse.ArgumentParser(description="")
PARSER.add_argument("-v", "--verbosity", action="store_true",
                    help="Increas output verbosity")
PARSER.add_argument("-u", "--update", type=int,
                    help="Update log file with a new version")
PARSER.add_argument("-r", "--random", action='store_true',
                    help="Randomize timings inside xml file")

ARGS = PARSER.parse_args()
if ARGS.update:
    update_log(ARGS.update)
elif ARGS.random:
    randomize_timings()
