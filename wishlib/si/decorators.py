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

from __future__ import absolute_import

from functools import wraps
from .shortcuts import si
from .utils import siget


def no_inspect(function):
    @wraps(function)
    def decorated(*args, **kwds):
        # backup old autoinspect
        param = siget("preferences.Interaction.autoinspect")
        old_value = param.Value
        # set autoinspect off
        param.Value = False
        # execute decorated function
        f = function(*args, **kwds)
        # retore autoinspect
        param.Value = old_value
        return f
    return decorated


def one_undo(function):
    @wraps(function)
    def decorated(*args, **kwds):
        try:
            si.BeginUndo()
            f = function(*args, **kwds)
        finally:
            si.EndUndo()
            return f
    return decorated


def OverrideWin32Controls(function):
    @wraps(function)
    def decorated(*args, **kwds):
        si.Desktop.SuspendWin32ControlsHook()
        f = function(*args, **kwds)
        si.Desktop.RestoreWin32ControlsHook()
        return f
    return decorated
