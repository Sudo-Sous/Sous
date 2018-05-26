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

var_dict = {}

def file_parser(line):
    if len(line) > 2:
        if line[len(line)-2] == '.':
            if re.search('(?<=Prep)\.', line):
                return True
    return False

def prep_parser(line):
    if re.match('Ingredients.', line):
        return True
    return False

def convert_to_int(token)
    try:
        return int(token)
    except ValueError:
        pass 

def ing_parser(line):
    tokens = line.split(' ')
    if len(tokens) == 1:
        var_dict[tokens[0]] = None
    else len(tokens) == 2:
       token_val = convert_to_int(tokens[0])
       if token_val:
           var_dict[tokens[1] = tokens[0]
       else:
           var_dict["{0} {1}"] = None

def exec_parser(line):
    pass 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    PREPFLAG = False
    EXECFLAG = False
    with open(args.filename, 'r') as f:
        for line in f:
            if EXECFLAG and line:
                exec_parser(line)
            elif INGFLAG and line:
                EXECFLAG = ing_parser(line)
            elif PREPFLAG and line:
                INGFLAG = prep_parser(line)
            elif line:
                PREPFLAG = file_parser(line)

main()
