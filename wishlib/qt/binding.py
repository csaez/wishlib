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

import sys
import imp
from types import ModuleType


class Qt(ModuleType):

    def __init__(self, *args, **kargs):
        super(Qt, self).__init__(*args, **kargs)
        self._bindings = ("PyQt4", "PySide")  # favors the first one
        for b in self._bindings:
            try:
                imp.find_module(b)
            except ImportError:
                continue
            self._active = b
            break
        if not hasattr(self, "_active"):
            raise Exception("PyQt4/PySide not found!")

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if value in self._bindings:
            self._active = value

    def __getattr__(self, attr):
        item = self.__dict__.get(attr)
        if item is None:
            top_lvl = __import__("{0}.{1}".format(self.active, attr),
                                 globals(), locals(), [], -1)
            item = getattr(top_lvl, attr)
        return item

# trick python overriding the module with an instance,
# ref is needed to avoid python gc
ref = sys.modules[__name__]
sys.modules[__name__] = Qt(__name__)
