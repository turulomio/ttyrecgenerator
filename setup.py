from setuptools import setup
from ttyrecgenerator import __version__

setup(name='ttyrecgenerator',
      version=__version__,
      description='Python module to save console output into a GIF or a video',
      url='https://ttyrecgenerator.sourceforge.io/',
      author='Turulomio',
      author_email='turulomio@yahoo.es',
      license='GPL-3',
      packages=['ttyrecgenerator'],
#      $ python
#>>> import funniest.command_line
#>>> funniest.command_line.main()
#The main() function can then be registered like so:
      entry_points = {
        'console_scripts': ['ttyrecgenerator=ttyrecgenerator.libttyrecgenerator:main'],
      },
      zip_safe=False)
