# coding: utf-8
from __future__ import print_function

import os

from ..report_parser import XmlData


def _bypass_filedialog(func):
    """developlement only function.

    bypass asking user for filedialog.
    """
    def inner_wrapper(*args, **kwargs):
        status = None
        self = args[0]
        if os.getenv('_TEST_ENV') == '1':
            # file = 'other/samples/example_profiling_log.xml'
            # file = 'other/samples/report_unclosed_tags.xml'
            # file = 'other/samples/example_profiling_simple.xml'
            file = 'other/samples/report_wrong_type.xml'
            file = 'other/samples/report_wrong_syntax.xml'
            file = 'other/samples/profiling_report_nuke13.xml'

            path = os.getenv('PWD')
            status = XmlData.load_file(os.path.join(path, file), self)

        func(self)

        if status:
            self._show_inspector()

    return inner_wrapper
