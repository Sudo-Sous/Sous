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

import loader
import var_gen as gen
import sous_ops as ops

prep_list = []


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


def prep(instruct, dirname):
    """Run instructions within the prep"""

    bowl_pile = parse_prep(instruct, dirname)
    if len(mixing_bowls) > 1:
        temp_bowl = {}
        for bowl in mixing_bowls:
            temp_bowl.update(bowl)
        bowl_pile = [temp_bowl]
    # This is temp only until add bowls is impl
    return mixing_bowls[0].append(bowl_pile[0][0])


def run_instruction(command, instruct, dirname, mixing_bowls):
    """Gets instruction arguments where they need to go

    return -- a mixing bowl with new args or None
    """
    if command == "Fetch":
        prep_list.append(ops.fetch(instruct, dirname))
    elif command == "Prep":
        return prep(instruct[5:], dirname)
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
    """Iterate over the prep instructions

    From there, send them off to the run_instruction func
    to be executed. If run_instruction returns anything,
    it is an updated mixing_bowl and therefore should replace
    the old one.
    """

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


def parse_prep(prep_name, dirname):
    """Parse the prep

    Loops over the lines within the prep
    and either adds the to the mixing bowl (ingredients)
    or executes them (instructions)

    return -- mixing_bowls double array w/ internal dicts
    """
    INGFLAG = False
    mixing_bowls = [[]]

    # Search through the prep_hash and find the
    # proper prep contents.
    for x in range(0, len(prep_hash)):
        if [*prep_hash[x]][0] == prep_name:
            prep_lines = prep_hash[x][prep_name]

    if prep_lines:
        # cnt keeps track of the number of new lines
        # between the ingredient list and instructions.
        cnt = 0

        for line in prep_lines.split('\n'):
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
    # else:
    #     raise MethodNotFoundException()
    return mixing_bowls


def driver(filename_fetch=None):
    """ Main driver function

    Loads all preps within the file into the prep_hash.
    If filename_fetch is set, then their is nothing more
    to do. Otherwise, execute the first prep within the file.
    The first prep is always treated as the "main" function. 

    filename_fetch: absolute filepath or None

    return -- list of ingredients or None 
    """
    if not filename_fetch:
        parser = argparse.ArgumentParser()
        parser.add_argument("filename")
        args = parser.parse_args()
        filename = args.filename
    else:
        filename = filename_fetch

    prep_list = loader.load_file(filename)

    if not filename_fetch:
        parse_prep([*prep_hash[0]][0], dirname)

driver()
