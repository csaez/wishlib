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

import os
import sys
from cStringIO import StringIO
from xml.etree import ElementTree as xml


def set_style(widget, force_style_factory=True):
    from wishlib.qt import QtGui
    if force_style_factory:
        widget.setStyle(QtGui.QStyleFactory().create("plastique"))
    style_file = os.path.join(os.path.dirname(__file__), "style",
                              "darkorange.stylesheet")
    with file(style_file) as f:
        stylesheet = f.read()
    widget.setStyleSheet(stylesheet)
    set_icon(widget)


def set_icon(widget):
    from wishlib.qt import QtGui
    icon_file = os.path.join(os.path.dirname(__file__),
                             "images", "cs-icon.png")
    widget.setWindowIcon(QtGui.QIcon(icon_file))


# Thanks to ros-visualization
# http://github.com/ros-visualization/python_qt_binding
def loadUi(uifile, baseinstance=None, package="", custom_widgets=None):
    from wishlib.qt import QtCore, active
    if active == "PyQt4":
        from PyQt4 import uic
        return uic.loadUi(uifile, baseinstance, package)

    elif active == "PySide":
        from PySide.QtUiTools import QUiLoader

        class CustomUiLoader(QUiLoader):
            class_aliases = {"Line": "QFrame"}

            def __init__(self, baseinstance=None, custom_widgets=None):
                super(CustomUiLoader, self).__init__(baseinstance)
                self._base_instance = baseinstance
                self._custom_widgets = custom_widgets or {}

            def createWidget(self, class_name, parent=None, name=''):
                # don't create the top-level widget, if a base instance is set
                if self._base_instance and not parent:
                    return self._base_instance

                if class_name in self._custom_widgets:
                    widget = self._custom_widgets[class_name](parent)
                else:
                    widget = QUiLoader.createWidget(
                        self, class_name, parent, name)

                if str(type(widget)).find(self.class_aliases.get(class_name, class_name)) < 0:
                    sys.modules['QtCore'].qDebug(
                        str('PySide.loadUi(): could not find widget class "%s", defaulting to "%s"' % (class_name, type(widget))))

                if self._base_instance:
                    setattr(self._base_instance, name, widget)

                return widget

        loader = CustomUiLoader(baseinstance, custom_widgets)
        # instead of passing the custom widgets, they should be registered using
        # QUiLoader.registerCustomWidget(), but this does not work in
        # PySide 1.0.6: it simply segfaults...
        ui = loader.load(uifile)
        QtCore.QMetaObject.connectSlotsByName(ui)
        return ui


# thank you Nathan Horne
# http://nathanhorne.com/?p=485
def wrapinstance(ptr, base=None):
    """convert a pointer to a Qt class instance (PySide/PyQt compatible)"""
    if ptr is None:
        return None
    ptr = long(ptr)  # Ensure type
    from wishlib.qt import active, QtCore, QtGui
    if active == "PySide":
        import shiboken
        if base is None:
            qObj = shiboken.wrapInstance(ptr, QtCore.QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, superCls):
                base = getattr(QtGui, superCls)
            else:
                base = QtGui.QWidget
        return shiboken.wrapInstance(ptr, base)
    elif active == "PyQt4":
        import sip
        return sip.wrapinstance(ptr, QtGui.QWidget)
    return None


# thank you Nathan Horne
# http://nathanhorne.com/?p=451
def loadUiType(ui_file):
    from wishlib.qt import active, QtGui
    if active == "PySide":
        import pysideuic
        parsed = xml.parse(ui_file)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text

        with open(ui_file, 'r') as f:
            o = StringIO()
            frame = {}

            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec pyc in frame

            # Fetch the base_class and form class based on their type in the
            # xml from designer
            form_class = frame['Ui_%s' % form_class]
            # base_class = eval('QtGui.%s' % widget_class)
            base_class = getattr(QtGui, widget_class)
        return form_class, base_class
    elif active == "PyQt4":
        from PyQt4 import uic
        return uic.loadUiType(ui_file)
    return None
