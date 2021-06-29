# coding: utf-8
from __future__ import print_function

import os


def _bypass_filedialog(func):
    def inner_wrapper(*args, **kwargs):
        self = args[0]
        view = args[1]

        func(self, view)

        if not os.getenv('_TEST_ENV') == '1':
            return

        file = os.path.join(os.getenv('PWD'), 'other/profiling_test.xml')

        self.nuke_info.file_label.setText(file)
        self.launch_app.setEnabled(True)

    return inner_wrapper
