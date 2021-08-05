# coding: utf-8
from __future__ import print_function

import os


def file(path):
    return os.path.join(os.getenv('PWD'), 'other', path)


def _bypass_filedialog(func):
    def inner_wrapper(*args, **kwargs):
        self = args[0]
        view = args[1]

        func(self, view)

        if os.getenv('TEST_ENV') == '1':
            self.nuke_info.nuke_comp.setText(file('test_project.kw'))
            self.nuke_info.file_label.setText(file('profiling_test.xml'))

    return inner_wrapper
