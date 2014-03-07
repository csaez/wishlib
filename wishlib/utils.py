# The MIT License (MIT)

# Copyright (c) 2014 Cesar Saez

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from os import path
import json


class JSONDict(dict):

    def __init__(self, fp, *args, **kwds):
        super(JSONDict, self).__init__(*args, **kwds)
        self.fp = fp
        if path.exists(fp):
            with open(self.fp) as fp:
                data = json.load(fp)
            self.update(data)

    def __setitem__(self, key, value):
        super(JSONDict, self).__setitem__(key, value)
        self.__updatejson__()

    def __delitem__(self, key):
        super(JSONDict, self).__delitem__(key)
        self.__updatejson__()

    def clear(self):
        super(JSONDict, self).clear()
        self.__updatejson__()

    def update(self, other):
        super(JSONDict, self).update(other)
        self.__updatejson__()

    def __updatejson__(self):
        with open(self.fp, "w") as fp:
            json.dump(self, fp, indent=4)


def map_recursive(function, iterable):
    """
    Apply function recursively to every item or value of iterable and returns a
    new iterable object with the results.
    """
    if isiterable(iterable):
        dataOut = iterable.__class__()
        for i in iterable:
            if isinstance(dataOut, dict):
                dataOut[i] = map_recursive(function, iterable[i])
            else:
                # convert to list and append
                if not isinstance(dataOut, list):
                    dataOut = list(dataOut)
                dataOut.append(map_recursive(function, i))
        return dataOut
    return function(iterable)


def isiterable(iterable):
    if all((hasattr(iterable, "__iter__"), hasattr(iterable, "__getitem__"))):
        try:
            (_ for _ in iterable).next()
            return True
        except:
            pass
    return False
