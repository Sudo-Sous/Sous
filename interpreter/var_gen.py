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

DRY = ("g", "kg", "pinch", "pinches")

LIQUID = ("ml", "l", "dash", "dashes")

EITHEROR = ("tablespoon", "tablespoons", "cup", "cups", "teaspoon", "teaspoons")

DRYFLAG = ("heaping", "level")

def convert_to_int(token)
    try:
        return int(token)
    except ValueError:
        pass

def set_dry_val(tokens):
    token_val = convert_to_int(tokens[0])
    if token_val:
        return {tokens[1]: token_val}
    else:
        raise ValueError

def set_liquid_val(tokens):
    token_val = convert_to_int(tokens[0])
    if token_val:
        return {tokens[1]: tokens[0]}
    else:
        raise ValueError

def gen_var_name(tokens):
    var_name = ""
    for token in tokens:
        if len(var_name) > 0:
            var_name += " {}".format(token)
         else:
            var_name += token
    return var_name

def one_token(tokens):
    return {tokens[0]: None}

def two_token(tokens):
    token_val = convert_to_int(tokens[0])
    if token_val:
        return {tokens[1]: tokens[0]}
    else:
        return {"{0} {1}".format(tokens[1], tokens[0]): None}

def three_token(tokens):
    if tokens[1] in DRY:
        del tokens[1]
        return set_dry_val(tokens)
    elif tokens[1] in LIQUID:
        del tokens[1]
        return set_liquid_val(tokens)
    elif tokens[1] in EITHEROR:
        del tokens[1]
        if tokens[1] in DRYFLAG:
            return set_dry_val(tokens)
        else:
            return set_liquid_val(tokens)
    else:
        token_val = convert_to_int(tokens[0])
        if token_val:
            return {gen_var_name(tokens[1:]): tokens[0]}
        else:
            return {gen_var_name(tokens): None}

def multi_token(tokens):
    if tokens[1] in DRY:
       del tokens[1]
       return set_dry_val([tokens[0], gen_var_name(tokens[1:])])
    elif tokens[1] in LIQUID:
       del tokens[1]
       return set_dry_val([tokens[0], gen_var_name(tokens[1:])])
    elif tokens[1] in EITHEROR:
       del tokens[1]
       return set_dry_val([tokens[0], gen_var_name(tokens[1:])])
