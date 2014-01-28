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
