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


def check_prep(line):
    """Checks if prep block has been reached.

    return --- Prep title or None
    """
    if len(line) > 0:
        if line[len(line)-1] == '.':
            if re.search('(?<=Prep)\.', line):
                return line[:-6]


def load_file(filename, dirname):
    prep_list = []
    prep_title = ''
    with open(filename, 'r') as f:
        for line in f:
            line2 = line.strip('\n')
            if prep_title and line:
                faux_title = check_prep(line2)
                if not faux_title:
                    prep_list[len(prep_list)-1][prep_title] += line
                elif faux_title:
                    prep_title = faux_title
                    prep_list.append({prep_title: ""})

            elif line:
                prep_title = check_prep(line2)
                if prep_title:
                    prep_list.append({prep_title: ""})

    return prep_list
