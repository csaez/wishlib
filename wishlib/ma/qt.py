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

from wishlib.qt import init
init("pyside")
from ..qt import QtGui, QtCore, wrapinstance, set_style
import maya.OpenMayaUI as apiUI


def anchor():
    ptr = apiUI.MQtUtil.mainWindow()
    return wrapinstance(ptr, QtGui.QMainWindow)


def show_qt(qt_class, modal=False, onshow_event=None, force_style=False):
    """
    Shows and raise a pyqt window ensuring it's not duplicated
    (if it's duplicated then raise the old one).
    qt_class argument should be a class/subclass of QMainWindow, QDialog or any
    top-level widget.
    onshow_event provides a way to pass a function to execute before the window
    is showed on screen, it should be handy with modal windows.
    Returns the qt_class instance.
    """
    dialog = None
    window = anchor()
    # look for a previous instance
    for d in window.children():
        if isinstance(d, qt_class):
            dialog = d
    # if there's no previous instance then create a new one
    if dialog is None:
        dialog = qt_class(window)
    # stylize
    if force_style:
        set_style(dialog, not isinstance(dialog, QtGui.QMenu))
    # gc
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    # show dialog
    pos = QtGui.QCursor.pos()
    dialog.move(pos.x(), pos.y())
    # execute callback
    if onshow_event:
        onshow_event(dialog)
    if modal:
        dialog.exec_()
    else:
        dialog.show()
        dialog.raise_()  # ensures dialog window is on top
    return dialog
