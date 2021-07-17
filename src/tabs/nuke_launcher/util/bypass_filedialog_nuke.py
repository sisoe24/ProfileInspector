# coding: utf-8
from __future__ import print_function

import os


def file(path):
    return os.path.join(os.getenv('PWD'), path)


def _bypass_filedialog(func):
    def inner_wrapper(*args, **kwargs):
        self = args[0]
        view = args[1]

        func(self, view)

        if not os.getenv('_TEST_ENV') == '1':
            return

        self.nuke_info.nuke_comp.setText(file('other/test_project.kw'))
        self.nuke_info.file_label.setText(file('other/profiling_test.xml'))
        self.launch_app.setEnabled(True)

    return inner_wrapper
