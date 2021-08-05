# coding: utf-8
from __future__ import print_function

import os

from ..report_parser import XmlData

FILES = [
    'other/samples/example_profiling_log.xml',
    'other/samples/report_unclosed_tags.xml',
    'other/samples/example_profiling_simple.xml',
    'other/samples/report_wrong_type.xml',
    'other/samples/report_wrong_syntax.xml',
    'other/samples/profiling_report_nuke13.xml',
]


def _bypass_filedialog(func):
    """Development only function. Bypass asking user for filedialog."""
    def inner_wrapper(*args, **kwargs):
        status = None
        self = args[0]

        # if test env then load xml file otherwise just call self
        if os.getenv('TEST_ENV') == '1':
            path = os.path.join(os.getenv('PWD'), FILES[0])
            status = XmlData.load_file(path, self)

        func(self)

        if status:
            self._show_inspector()

    return inner_wrapper
