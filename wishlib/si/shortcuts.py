from win32com.client import Dispatch as disp
from win32com.client import constants as C

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
