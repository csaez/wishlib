from functools import wraps
import sip
from win32com.client import Dispatch as disp
from win32com.client import constants as C
from PyQt4.QtGui import QWidget


# SOFTIMAGE SHORTCUTS
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


def sianchor():
    """
    Return pyqt windows' anchor inside softimage, this function relies on
    pyqtforsoftimage beta5 (https://github.com/caron/PyQtForSoftimage).
    """
    return sip.wrapinstance(long(si.getQtSoftimageAnchor()), QWidget)


def siget(fullname=""):
    """Returns a softimage object given its fullname."""
    fullname = str(fullname)
    if not len(fullname):
        return None
    return sidict.GetObject(fullname, False)


# HELPER FUNCTIONS
def inside_softimage():
    """Returns a boolean indicating if the code is executed inside softimage."""
    try:
        disp('XSI.Application')
        return True
    except:
        return False


def show_qt(qt_class):
    """
    Shows and raise a pyqt window inside softimage ensuring it's not duplicated
    (if it's duplicated then raise the old one).
    qt_class argument should be a class/subclass of QMainWindow, QDialog or any
    non modal Qt top-level window supported by PyQtForSoftimage plugin.
    """
    dialog = None
    anchor = sianchor()
    for i in anchor.children():
        if type(i).__name__ == qt_class.__name__:
            dialog = i
    if not dialog:
        dialog = qt_class(anchor)
    dialog.show()
    dialog.raise_()  # ensures dialog window is on top


# DECORATORS
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
    def decorated(*args, **kwargs):
        try:
            si.BeginUndo()
            f = function(*args, **kwargs)
        finally:
            si.EndUndo()
            return f
    return decorated


# ENCODE / DECODE SOFTIMAGE DATA
def map_recursive(function, iterable):
    """
    Apply function recursively to every item or value of iterable and returns a
    new iterable object with the results.
    """
    if hasattr(iterable, "__iter__"):
        dataOut = iterable.__class__()
        for i in iterable:
            if isinstance(dataOut, dict):
                dataOut[i] = map_recursive(function, iterable[i])
            else:
                # convert to list and append
                if not isinstance(dataOut, list):
                    dataOut = list(dataOut)
                dataOut.append(map_recursive(function, i))
        return dataOut
    return function(iterable)


def _encode(dataIn):
    dataOut = repr(dataIn)
    if repr(dataIn) == "<COMObject <unknown>>":
        dataOut = "si:" + str(dataIn.FullName)
    return dataOut


def _decode(dataIn):
    if dataIn.startswith("si:"):
        fullname = dataIn.replace("si:", "")
        dataOut = siget(fullname)
    else:
        try:
            dataOut = eval(dataIn)
        except:
            dataOut = dataIn
            print "WARNING:", dataIn, "cant be decoded."
    return dataOut

encode = lambda x: repr(map_recursive(_encode, x))
decode = lambda x: map_recursive(_decode, eval(x))


# CLASSES
class SIWrapper(object):

    """
    The class is designed to be used as base class in situations where a python
    object is linked to a softimage dispatched object (otherwise json should be
    a far better solution) and we need some sort of serialization to rebuild the
    class on each execution.
    SIWrapper class override python magic methods in order to create softimage
    custom parameters where encoded/serialized data is stored.
    """

    @classmethod
    def auto_update(cls, function):
        """
        This class method could be used as decorator on subclasses, it ensures
        update method is called after function execution.
        """
        def wrapper(self, *args, **kwargs):
            f = function(self, *args, **kwargs)
            self.update()
            return f
        return wrapper

    # attribute prefixes excluded from serialization
    EXCEPTIONS = ("Name", "obj", "holder", "_holder")

    def __init__(self, obj, holdername="wrapperdata"):
        """
        The init method will create a softimage custom property (self.holder)
        to store/read data via python magic methods.
        The class should be initialized with a softimage host object (stored at
        self.obj) and an optional holdername argument which will be used as the
        softimage custom property name.
        """
        self.obj = obj
        self.holder = self.obj.Properties(holdername)
        if not self.holder:
            self.holder = self.obj.AddCustomProperty(holdername)
        # every time we get a string-like value from softimage's sdk it should be
        # converted to str, in some version they switched to unicode but the
        # code still works with str internally.
        for param in self.holder.Parameters:
            if self._validate_key(str(param.Name)):
                # We are passing skip_softimage = True, otherwise parameters
                # would be overriden with raw values. Internal use only!
                self.__setattr__(str(param.Name), decode(str(param.Value)),
                                 skip_softimage=True)

    def update(self):
        """
        This method should be called when you want to ensure all cached attributes
        are in sync with the actual object attributes at runtime.
        This happens because attributes could store mutable objects and be
        modified outside the scope of this class.
        The most common idiom that isn't automagically caught is mutating a list
        or dictionary. Lets say 'user' object have an attribute named 'friends'
        containing a list, calling 'user.friends.append(new_friend)' only get the
        attribute, SIWrapper isn't aware that the object returned was modified
        and the cached data is not updated.
        """
        for key, value in self.__dict__.iteritems():
            if self._validate_key(key):
                self.holder.Parameters(key).Value = encode(value)

    def _validate_key(self, key):
        """Returns a boolean indicating if the attribute name is valid or not"""
        return not any([key.startswith(i) for i in self.EXCEPTIONS])

    def __setattr__(self, key, value, skip_softimage=False):
        object.__setattr__(self, key, value)
        # super(SIWrapper, self).__setattr__(key, value)
        if any((skip_softimage, not self._validate_key(key),
                type(value) == property)):
            return
        # filtering softimage objects
        if repr(value) == "<COMObject <unknown>>":
            # check if value has a FullName attribute, if not means it's a
            # softimage collection and should be converted to a list in order to
            # work with map_recursively later on.
            # As value is a softimage object the only way to check it is duck
            # typing.
            try:
                value.FullName
            except:
                value = list(value)
        # store encoded attribute's data into its own custom parameter
        if not self.holder.Parameters(key):
            self.holder.AddParameter3(key, C.siString)
        self.holder.Parameters(key).Value = encode(value)

    def __delattr__(self, key):
        super(SIWrapper, self).__delattr__(key)
        # remove the custom parameter
        param = self.holder.Parameters(key)
        if param:
            self.holder.RemoveParameter(param)
