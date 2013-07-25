from functools import wraps
from .QtGui import QProgressDialog
from ..si import sianchor


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
            finally:
                pb.close()
            return f
        return _decorated
    return _wrapped


def bussy(function):
    @wraps(function)
    def _decorated(*args, **kwds):
        self = args[0]
        # disable window
        self.setEnabled(False)
        self.repaint()
        try:
            f = function(*args, **kwds)
        finally:
            # cleanup
            self.setEnabled(True)
            return f
    return _decorated
