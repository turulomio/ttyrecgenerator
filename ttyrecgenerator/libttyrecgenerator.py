## @namespace ttyrecgenerator.libttyrecgenerator
## @brief Library to generate gifs and video from console output
import argparse
import time
import colorama
import datetime
import gettext
import locale
import os
import pkg_resources
import platform
import subprocess

try:
    t = gettext.translation('ttyrecgenerator', pkg_resources.resource_filename('ttyrecgenerator', "locale"))
    _ = t.gettext
except:
    _ = str

## @brief Class with predefinied pauses and colors. Allows to launch commands and pretend it's launch
## The use of this class is not mandatory
## This class provide methods with predefined pauses
class RecSession:
    def __init__(self):
        self.__hostname="MyLinux"
        self.__cwd="/home/ttyrec/"

    ## This function emulates the hostnmae and the current directory, with the colors of a unix tty
    def path(self):
        return "{} {}".format(colorama.Style.BRIGHT + colorama.Fore.RED + "sg" + colorama.Style.RESET_ALL, colorama.Style.BRIGHT + colorama.Fore.BLUE + "/ttyrec/ # " + colorama.Style.RESET_ALL)

    ## This function prints comments is yellow
    ## # must be added to s
    def comment(self, s, sleep=3):
        print(self.path()+ colorama.Fore.YELLOW + s + colorama.Style.RESET_ALL)
        time.sleep(sleep)


    ## This function launches a command and prints the command in green
    def command(self, s, sleep=5):
        print(self.path() + colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)
        p=subprocess.run(s,shell=True, stderr=subprocess.STDOUT)
        time.sleep(sleep)

    ## This method changes current directory and shows a cd command in green
    def chdir(self, dir, sleep=5):
        print(self.path() + colorama.Fore.GREEN + "cd " + dir + colorama.Style.RESET_ALL)
        os.chdir(dir)
        print()
        time.sleep(sleep)

    ## This method launches commands with a pipe and prints it in green
    def command_pipe(self, c1,c2, sleep=5):
        cmd = "{}|{}".format(c1,c2)
        print(self.path() + colorama.Fore.GREEN + cmd + colorama.Style.RESET_ALL)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        print (output.decode('utf-8'))
        time.sleep(6)

    ## Sometimes when you are documenting a command. If you invoke it from the script, you enter in a bucle
    ##
    ## This function prints in console in the command color, but doesn't call the command
    ## @param s String with the command
    ## @param sleep Number of seconds to sleep after function
    def command_fake(self, s, sleep=5):
        print(self.path() + colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)
        time.sleep(sleep)

def platform_incompatibility():
    print( colorama.Style.BRIGHT + colorama.Fore.RED +  _("This funcionality doen't work on {}. Please move to Linux.").format(platform.system()) + colorama.Style.RESET_ALL)