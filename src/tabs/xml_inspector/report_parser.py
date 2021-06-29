# coding: utf-8
from __future__ import print_function

import os
import re
import logging
import xml.etree.ElementTree as ET


LOGGER = logging.getLogger('ProfileInspector.xml_data')


def _check_closing_tags(file):
    # XXX: file might have some unclosed tags usually Frame and PerformanceProfile
    # TODO: could try to auto fix it?

    err_msg = None

    with open(file, 'r') as f:

        lines = f.readlines()
        lines_copy = list(lines)

        match_tag = re.compile(r'<[^\/]+?>')

        for line_num, line in enumerate(lines, 1):
            no_match = True
            open_tag = 0

            # skip first 2 lines of the header
            if re.search(r'^<\?xml', line):
                lines_copy.pop(0)
                continue

            tag = match_tag.search(line)
            if tag:
                tag = tag.group()

                # print("➡ Matching tag %s line: %s" % (tag, line_num))

                for subline in lines_copy:

                    sub_tag = match_tag.search(subline)
                    if sub_tag:
                        if sub_tag.group() == tag:
                            open_tag += 1

                    closing_tag = tag.replace('<', '</')
                    re_match = re.search(closing_tag, subline)
                    if re_match:
                        # print('Found closing tag %s line: %s' % (tag, line_num))
                        no_match = False
                        break

                if no_match or open_tag == 2:
                    err_msg = 'Tag %s has no enclosing tag: line %s.' % (
                        tag, line_num)
                    LOGGER.error(err_msg)
                    break

            lines_copy.pop(0)

    return err_msg


class XmlData:

    _xml = ""
    _file = ""
    _nodes = {}

    @ classmethod
    def load_file(cls, file, parent):
        error_status = ""
        try:
            xml = ET.parse(file).getroot()
            LOGGER.debug('Try parsing xml file...')

        except ET.ParseError as err:
            LOGGER.error('XML Parsing error: %s', err)

            err_msg = _check_closing_tags(file)

            if err_msg:
                err_msg += '\n' + str(err)

            error_status = err_msg

        else:
            if xml.tag != 'PerformanceProfile':
                error_status = 'Not a valid Nuke PerformanceProfile xml file'
                LOGGER.error('File doesnt seem to be a valid nuke xml file')
            else:
                cls._file = file
                cls._xml = xml
                LOGGER.debug('XML file valid: %s', file)

        if error_status:
            raise ValueError(error_status)

        return True

    def file_name(self):
        return os.path.basename(self._file)

    @ property
    def root(self):
        return self._xml

    def num_threads(self):
        return self.root.findtext('NumThreads')

    def script_name(self):
        return self.root.findtext('ScriptName')

    def time_stored(self):
        return self.root.findtext('TimeStored')

    def machine_info(self):
        # TODO: looks like xml data has stored a string "b'text'"
        return self.root.findtext('MachineInfo/OS')

    def frames_element(self):
        return self.root.findall('Frame')

    def frame_count(self):
        return len(self.frames_element())

    def nodes_elements(self):
        first_frame = self.root.find('Frame')
        return first_frame.findall('Node')

    def node_count(self):
        return len(self.nodes_elements())

    def nodes_name(self):
        names = []
        for index, name in enumerate(self.nodes_elements()):
            name = name.findtext('Name')

            self._nodes[index] = name

            max_chars = 15
            if len(name) >= max_chars:

                name = name[:max_chars] + '...'

            names.append(name)

        return names

    def nodes_class(self):
        return [n.findtext('Class') for n in self.nodes_elements()]

    def node_class(self, node_name):
        node_name = node_name.replace('...', '')
        for node in self.nodes_elements():
            if node.findtext('Name').startswith(node_name):
                return node.findtext('Class')
