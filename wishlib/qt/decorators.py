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

from functools import wraps

from .QtGui import QProgressDialog
from ..si import C, log, sianchor


def progressbar(label="Work in progress...", anchor=None):
    def _wrapped(function):
        @wraps(function)
        def _decorated(*args, **kwds):
            pb = QProgressDialog(anchor or sianchor(), label)
            pb.setMinimum(0)
            pb.setMaximum(0)  # indeterminated
            pb.show()
            try:
                f = function(*args, **kwds)
            except Exception as err:
                log(err, C.siError)
                f = None
            finally:
                pb.close()
            return f
        return _decorated
    return _wrapped


def bussy(function):
    @wraps(function)
    def _decorated(*args, **kwds):
        ui = args[0]
        # disable window
        ui.setEnabled(False)
        ui.repaint()
        try:
            f = function(*args, **kwds)
        except Exception as err:
            log(err, C.siError)
            f = None  # workaround UnboundLocalError
        finally:
            # cleanup
            ui.setEnabled(True)
            return f
    return _decorated
