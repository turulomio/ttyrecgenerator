#!/usr/bin/python3
## @package ttyrecgenerator
## @brief Program that generate gifs and video from console output

import argparse
import time
import colorama
import datetime
import gettext
import os
import subprocess
from .__init__ import __version__, __versiondate__

# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work. Nuevo sistema2
#gettext.install('ttyrecgenerator','locale')

#If you are localizing your module, you must take care not to make global changes, e.g. to the built-in namespace. You should not use the GNU gettext API but instead the class-based API.
#Let’s say your module is called “spam” and the module’s various natural language translation .mo files reside in /usr/share/locale in GNU gettext format. Here’s what you would put at the top of your module:

try:
    t = gettext.translation('ttyrecgenerator','/usr/share/locale')
    _ = t.gettext
except:
    print("Error in translation")



def main():
    parser=argparse.ArgumentParser(prog='ttyrecgenerator', description=_('Create an animated gif/video from the output of the program passed as parameter'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(__versiondate__.year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('program',  help=_("Path to program"))
    parser.add_argument('--output', help=_("Ttyrec output path"), action="store", default="ttyrecord.rec")
    parser.add_argument('--video', help=_("Makes a simulation and doesn't remove files"), action="store_true", default=False)
    args=parser.parse_args()

    subprocess.run(["xterm", "-hold", "-bg", "black", "-geometry", "140x400", "-fa", "monaco", "-fs", "18", "-fg", "white", "-e", "ttyrec -e '{0}' {1}; ttygif {1}".format(args.program, args.output)])
    os.system("mv tty.gif {}.gif".format(args.output))
    if args.video==True:
        subprocess.run(["ffmpeg", "-i", "{}.gif".format(args.output), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "{}.mp4".format(args.output)])


if __name__ == "__main__":
    main()