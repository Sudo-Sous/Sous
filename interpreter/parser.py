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

func_hash = []


def check_prep(line):
    """Checks if prep block has been reached.

    return --- Prep title or None
    """
    if len(line) > 0:
        if line[len(line)-1] == '.':
            if re.search('(?<=Prep)\.', line):
                return line[:-6]


def check_ing(line):
    """Checks if ingredient block has been reached."""

    if re.match('Ingredients\.', line):
        return True
    return False


def ing_parser(line):
    """Initial processing of variable (ingredient).

    return -- dict as {var_name: var_val} or None
    """

    if len(line) > 0:
        tokens = line.split(' ')
        if len(tokens) == 1:
            return gen.one_token(tokens)
        elif len(tokens) == 2:
            return gen.two_token(tokens)
        elif len(tokens) == 3:
            return gen.three_token(tokens)
        else:
            return gen.multi_token(tokens)


def fetch(instruct, dirname="."):
    """Imports preps from other files.

    The parser is being run from a directory different
    than the actual code it is interpreting. Therefore,
    it must step into directory of the file being parsed,
    and from there using relative paths to find the file
    which is desired to be imported.

    No return value is needed as the global func_hash
    variable is directly modified by the driver function.
    """

    import os
    root = None
    name = None
    ret_dir = None
    func_ret = None

    if os.getcwd() != dirname:
       ret_dir = os.getcwd()
       os.chdir(dirname)

    if re.search('from the counter', instruct):
        root = '..'
        name = instruct[10:-17]+".sf"
        name = name.replace(' ', '_')
    elif re.search('from the pantry', instruct):
        root = './pantry'                                           
        name = instruct[10:-12]+".sf"
        name = name.replace(' ', '_')
    elif re.match('Fetch the ([^.=*&1-9A-Z]+)', instruct):
        root = '.'
        name = instruct[10:]+".sf"
        name = name.replace(' ', '_')

    if root and name:
        for root, dirs, files in os.walk(root):
            for filename in files:
                if filename.split('/')[-1] == name:
                    driver(filename)
    # TODO: else throw error

    # Return to the directory of the parser
    if ret_dir:
        os.chdir(ret_dir)


def run_instruction(command, instruct, dirname, mixing_bowls):
    if command == "Fetch":
        fetch(instruct, dirname)
    elif command == "Prep":
        bowl_pile = parse_func(instruct[5:], dirname)
        if len(mixing_bowls) > 1:
            temp_bowl = {}
            for bowl in mixing_bowls:
                temp_bowl.update(bowl)
            bowl_pile = [temp_bowl]
        # This is temp only until add bowls is impl
        return mixing_bowls[0].append(bowl_pile[0][0])
    else:
        command_list = {
            "Add": ops.add,
            "Remove": ops.sub,
            "Combine": ops.multi,
            "Divide": ops.div,
            "Taste": ops.prnt,
        }

        return command_list[command](instruct, mixing_bowls)


def exec_parser(line, dirname, mixing_bowls):
    if len(line) > 0:
        sanitized_line = line.replace('. ', '.')
        instructions = sanitized_line.split('.')
 
        # Split causes extra blank to be added -> Remove it
        del instructions[-1]

        for instruct in instructions:
            command = instruct.split(' ')[0]
            ret_val = run_instruction(command,
                instruct, dirname, mixing_bowls)
            if ret_val:
                mixing_bowls = ret_val
        return mixing_bowls    
    return mixing_bowls


def parse_func(func_name, dirname):
    INGFLAG = False

    found = False
    func_line = ""
    mixing_bowls = [[]]
    for x in range(0, len(func_hash)):
        if [*func_hash[x]][0] == func_name:
            func_line = func_hash[x][func_name]
            if func_line:
                found = True
                cnt = 0
                for line in func_line.split('\n'):
                    if INGFLAG and line:
                        ing = ing_parser(line)
                        if ing:
                            mixing_bowls[0].append(ing)
                        else:
                            INGFLAG = False
                    elif cnt == 2:
                        mix = exec_parser(line, dirname, mixing_bowls)
                        if mix:
                            mixing_bowls = mix
                    elif not INGFLAG and cnt <= 1 and line:
                        INGFLAG = check_ing(line)
                    else:
                        if cnt == 1:
                            INGFLAG = False
                        cnt += 1
    # if not found:
    #     raise MethodNotFoundException()
    return mixing_bowls


def driver(filename_fetch=None):
    if not filename_fetch:
        parser = argparse.ArgumentParser()
        parser.add_argument("filename")
        args = parser.parse_args()
        filename = args.filename
    else:
        filename = filename_fetch

    # Splitting results in removal of delim. Have to rebuild
    dirname = ''.join(['/' + token for token in filename.split('/')[1:-1]]) 

    prep_title = ''
    with open(filename, 'r') as f:
        for line in f:
            line2 = line.strip('\n')
            if prep_title and line:
                faux_title = check_prep(line2)
                if not faux_title:
                    func_hash[len(func_hash)-1][prep_title] += line
                elif faux_title:
                    prep_title = faux_title
                    func_hash.append({prep_title: ""})

            elif line:
                prep_title = check_prep(line2)
                if prep_title:
                    func_hash.append({prep_title: ""})

    if not filename_fetch:
        mixing_bowls = parse_func([*func_hash[0]][0], dirname)
        ret_bowls = []
        for bowls in mixing_bowls:
            for ing in bowls:
                ret_bowls.append(ing)
        return ret_bowls 

driver()
