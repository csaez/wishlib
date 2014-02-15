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
from types import ModuleType
from importlib import import_module

try:
    import PySide  # init pyside, otherwise relative imports will fail
except:
    pass


class Qt(ModuleType):

    def __init__(self, *args, **kargs):
        super(Qt, self).__init__(*args, **kargs)
        self.bindings = ("PySide", "PyQt4")  # favors the first one

    @property
    def active(self):
        if hasattr(self, "_active"):
            return self._active
        for b in self.bindings:
            try:
                import_module(b)
                self.active = b
                return self._active
            except Exception as err:
                print err
        raise Exception("PyQt4/PySide not found!")

    @active.setter
    def active(self, value):
        if value in self.bindings:
            self._active = value

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return import_module("{0}.{1}".format(self.active, attr))
        return self.__dict__.get(attr)

# trick python overriding the module cache with the instance itself,
# this way 'magic methods' and properties works at a module level
ref = sys.modules[__name__]
sys.modules[__name__] = Qt(__name__)
