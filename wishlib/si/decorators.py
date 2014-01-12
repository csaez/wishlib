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
