THIS PROJECT IS NOW ARCHIVED DUE TO TTREC IS MORE THAN 10 YEARS WITHOUT A MODIFICATION. ASCIINEMA IS A BETTER SOLUTION


Source code & Development:
    https://ttyrecgenerator.sourceforge.io
Doxygen documentation:
    http://turulomio.users.sourceforge.net/doxygen/ttyrecgenerator/
Main developer web page:
    http://turulomio.users.sourceforge.net/en/proyectos.html
Gentoo ebuild
    You can find a Gentoo ebuild in https://sourceforge.net/p/xulpymoney/code/HEAD/tree/myportage/dev-python/ttyrecgenerator/

Description
===========
Command and API to generate animated gifs from scripts output.

License
=======
GPL-3

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.
* https://pypi.org/project/mangenerator/, to generate man files.
* https://invisible-island.net/xterm/, as tty used to rec with ttyrec.
* https://github.com/mjording/ttyrec, system to record console output.
* https://github.com/icholy/ttygif, program to generate animated gif from ttyrec saves.
* https://www.ffmpeg.org/, to generate videos from animated gifs.

Usage
=====
You can see this animated gif:

.. image:: https://sourceforge.net/p/ttyrecgenerator/code/HEAD/tree/doc/ttyrec/ttyrecgenerator_howto_en.gif?format=raw
   :height: 800px
   :width: 600px
   :scale: 100 %
   :align: center

Changelog
=========
0.6.0
  * Replaces --language to --lc_all. Now translation are more easy
0.5.0
  * Added command_fake in RecSession to pretend a command
  * Improved README.rst and doxygen documentation
  * Added project icon
0.4.0
  * Added ttyrecgenerator howto in gif and video
0.3.0
  * Console output command is now in color
  * Output commands is now localized
0.2.2
  * Improving README
0.2.0
  * Solved problems with internacionalization distribution
0.1.0
  * Basic funcionality
