def inside_maya():
    try:
        import maya  # detect maya by ducktyping
        return True
    except ImportError:
        return False

if inside_maya():
    from .qt import *
    from .wrapper import Wrapper
