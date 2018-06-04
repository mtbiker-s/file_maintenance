#!/usr/bin/python3

import sys

class Utils:

    def get_program_name(self):
        program_name = sys.argv[0]

        return program_name

    def get_program_name_no_extension(self):

        program_name_len = len(self.get_program_name()) - 3

        program_name = self.get_program_name()[:program_name_len]

        return program_name
