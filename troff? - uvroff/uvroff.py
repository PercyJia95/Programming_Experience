#!/usr/bin/env python3

import sys
import fileinput


def main():
    # if len(sys.argv) == 1:
    #     print("Sorry, uvroff has given no argument")
    # elif len(sys.argv) > 2:
    #     print("uvroff only permits one argument")
    # else:
    #     print("First argument is", sys.argv[1])

    lw = 0
    lm = 0
    ft = 0
    ls = 0
    last_line = None

    try:
        f = fileinput.input()
    except IOError:
        sys.exit("file is not opened successfully")
    else:
        for line in f:
            if line == '\n':
                if last_line != '\n' and ft != 0 and inter_line_list != [' '* (lm -1)] and inter_line_list != []:
                    # .FT is not off
                    try:
                        print(' '.join(inter_line_list))
                        for i in range(ls):
                            print()
                    except NameError:
                        pass

                print()
                for i in range(ls):
                    print()
                inter_line_list = [' ' * (lm - 1)] if lm != 0 else []
                current_len = lm - 1 if lm != 0 else 0

                last_line = '\n'
                continue

            last_line = None

            words = line.split()
            w = words[0]
            if w == '.LW' or w == '.LM' or w == '.FT' or w == '.LS':
                last_lm = lm
                lw, lm, ft, ls = parse_option(words, lw, lm, ft, ls)

                try:
                    if inter_line_list != [' '* (last_lm -1)] and inter_line_list != []:
                        print(' '.join(inter_line_list))
                except NameError:
                    pass

                inter_line_list = [' ' * (lm - 1)] if lm != 0 else []
                current_len = lm - 1 if lm != 0 else 0
            elif ft == 0:
                print(line, end='')
            else:
                inter_line_list, current_len = put_a_line(words, lw, lm, ls, inter_line_list, current_len)

        # finish a left_over_line
        try:
            if len(inter_line_list) != 0 and line != '\n':
                print(' '.join(inter_line_list))
        except NameError:
            pass


def put_a_line(words, lw, lm, ls, inter_line_list, current_len):
    for word in words:
        if len(inter_line_list) == 0:
            inter_line_list.append(word)
            current_len += len(word) + 1 if lm != 0 else len(word)
            continue
        if current_len + len(word) + 1 <= lw:
            inter_line_list.append(word)
            current_len = current_len + len(word) + 1
        else:
            print(' '.join(inter_line_list))
            for i in range(ls):
                print()
            inter_line_list = [' ' * (lm - 1)] if lm != 0 else []
            current_len = lm - 1 if lm != 0 else 0
            current_len += len(word) + 1 if lm != 0 else len(word)
            inter_line_list.append(word)

    return inter_line_list, current_len


def parse_option(words, lw, lm, ft, ls):
    if words[0] == '.LW':
        lw = int(words[1])
        ft = 1
    elif words[0] == '.LM':
        if words[1][0] == '-' or words[1][0] == '+':
            lm += int(words[1])
        else:
            lm = int(words[1])

        if lm > lw - 20:
            lm = lw - 20
        if lm < 0:
            lm = 0
    elif words[0] == '.FT':
        if words[1] == 'on':
            ft = 1
        elif words[1] == 'off':
            ft = 0
        else:
            sys.exit("Misuse of .FT at somewhere")
    else:
        # words[0] == '.LS'
        ls = int(words[1])

    return lw, lm, ft, ls


if __name__ == "__main__":
    main()
