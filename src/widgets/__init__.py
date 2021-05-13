# coding: utf-8
from __future__ import print_function

try:
    from .lower_buttons import ButtonSection
    from .search import SearchBarWidget
    from .profiling import ProfilingWidget
    from .rename import RenameDialogBox, parse_user_variables
    from .settings import SettingsWidget
    from .xml_inspector import XmlInspector
except Exception as error:
    print('WIDGET PACKAGE: %s' % error)
