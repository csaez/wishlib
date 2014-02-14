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

import os
from PyQt4 import QtGui
file_dir = os.path.dirname(__file__)


def _setStyle(widget, force_style_factory=True):
    if force_style_factory:
        widget.setStyle(QtGui.QStyleFactory().create("plastique"))
    style_file = os.path.join(file_dir, "style",
                              "darkorange.stylesheet")
    with file(style_file) as f:
        stylesheet = f.read()
    widget.setStyleSheet(stylesheet)
    _setIcon(widget)


def _setIcon(widget):
    icon_file = os.path.join(file_dir, "images", "cs-icon.png")
    widget.setWindowIcon(QtGui.QIcon(icon_file))
