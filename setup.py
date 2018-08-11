from ttyrecgenerator import __version__
from setuptools import setup, Command

# for setuptools use
# from setuptools.command.build_py import build_py as build

import os
import shutil

package = "mypackage"      # <- change this

podir = "locale"
pos = [x for x in os.listdir(podir) if x[-3:] == ".po"]
langs = sorted([os.path.split(x)[-1][:-3] for x in pos])


def modir(lang):
    mobase = "build/mo"
    return os.path.join(mobase, lang)


def mkmo(lang):
    outpath = modir(lang)
    if os.path.exists(outpath):
        shutil.rmtree(outpath)
    os.makedirs(outpath)

    inpath = os.path.join(podir, lang + ".po")

    cmd = "msgfmt %s -o %s/%s.mo" % (inpath, outpath, package)

    os.system(cmd)


def merge_i18n():
    cmd = "LC_ALL=C intltool-merge -u -c ./po/.intltool-merge-cache ./po "
    for infile in (x[:-3] for x in os.listdir('.') if x[-3:] == '.in'):
        print("Processing %s.in to %s" % (infile, infile))

        if 'desktop' in infile:
            flag = '-d'
        elif 'schema' in infile:
            flag = '-s'
        elif 'xml' in infile:
            flag = '-x'
        else:
            flag = ''

        if flag:
            os.system("%s %s %s.in %s" % (cmd, flag, infile, infile))

def polist():
    dst_tmpl = "share/locale/%s/LC_MESSAGES/"
    polist = [(dst_tmpl % x, ["%s/%s.mo" % (modir(x), package)]) for x in langs]

    return polist

class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.chdir("..")


def shell(*args):
    print(" ".join(args))
    call(args,shell=True)

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


class my_build_i18n(Command):
    description = "Create/update po/pot translation files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating POT file")
        cmd = "cd po; intltool-update --pot --gettext-package=%s" % package
        os.system(cmd)

        for lang in langs:
            print("Updating %s PO file" % lang)
            cmd = "cd po; intltool-update --dist \
                   --gettext-package=%s %s >/dev/null 2>&1" % (package, lang)
            os.system(cmd)


class my_clean:#(clean):
    def run(self):
        clean.run(self)

        filelist = [x[:-3] for x in os.listdir('.') if x[-3:] == '.in']
        filelist += ['po/.intltool-merge-cache']
        for infile in filelist:
            if os.path.exists(infile):
                os.unlink(infile)

        for dir in ['build/mo', 'build/scripts-2.7', 'build/scripts-3.4'
                    'build/scripts-3.5']:
            if os.path.exists(dir):
                shutil.rmtree(dir)



setup(name='ttyrecgenerator',
      version=__version__,
      description='Python module to save console output into a GIF or a video',
      url='https://ttyrecgenerator.sourceforge.io/',
      author='Turulomio',
      author_email='turulomio@yahoo.es',
      license='GPL-3',
      packages=['ttyrecgenerator'],
      entry_points = {'console_scripts': ['ttyrecgenerator=ttyrecgenerator.cmd_ttyrecgenerator:main',
                                          ],
                     },
                     
        
      data_files=[ ('locale/es/LC_MESSAGES/', ['locale/es/LC_MESSAGES/ttyrecgenerator.mo']),
               ],
               
    cmdclass={
        'doxygen': Doxygen,
             },
      zip_safe=False
     )
