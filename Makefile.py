#!/usr/bin/python3
import argparse
import datetime
import os
from subprocess import call
from multiprocessing import cpu_count
from mangenerator import Man
from ttyrecgenerator import __version__
import gettext


# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work
gettext.install('ttyrecgenerator', 'locale')


def shell(*args):
    print(" ".join(args))
    call(args,shell=True)

def makefile_dist_sources():
    shell("{} setup.py sdist".format(args.python))

def makefile_doc():
    #es
    shell("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/ttyrecgenerator.pot *.py doc/ttyrec/*.py")
    shell("msgmerge -N --no-wrap -U locale/es.po locale/ttyrecgenerator.pot")
    shell("msgfmt -cv -o locale/es/LC_MESSAGES/ttyrecgenerator.mo locale/es.po")

    for language in ["en", "es"]:
        mangenerator(language)

def makefile_install():
    shell("install -o root -d "+ prefixbin)
    shell("install -o root -d "+ prefixlib)
    shell("install -o root -d "+ prefixshare)
    shell("install -o root -d "+ prefixlocale+"/es/LC_MESSAGES/")
    shell("install -o root -d "+ prefixman+"/man1")
    shell("install -o root -d "+ prefixman+"/es/man1")

    shell("install -m 755 -o root ttyrecgenerator.py "+ prefixbin+"/ttyrecgenerator")
    shell("install -m 755 -o root libttyrecgenerator.py "+ prefixlib+"/libttyrecgenerator.py")
    shell("install -m 644 -o root locale/es/LC_MESSAGES/ttyrecgenerator.mo " + mo_es)
    shell("install -m 644 -o root locale/ttyrecgenerator.en.1 "+ prefixman+"/man1/ttyrecgenerator.1")
    shell("install -m 644 -o root locale/ttyrecgenerator.es.1 "+ prefixman+"/es/man1/ttyrecgenerator.1")

def makefile_uninstall():
    shell("rm " + prefixbin + "/ttyrecgenerator")
    shell("rm -Rf " + prefixshare)
    shell("rm -Rf " + prefixlib)
    shell("rm " + mo_es)
    shell("rm " + man_en)
    shell("rm " + man_es)

def doxygen():
    os.chdir("doc")
    shell("doxygen Doxyfile")
    os.chdir("..")

def video():
    os.chdir("doc/ttyrec")
    shell("ttyrecgenerator --output ttyrecgenerator_howto_es 'python3 howto.py --language es' --video")
    shell("ttyrecgenerator --output ttyrecgenerator_howto_en 'python3 howto.py --language en' --video")
    os.chdir("../..")


def mangenerator(language):
    """
        Create man pages for parameter language
    """
    if language=="en":
        gettext.install('ttyrecgenerator', 'badlocale')
    else:
        lang1=gettext.translation('ttyrecgenerator', 'locale', languages=[language])
        lang1.install()
    print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

    man=Man("locale/ttyrecgenerator.{}".format(language))
    man.setMetadata("ttyrecgenerator",  1,   datetime.date.today(), "Mariano Muñoz", _("Remove innecesary files or directories with a date and time pattern in the current directory."))
    man.setSynopsis("""[-h] [--version] (--create_example | --remove | --pretend)
                    [--pattern PATTERN] [--disable_log]
                    [--remove_mode {RemainFirstInMonth,RemainLastInMonth}]
                    [--too_young_to_delete TOO_YOUNG_TO_DELETE]
                    [--max_files_to_store MAX_FILES_TO_STORE]""")
    man.header(_("DESCRIPTION"), 1)
    man.paragraph(_("This app has the following mandatory parameters:"), 1)
    man.paragraph("--create_example", 2, True)
    man.paragraph(_("Create two directories called 'example' and 'example_directories' in the current working directory and fill it with example files with date and time patterns."), 3)
    man.save()
    ########################################################################



if __name__ == '__main__':
    start=datetime.datetime.now()
    parser=argparse.ArgumentParser(prog='Makefile.py', description='Makefile in python', epilog=_("Developed by Mariano Muñoz 2018-{}".format(datetime.date.today().year)), formatter_class=argparse.RawTextHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--doc', help=_("Generate docs and i18n"),action="store_true",default=False)
    group.add_argument('--doxygen', help=_("Generate doxygen api documentation"), action="store_true", default=False)
    group.add_argument('--install', help=_("Directory to install app. / recomended"), action="store", metavar="PATH", default=None)
    group.add_argument('--uninstall', help=_("Uninstall. / recomended") ,action="store", metavar="PATH", default=None)
    group.add_argument('--video', help=_("Make a HOWTO video and gif "), action="store_true",default=False)
    group.add_argument('--dist_sources', help=_("Make a sources tar"), action="store_true",default=False)
    parser.add_argument('--python', help=_("Python path"), action="store",default='/usr/bin/python3')

    args=parser.parse_args()

    if args.install or args.uninstall:
        if args.install:
            destdir=args.install
        elif args.uninstall:
            destdir=args.uninstall

        prefixbin=destdir+"/usr/bin"
        prefixshare=destdir+"/usr/share/ttyrecgenerator"
        prefixman=destdir+"/usr/share/man"
        prefixlocale=destdir+"/usr/share/locale"
        prefixlib=destdir+"/usr/lib/ttyrecgenerator"
        mo_es=prefixlocale+"/es/LC_MESSAGES/ttyrecgenerator.mo"
        man_en=prefixman+"/man1/ttyrecgenerator.1"
        man_es=prefixman+"/es/man1/ttyrecgenerator.1"

        if args.install:
            makefile_install()
        if args.uninstall:
            makefile_uninstall()

    elif args.doc==True:
        makefile_doc()
    elif args.dist_sources==True:
        makefile_dist_sources()
    elif args.doxygen==True:
        doxygen()
    elif args.video==True:
        video()

    print ("*** Process took {} using {} processors ***".format(datetime.datetime.now()-start , cpu_count()))
