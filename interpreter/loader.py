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

def load_file(filename):
    # Splitting results in removal of delim. Have to rebuild
    dirname = ''.join(['/' + token for token in filename.split('/')[1:-1]])

    prep_list = []
    prep_title = ''
    with open(filename, 'r') as f:
        for line in f:
            line2 = line.strip('\n')
            if prep_title and line:
                faux_title = check_prep(line2)
                if not faux_title:
                    prep_hash[len(prep_hash)-1][prep_title] += line
                elif faux_title:
                    prep_title = faux_title
                    prep_hash.append({prep_title: ""})

            elif line:
                prep_title = check_prep(line2)
                if prep_title:
                    prep_hash.append({prep_title: ""})

    return prep_list
