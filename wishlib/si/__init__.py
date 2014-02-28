from win32com.client import Dispatch as disp


def inside_softimage():
    """Returns a boolean indicating if the code is executed inside softimage."""
    try:
        disp('XSI.Application')
        return True
    except:
        return False

if inside_softimage():
    from .shortcuts import *
    from .decorators import *
    from .math import *
    from .qt import *
    from .siwrapper import *
    from .utils import *
