import sys

from . import binding
from . import widgets
from . import decorators
from .helpers import set_style, set_icon, loadUi, wrapinstance

# monkey patch helpers
binding.set_style = set_style
binding.set_icon = set_icon
binding.loadUi = loadUi
binding.wrapinstance = wrapinstance
binding.widgets = widgets  # customized qt widgets
binding.decorators = decorators

ref = sys.modules[__name__]
sys.modules[__name__] = binding
