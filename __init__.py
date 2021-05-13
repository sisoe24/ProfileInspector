# coding: utf-8
from __future__ import with_statement, print_function


def report_error(message):
    import os
    import traceback
    from datetime import datetime

    report = os.path.join(os.path.dirname(__file__), 'log/errors.log')

    with open(report, 'a') as f:
        f.write("NODEBOX: [%s] %s - %s\n " %
                (datetime.now(), traceback.format_exc(), message))


try:
    import NodeBox.src
except Exception as error:
    report_error(error)
