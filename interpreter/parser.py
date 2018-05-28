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

var_dict = {}

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
            var_dict.udpate(gen.one_token(tokens))
        elif len(tokens) == 2:
            var_dict.update(gen.two_token(tokens))
        elif len(tokens) == 3:
            var_dict.update(gen.three_token(tokens))
        else:
            var_dict.update(gen.multi_token(tokens))
        return False

    if cnt > 0:
        return True

def exec_parser(line):
    pass 

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
                exec_parser(line2)
            elif INGFLAG and line:
                EXECFLAG = ing_parser(line2, cnt)
                cnt += 1 
            elif PREPFLAG and line:
                INGFLAG = prep_parser(line2)
            elif line:
                PREPFLAG = file_parser(line2)

main()
