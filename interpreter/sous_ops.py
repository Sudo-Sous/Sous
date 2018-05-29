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

import re

def get_top_elem(mixing_bowls, index):
    return [*mixing_bowls[index][len(mixing_bowls)]][0] 


def get_ing_val(mixing_bowls, token):
    for bowl in mixing_bowls:
        for ing in bowl:
            if ing.get(token):
                return ing[token]


def op_setup(mixing_bowls, index, ing):
    key = get_top_elem(mixing_bowls, index)
    return (key, get_ing_val(mixing_bowls, ing))


def add(instruct, mixing_bowls):
    result = re.match('Add ([a-z]+) to the ([0-9])(th|st|nd|rd) mixing bowl',
                      instruct)
    index = int(result.group(2)) - 1
    ing = result.group(1)

    key, val = op_setup(mixing_bowls, index, ing)

    # Strings support addition
    mixing_bowls[index][len(mixing_bowls)][key] += val
    return mixing_bowls


def sub(instruct, mixing_bowls):
    result = re.match('Remove ([a-z]+) from the ([0-9])(th|st|nd|rd) mixing bowl',
                      instruct)
    index = int(result.group(2)) - 1
    ing = result.group(1)

    key, val = op_setup(mixing_bowls, index, ing)
    mixing_bowls[index][key] -= int(val)
    return mixing_bowls


def multi(instruct, mixing_bowls):
    result = re.match('Combine ([a-z]+) into the ([0-9])(th|st|nd|rd) mixing bowl',
                      instruct)
    index = int(result.group(2)) - 1
    ing = result.group(1)

    # Stings support multiplcation 
    key, val = op_setup(mixing_bowls, index, ing)
    mixing_bowls[index][key] *= val
    return mixing_bowls


def div(instruct, mixing_bowls):
    result = re.match('Divide ([a-z]+) into the ([0-9])(th|st|nd|rd) mixing bowl',
                      instruct)                                     
    index = int(result.group(2)) - 1
    ing = result.group(1)

    key, val = op_setup(mixing_bowls, index, ing)
    mixing_bowls[index][key] /= int(val)
    return mixing_bowls

def prnt(instruct, mixing_bowls):
    result = re.match('Taste the ([a-z]+)',
                      instruct)
    ing = result.group(1)

    print(get_ing_val(mixing_bowls, ing))


def prnt_ing():
    pass


def prnt_bowl():
    pass
