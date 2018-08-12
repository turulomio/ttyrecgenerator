## @package libttyrecgenerator
## @brief Library to generate gifs and video from console output

import argparse
import time
import colorama
import datetime
import gettext
import os
import subprocess

#If you are localizing your module, you must take care not to make global changes, e.g. to the built-in namespace. You should not use the GNU gettext API but instead the class-based API.
#Let’s say your module is called “spam” and the module’s various natural language translation .mo files reside in /usr/share/locale in GNU gettext format. Here’s what you would put at the top of your module:
try:
    t = gettext.translation('ttyrecgenerator','/usr/share/locale')
    _ = t.gettext
except:
    print("Error loading translation")


class RecSession:
    def __init__(self):
        self.__hostname="MyLinux"
        self.__cwd="/home/ttyrec/"
        
    def path(self):
        return "{} {}".format(colorama.Fore.RED + "sg" + colorama.Style.RESET_ALL, colorama.Fore.BLUE + "/ttyrec/ # " + colorama.Style.RESET_ALL)

    ## # must be added to s
    def comment(self, s, sleep=4):
        print(self.path()+ colorama.Fore.YELLOW + s + colorama.Style.RESET_ALL)
        time.sleep(sleep)

    def command(self, s, sleep=6):
        print()
        print(self.path() + colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)
        print(subprocess.check_output(s,shell=True).decode('utf-8'))
        time.sleep(sleep)

    def chdir(self, dir, sleep=6):
        print()
        print(self.path() + colorama.Fore.GREEN + "cd " + dir + colorama.Style.RESET_ALL)
        os.chdir(dir)
        print()
        time.sleep(sleep)


    def command_pipe(self, c1,c2, sleep=6):
        cmd = "{}|{}".format(c1,c2)
        print()
        print(self.path() + colorama.Fore.GREEN + cmd + colorama.Style.RESET_ALL)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        print (output.decode('utf-8'))
        time.sleep(6)


    def change_language(self, language):
        if language=="en":
            gettext.install('ttyrecgenerator', 'badlocale')
        else:
            lang1=gettext.translation('ttyrecgenerator', 'locale', languages=[language])
            lang1.install()

