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

from .binding import QtGui, QtCore
from .helpers import set_style


class QWidget(QtGui.QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        # styling
        set_style(self, True)
        # garbage collection
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class QMenu(QtGui.QMenu):

    def __init__(self, *args, **kwds):
        super(QMenu, self).__init__(*args, **kwds)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        set_style(self, False)


class QDialog(QtGui.QDialog):

    def __init__(self, *args, **kwds):
        super(QDialog, self).__init__(*args, **kwds)
        # dialog defaults
        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.WindowMinimizeButtonHint)
        # styling
        set_style(self, True)
        # garbage collection
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class QMainWindow(QtGui.QMainWindow):

    def __init__(self, *args, **kwds):
        super(QMainWindow, self).__init__(*args, **kwds)
        # styling
        set_style(self, True)
        # garbage collection
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
