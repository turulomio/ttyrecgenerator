#!/usr/bin/python3
import argparse
import gettext
import pkg_resources

from ttyrecgenerator import RecSession
gettext.install('ttyrecgenerator', pkg_resources.resource_filename('ttyrecgenerator', 'locale'))

parser=argparse.ArgumentParser(description='HOWTO to save with ttyrec', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--language', help=_("Sets output language"), action="store",default='en')
args=parser.parse_args()

r=RecSession()
r.change_language(args.language)
r.comment("# " + _("This is a video to show how to use 'ttyrecgenerator' command"))
r.comment("# " + _("First we have to create a unix command. This file in doc/ttyrec directory is an example. We display it:"))
r.command("cat howto.py")
r.comment("# " + _("Now we are going to execute it with:"))
r.comment("ttyrecgenerator --output ttyrecgenerator_howto_es 'python3 howto.py --language es'")
r.comment("# " +_("A file called ttyrecgenerator_howto_es.gif is generated"))
r.comment("# " + _("If you want to generate a video use --video parameter"))
