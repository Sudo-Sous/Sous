# Copyright (c) 2018 Hunter Thompson 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import re

import var_gen as gen
import sous_ops as ops

mixing_bowls = [[]]

def len_mb(offset=0):
    return len(mixing_bowls)-offset


def bowl_builder(var_func, tokens):
    mixing_bowls[len_mb(1)].append(var_func(tokens))


def file_parser(line):
    if len(line) > 0:
        if line[len(line)-1] == '.':
            if re.search('(?<=Prep)\.', line):
                return True
    return False


def prep_parser(line):
    if re.match('Ingredients\.', line):
        return True
    return False


def ing_parser(line, cnt):
    if len(line) > 0:
        tokens = line.split(' ')
        if len(tokens) == 1:
            bowl_builder(gen.one_token, tokens)
        elif len(tokens) == 2:
            bowl_builder(gen.two_token, tokens) 
        elif len(tokens) == 3:
            bowl_builder(gen.three_token, tokens) 
        else:
            bowl_builder(gen.multi_token, tokens) 
        return False

    if cnt > 0:
        return True

def run_instruction(command, instruct):
    command_list = {
        "Add": ops.add,
        "Remove": ops.sub,
        "Combine": ops.multi,
        "Divide": ops.div,
        "Taste": ops.prnt
    }

    #TODO: Raise error for unknown command
    return command_list[command](instruct, mixing_bowls)

def exec_parser(line, cnt):
    if len(line) > 0:
        sanitized_line = line.replace('. ', '.')
        instructions = sanitized_line.split('.')
 
        # Split causes extra blank to be added -> Remove it
        del instructions[-1]

        for instruct in instructions:
            command = instruct.split(' ')[0]
            mixing_bowls = run_instruction(command, instruct)
        return True

    if cnt > 0:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    PREPFLAG = False
    EXECFLAG = False
    INGFLAG = False
    cnt = 0

    with open(args.filename, 'r') as f:
        for line in f:
            line2 = line.strip('\n')
            if EXECFLAG and line:
                EXECFLAG = exec_parser(line2, cnt)
                cnt += 1
            elif INGFLAG and line:
                EXECFLAG = ing_parser(line2, cnt)
                cnt += 1
                if EXECFLAG:
                    INGFLAG = False
                    cnt = 0
            elif PREPFLAG and line:
                INGFLAG = prep_parser(line2)
                if INGFLAG:
                    PREPFLAG = False
            elif line:
                PREPFLAG = file_parser(line2)

main()
