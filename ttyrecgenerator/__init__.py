# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
#from .initialise import init, deinit, reinit, colorama_text
#from .ansi import Fore, Back, Style, Cursor
#from .ansitowin32 import AnsiToWin32
import datetime

import locale
import gettext
import os

from .libttyrecgenerator import RecSession 

#language = gettext.translation ('ttyrecgenerator', 'locale' )
#language.install()

__version__ = '0.1.0'
__versiondate__=datetime.date(2018,8,11)
