import sip
from win32com.client import Dispatch as disp
from win32com.client import constants as C
from PyQt4.QtGui import QWidget

__all__ = ["disp", "C", "si", "log", "sidesk", "sidict", "siproj", "sisel",
           "sifact", "simath", "siui", "siut", "sianchor", "siget",
           "inside_softimage"]


def inside_softimage():
    try:
        disp('XSI.Application')
        return True
    except Exception:
        return False

# SHORTCUTS
if inside_softimage():
    si = disp('XSI.Application')
    log = si.LogMessage
    sidesk = si.Desktop
    sidict = si.Dictionary
    siproj = si.ActiveProject2
    sisel = si.Selection
    sifact = disp('XSI.Factory')
    simath = disp('XSI.Math')
    siui = disp('XSI.UIToolkit')
    siut = disp('XSI.Utils')
    if si.Commands("getQtSoftimageAnchor"):
        sianchor = sip.wrapinstance(long(si.getQtSoftimageAnchor()), QWidget)

    def siget(self, fullname=""):
        fullname = str(fullname)
        if not len(fullname):
            return None
        return sidict.GetObject(fullname, False)
