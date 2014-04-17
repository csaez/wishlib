# The MIT License (MIT)

# Copyright (c) 2014 Cesar Saez

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import

from pymel import core as pm
from ..utils import map_recursive


# ENCODE / DECODE SOFTIMAGE DATA
def _encode(dataIn):
    try:
        dataOut = "pm:" + str(dataIn.name())
    except:
        dataOut = repr(dataIn)
    return dataOut


def _decode(dataIn):
    if dataIn.startswith("pm:"):
        fullname = dataIn.replace("pm:", "")
        dataOut = pm.PyNode(fullname)
    else:
        try:
            dataOut = eval(dataIn)
        except:
            return None
    return dataOut

encode = lambda x: repr(map_recursive(_encode, x))
decode = lambda x: map_recursive(_decode, eval(x))


class Wrapper(object):

    """
    The class is designed to be used as base class in situations where a python
    object is linked to a maya node and we need some sort of serialization to
    rebuild the instance.
    Wrapper class override python magic methods storing encoded/serialized data
    is maya attributes as strings.
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
    EXCEPTIONS = ("obj", "node")

    def __init__(self, obj, holdername="metadata_"):
        """
        The class should be initialized with a maya host node (stored at
        self.obj) and an optional namespace which will be used as prefix on
        maya attribute names.
        """
        if isinstance(obj, basestring):
            obj = pm.PyNode(obj)
        self.obj = self.node = obj
        self.namespace = holdername
        for attr in self.obj.listAttr():
            attr_name = str(attr.name().split(".")[-1])
            if self.namespace not in attr_name:
                continue
            if self._validate_key(attr_name):
                # pass skip = True, otherwise parameters would override with
                # raw values. Internal use only!
                safe_name = attr_name.replace(self.namespace, "")
                self.__setattr__(safe_name, decode(attr.get()), skip=True)

    def update(self):
        """
        This method should be called to ensure all cached attributes
        are in sync with the metadata at runtime.
        This happens because attributes could store mutable objects and be
        modified outside the scope of this class.
        The most common idiom that isn't automagically caught is mutating a list
        or dictionary. Lets say 'user' object have an attribute named 'friends'
        containing a list, calling 'user.friends.append(new_friend)' only get the
        attribute, Wrapper isn't aware that the object returned was modified
        and the cached data is not updated.
        """
        for key, value in self.__dict__.iteritems():
            key = self._compose(key)
            if self._validate_key(key):
                if not self.obj.hasAttr(key):
                    pm.addAttr(self.obj, ln=key, dt="string")
                self.obj.attr(key).set(encode(value))

    def _compose(self, key):
        return self.namespace + "_" + key

    def _validate_key(self, key):
        return not any([key.startswith(i) for i in self.EXCEPTIONS])

    def __setattr__(self, key, value, skip=False):
        super(Wrapper, self).__setattr__(key, value)
        if any((skip, not self._validate_key(key),
                type(value) == property)):
            return
        if not hasattr(self, "namespace"):
            return
        key = self._compose(key)
        if not self.obj.hasAttr(key):
            self.obj.addAttr(key, dt="string")
        self.obj.attr(key).set(encode(value))

    def __delattr__(self, key):
        super(Wrapper, self).__delattr__(key)
        key = self._compose(key)
        attr = self.obj.attr(key)
        if attr:
            pm.deleteAttr(attr)
