from ttyrecgenerator import __version__
from setuptools import setup, Command
from mangenerator import Man

import datetime
import gettext
import os
import site

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
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/ttyrecgenerator/ --delete-after")
        os.chdir("..")

class Video(Command):
    description = "Create video/GIF from console ouput"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.chdir("doc/ttyrec")
        os.system("ttyrecgenerator --output ttyrecgenerator_howto_es 'python3 howto.py --language es' --video")
        os.system("ttyrecgenerator --output ttyrecgenerator_howto_en 'python3 howto.py --language en' --video")
        os.chdir("../..")


class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("rm -Rf {}/ttyrecgenerator*".format(site.getsitepackages()[0]))
        os.system("rm /usr/bin/ttyrecgenerator")
        os.system("rm /usr/share/locale/es/LC_MESSAGES/ttyrecgenerator.mo")
        os.system("rm /usr/share/man/man1/ttyrecgenerator.1")
        os.system("rm /usr/share/man/es/man1/ttyrecgenerator.1")

class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/ttyrecgenerator.pot *.py ttyrecgenerator/*.py doc/ttyrec/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/ttyrecgenerator.pot")
        os.system("msgfmt -cv -o locale/es/LC_MESSAGES/ttyrecgenerator.mo locale/es.po")

        for language in ["en", "es"]:
            self.mangenerator(language)

    def mangenerator(self, language):
        """
            Create man pages for parameter language
        """
        if language=="en":
            gettext.install('ttyrecgenerator', 'badlocale')
            man=Man("man/man1/ttyrecgenerator")
        else:
            lang1=gettext.translation('ttyrecgenerator', 'locale', languages=[language])
            lang1.install()
            man=Man("man/es/man1/ttyrecgenerator")
        print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

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

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(name='ttyrecgenerator',
     version=__version__,
     description='Python module to save console output into a GIF or a video',
     long_description=long_description,
     long_description_content_type='text/markdown',
     classifiers=['Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                  'Programming Language :: Python :: 3',
                 ], 
     keywords='ttyrec save console output',
     url='https://ttyrecgenerator.sourceforge.io/',
     author='Turulomio',
     author_email='turulomio@yahoo.es',
     license='GPL-3',
     packages=['ttyrecgenerator'],
     entry_points = {'console_scripts': ['ttyrecgenerator=ttyrecgenerator.cmd_ttyrecgenerator:main',
                                        ],
                    },
     data_files=[ ('/usr/share/locale/es/LC_MESSAGES/', ['locale/es/LC_MESSAGES/ttyrecgenerator.mo']),
                        ('/usr/share/man/man1/', ['man/man1/ttyrecgenerator.1']), 
                        ('/usr/share/man/es/man1/', ['man/es/man1/ttyrecgenerator.1'])
               ] , 
     cmdclass={
        'doxygen': Doxygen,
        'doc': Doc,
        'uninstall':Uninstall, 
        'video': Video, 
             },
      zip_safe=False
     )
