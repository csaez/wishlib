from .shortcuts import si, C
from .utils import siget


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
    try:
        dataOut = "si:" + str(dataIn.FullName)
    except:
        dataOut = repr(dataIn)
    return dataOut


def _decode(dataIn):
    if dataIn.startswith("si:"):
        fullname = dataIn.replace("si:", "")
        dataOut = siget(fullname)
    else:
        try:
            dataOut = eval(dataIn)
        except:
            # dataOut = dataIn
            # print "WARNING:", dataIn, "cant be decoded."
            return None
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
        self.namespace = "data_"
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
                safe_name = param.Name.replace(self.namespace, "")
                self.__setattr__(str(safe_name), decode(str(param.Value)),
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
        self.holder = siget(self.holder.FullName)  # fix dispatch issues
        for key, value in self.__dict__.iteritems():
            key = self.namespace + key
            if self._validate_key(key):
                if not self.holder.Parameters(key):
                    self.holder.AddParameter3(key, C.siString)
                self.holder.Parameters(key).Value = encode(value)

    def _validate_key(self, key):
        """Returns a boolean indicating if the attribute name is valid or not"""
        return not any([key.startswith(i) for i in self.EXCEPTIONS])
        # return True

    def __setattr__(self, key, value, skip_softimage=False):
        object.__setattr__(self, key, value)
        # super(SIWrapper, self).__setattr__(key, value)
        if any((skip_softimage, not self._validate_key(key),
                type(value) == property, not hasattr(self, "holder"))):
            return
        # CHECK SOFTIMAGE OBJECTS
        # check if value has a FullName attribute, if not means it's a
        # softimage collection and should be converted to a list in order to
        # work with map_recursively later on.
        try:
            if si.ClassName(value):  # is a softimage object
                try:
                    value.FullName  # has a fullname
                except:
                    value = list(value)  # it's a xsicollection
        except:
            pass
        # store encoded attribute's data into its own custom parameter
        self.holder = siget(self.holder.FullName)
        key = self.namespace + key
        if not self.holder.Parameters(key):
            self.holder.AddParameter3(key, C.siString)
        self.holder.Parameters(key).Value = encode(value)

    def __delattr__(self, key):
        super(SIWrapper, self).__delattr__(key)
        # remove the custom parameter
        key = self.namespace + key
        param = self.holder.Parameters(key)
        if param:
            self.holder.RemoveParameter(param)