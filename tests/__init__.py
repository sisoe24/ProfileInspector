"""
The only way I found to test the app outside Nuke is by adding the parent of root to sys.path.
This is because the menu.py has access only to the first level of packages (root).

At least I am only adding to path when testing locally and not when Nuke is running.

Also should be noted that the app is launched in "module mode" to work:

    `python -m tests.app`

"""
from os.path import dirname, abspath
import sys

# HACK: The only way I found to safely test the app in isolate environment
root = dirname(dirname(abspath(__file__)))
parent_root = dirname(root)

sys.path.insert(0, parent_root)
