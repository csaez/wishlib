from __future__ import absolute_import

def inside_maya():
    try:
        import maya  # detect maya by ducktyping
        return True
    except ImportError:
        return False

if inside_maya():
    from . import qt
    reload(qt)
    from .qt import *
    from . import wrapper
    reload(wrapper)
    from .wrapper import Wrapper
