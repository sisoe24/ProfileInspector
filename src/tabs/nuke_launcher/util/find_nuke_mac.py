import os
import plistlib

import logging


LOGGER = logging.getLogger('ProfileInspector.mac_nuke')


def mac_nuke_exec(nuke_path):
    """Get MacOS nuke executable file inside package.app"""

    def parse_plist(nuke_path):
        """Parse the plist file"""
        # TODO: redudant os path join
        plist_file = os.path.join(nuke_path, 'Contents/Info.plist')

        if os.path.exists(plist_file):

            LOGGER.debug('Found Nuke.app plist')

            exec_file = plistlib.readPlist(plist_file)['CFBundleExecutable']
            file_path = os.path.join(nuke_path, 'Contents/MacOS', exec_file)

            return file_path

        LOGGER.warning(
            'Nuke plist could be open or found: fallback on parsing files')
        raise IOError

    def parse_files(nuke_path):

        app = os.path.basename(nuke_path)
        search_path = os.path.join(nuke_path, 'Contents/MacOS')

        for file in os.listdir(search_path):
            if app.startswith(file):
                file_path = os.path.join(search_path, file)
                if os.access(file_path, os.X_OK) and os.path.isfile(file_path):
                    LOGGER.debug('Found Nuke.app executable: %s', file)
                    return file_path

        LOGGER.error("Couldn't find a valid nuke executable")
        return None

    try:
        nuke_exec = parse_plist(nuke_path)
    except IOError:
        nuke_exec = parse_files(nuke_path)

    return nuke_exec
