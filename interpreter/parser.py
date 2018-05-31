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
recipe_funs = []
func_hash = []

def len_mb(offset=0):
    return len(mixing_bowls)-offset


def file_parser(line):
    if len(line) > 0:
        if line[len(line)-1] == '.':
            if re.search('(?<=Prep)\.', line):
                return line[:-6]


def prep_parser(line):
    if re.match('Ingredients\.', line):
        return True
    return False


def ing_parser(line, cnt):
    mixing_bowl = []
    if len(line) > 0:
        tokens = line.split(' ')
        if len(tokens) == 1:
            mixing_bowl.append(gen.one_token(tokens))
        elif len(tokens) == 2:
            mixing_bowl.append(gen.two_token(tokens))
        elif len(tokens) == 3:
            mixing_bowl.append(gen.three_token(tokens))
        else:
            mixing_bowl.append(gen.multi_token(tokens))

    if cnt > 0:
        return mixing_bowl


def run_instruction(command, instruct, dirname):
    if command == "Fetch":
        return ops.fetch

    command_list = {
        "Add": ops.add,
        "Remove": ops.sub,
        "Combine": ops.multi,
        "Divide": ops.div,
        "Taste": ops.prnt,
    }

    return command_list[command](instruct, mixing_bowls)


def exec_parser(line, cnt, dirname):
    if len(line) > 0:
        sanitized_line = line.replace('. ', '.')
        instructions = sanitized_line.split('.')
 
        # Split causes extra blank to be added -> Remove it
        del instructions[-1]

        for instruct in instructions:
            command = instruct.split(' ')[0]
            if command == "Prep":
                bowl_pile = parse_func(instruct[5:-1])
                if len(mixing_bowls) > 1:
                    temp_bowl = {}
                    for bowl in mixing_bowls:
                        temp_bowl.update(bowl)
                    bowl_pile = [temp_bowl]
                mixing_bowls[0] = bowl_pile[0]
            else:
                mixing_bowls = run_instruction(command,
                    instruct, dirname)
        return True

    if cnt > 0:
        return False


def parse_func(func_name):

    EXECFLAG = False
    INGFLAG = False
    cnt = 0

    mixing_bowls = [] 

    for line in func_hash[func_name].split('\n'): 
        if mixing_bowls and line:
            mixing_bowls = exec_parser(line, cnt, dirname, mixing_bowls)
            cnt += 1
        elif INGFLAG and line:
            mixing_bowl = ing_parser(line, cnt)
            cnt += 1
            if mixing_bowl:
                mixing_bowls.append(mixing_bowl)
                INGFLAG = False
                cnt = 0
        elif line:
            INGFLAG = prep_parser(line)

    return mixing_bowls


def main(filename=None):
    if not filename:
        parser = argparse.ArgumentParser()
        parser.add_argument("filename")
        args = parser.parse_args()
        filename = args.filename

    # Splitting results in removal of delim. Have to rebuild
    dirname = ''.join(['/' + token for token in filename.split('/')[1:-1]]) 

    prep_title = ''
    with open(filename, 'r') as f:
        for line in f:
            line2 = line.strip('\n')
            if prep_title and line:
                faux_title = file_parser(line2)
                if not faux_title:
                    func_hash[len(func_hash)-1][prep_title] += line
                elif faux_title:
                    prep_title = faux_title
                    func_hash[len(func_hash)] = {prep_title: ""}

            if line:
                prep_title = file_parser(line2)
                if prep_title:
                    func_hash[len(func_hash)] = {prep_title: ""}

    return prep_func([*func_hash[0][0]])

main()
