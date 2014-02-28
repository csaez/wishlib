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

initialized = False
active = None
bindings = ["PySide", "PyQt4"]  # favors the first one
tokens = {"pyside": bindings[0], "pyqt": bindings[1], "pyqt4": bindings[1]}
qt_modules = ("QtCore", "QtDeclarative", "QtGui", "QtHelp", "QtNetwork",
              "QtOpenGL", "QtScript", "QtScriptTools", "QtSql", "QtSvg",
              "QtWebKit", "QtXml", "phonon")
for x in qt_modules:
    globals()[x] = None


def init(favor=None):
    global active, initialized

    # get active binding
    b = _get_binding()
    t = tokens.get(favor.lower()) if favor else None
    active = t if t is not None and t in b else b[0]

    # qt import
    for x in qt_modules:
        tp_lvl = __import__(active + "." + x, globals(), locals(), [], -1)
        globals()[x] = getattr(tp_lvl, x)
    main_mod = __import__(active, globals(), locals(), [], -1)

    # local imports
    from .helpers import set_style, set_icon, loadUi, wrapinstance
    from . import decorators

    # re-route modules
    initialized = True
    for scope in (globals(), locals()):
        for k, v in scope.iteritems():
            if not k.startswith("_"):
                setattr(main_mod, k, v)  # monkey patch globals
    main_mod.init = lambda x: x  # placeholder for re-init
    sys.modules[__name__] = main_mod


def _get_binding():
    # cleanup
    for i, b in enumerate(bindings):
        try:
            imp.find_module(b)
        except ImportError:
            bindings.pop(i)
    if not len(bindings):
        raise Exception("Couldn't import PySide or PyQt4!")
    return bindings

# auto init
if len(_get_binding()) == 1:
    init()
