import os
import sip
from PyQt4.QtGui import QWidget, QApplication

from .shortcuts import si


def sianchor():
    """
    Return pyqt anchor inside softimage, this function relies on
    pyqtforsoftimage beta5 (https://github.com/caron/PyQtForSoftimage).
    """
    # get the anchor from pyqtfromsoftimage addon
    sianchor = si.getQtSoftimageAnchor()
    # load plugins
    import PyQt4
    path = os.path.join(os.path.dirname(PyQt4.__file__), "plugins")
    QApplication.instance().addLibraryPath(path)
    # return a python wrapped anchor
    return sip.wrapinstance(long(sianchor), QWidget)


def show_qt(qt_class, modal=False, onshow_event=None):
    """
    Shows and raise a pyqt window inside softimage ensuring it's not duplicated
    (if it's duplicated then raise the old one).
    qt_class argument should be a class/subclass of QMainWindow, QDialog or any
    top-level window supported by PyQtForSoftimage plugin.
    onshow_event provides a way to pass a function to execute before the window
    is showed on screen, it can be specially handy on modal windows.
    Returns the qt_class instance.
    """
    dialog = None
    anchor = sianchor()
    # look for a previous instance
    for d in anchor.children():
        if isinstance(d, qt_class):
            dialog = d
    # if there's no previous instance then create a new one
    if dialog is None:
        dialog = qt_class(anchor)
    # execute callback
    if onshow_event:
        onshow_event(dialog)
    # show dialog
    if modal:
        dialog.exec_()
    else:
        dialog.show()
        dialog.raise_()  # ensures dialog window is on top
    return dialog
