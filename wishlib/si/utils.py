from .shortcuts import si, sidict, disp


def siget(fullname=""):
    """Returns a softimage object given its fullname."""
    fullname = str(fullname)
    if not len(fullname):
        return None
    return sidict.GetObject(fullname, False)


def inside_softimage():
    """Returns a boolean indicating if the code is executed inside softimage."""
    try:
        disp('XSI.Application')
        return True
    except:
        return False


def cmd_wrapper(cmd_name, **kwds):
    """Wrap and execute a softimage command accepting named arguments"""
    cmd = si.Commands(cmd_name)
    if not cmd:
        raise Exception(cmd_name + " doesnt found!")
    for arg in cmd.Arguments:
        value = kwds.get(arg.Name)
        if value:
            arg.Value = value
    return cmd.Execute()
