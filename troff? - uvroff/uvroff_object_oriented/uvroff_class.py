#!/usr/bin/env python3

import sys


class ArgumentError(Exception):
    pass

class FTOptionError(Exception):
    pass

class NegativeOptionArgumentError(Exception):
    pass


class UVroff:

    def __init__(self, filename, str_list):
        self.filename = filename
        self.str_list = str_list

        self.lw = 0
        self.lm = 0
        self.ft = 0
        self.ls = 0

        self.f = None
        self.nth_line = 0

        self.inter_line_list = []
        self.current_len = 0

        self.output_list = []

    def get_lines(self):
        self.__work_controller()
        return self.output_list

    def __arg_handler(self):
        condition_1 = (self.filename is None and self.str_list is None)
        condition_2 = (self.filename is not None and self.str_list is not None)
        if condition_1 or condition_2:
            raise ArgumentError("Two arguments were both None or both non-None, expect one and only one None argument")
        elif self.filename == "stdin":
            self.f = sys.stdin
        elif self.filename is not None:
            try:
                self.f = open(self.filename)
            except FileNotFoundError as e:
                print(e, file=sys.stderr)
                sys.exit(-1)
        else:
            self.f = self.str_list

    def __work_controller(self):

        self.__arg_handler()

        last_line = None
        for line in self.f:
            self.nth_line += 1
            if line == '\n' or line == '':
                # Control flow -- 1: case '\n'
                if last_line != '\n' and self.ft != 0 and self.inter_line_list != [' ' * (self.lm - 1)]\
                        and self.inter_line_list != []:
                    # .FT is not off
                    try:
                        self.output_list.append(' '.join(self.inter_line_list))
                        for i in range(self.ls):
                            self.output_list.append('')
                    except NameError:
                        pass

                self.output_list.append('')
                for i in range(self.ls):
                    self.output_list.append('')
                self.inter_line_list = [' ' * (self.lm - 1)] if self.lm != 0 else []
                self.current_len = self.lm - 1 if self.lm != 0 else 0

                last_line = '\n'
                continue

            last_line = None

            words = line.split()
            w = words[0]
            if w == '.LW' or w == '.LM' or w == '.FT' or w == '.LS': # need to check for testing ".LM 10 24", INVALID OPTION but not checked
                # Control flow -- 2: case options
                last_lm = self.lm
                try:
                    self.__parse_option(words)
                except ValueError:
                    print("At {} of the text file, .LW or .LS or .LM has invalid argument".format(self.nth_line), file=sys.stderr)
                    sys.exit(-1)
                except FTOptionError as e:
                    print(e, file=sys.stderr)
                    sys.exit(-1)
                except NegativeOptionArgumentError as e:
                    print(e, file=sys.stderr)
                    sys.exit(-1)
                try:
                    if self.inter_line_list != [' ' * (last_lm - 1)] and self.inter_line_list != []:
                        self.output_list.append(' '.join(self.inter_line_list))
                except NameError:
                    pass
                self.inter_line_list = [' ' * (self.lm - 1)] if self.lm != 0 else []
                self.current_len = self.lm - 1 if self.lm != 0 else 0

            elif self.ft == 0:
                # Control flow -- 3: just printing, case formatting off
                self.output_list.append(line.strip('\n'))

            else:
                # Control flow -- 4: format a line then print it
                self.__put_a_line(words)

        # finish a left_over_line
        try:
            if len(self.inter_line_list) != 0 and line != '\n':
                self.output_list.append(' '.join(self.inter_line_list))
        except NameError:
            pass

    def __parse_option(self, words):
        if words[0] == '.LW':
            self.lw = int(words[1])
            self.ft = 1
            if self.lw < 0:
                raise NegativeOptionArgumentError("At line {} of the text file, .LW or .LS option has negative argument".format(self.nth_line))
        elif words[0] == '.LM':
            if words[1][0] == '-' or words[1][0] == '+':
                self.lm += int(words[1])
            else:
                self.lm = int(words[1])

            if self.lm > self.lw - 20:
                self.lm = self.lw - 20
            if self.lm < 0:
                self.lm = 0
        elif words[0] == '.FT':
            if words[1] == 'on':
                self.ft = 1
            elif words[1] == 'off':
                self.ft = 0
            else:
                raise FTOptionError("At line {} of the text file, .FT option  has invalid argument".format(self.nth_line))
        else:
            # words[0] == '.LS'
            self.ls = int(words[1])
            if self.ls < 0:
                raise NegativeOptionArgumentError("At line {} of the text file, .LW or .LS option has negative argument".format(self.nth_line))

    def __put_a_line(self, words):
        for word in words:
            if len(self.inter_line_list) == 0:
                self.inter_line_list.append(word)
                self.current_len += len(word) + 1 if self.lm != 0 else len(word)
                continue
            if self.current_len + len(word) + 1 <= self.lw:
                self.inter_line_list.append(word)
                self.current_len = self.current_len + len(word) + 1
            else:
                self.output_list.append(' '.join(self.inter_line_list))
                for i in range(self.ls):
                    self.output_list.append('')
                self.inter_line_list = [' ' * (self.lm - 1)] if self.lm != 0 else []
                self.current_len = self.lm - 1 if self.lm != 0 else 0
                self.current_len += len(word) + 1 if self.lm != 0 else len(word)
                self.inter_line_list.append(word)
