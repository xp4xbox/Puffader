# setup script for py2exe

from distutils.core import setup
import py2exe

setup(script_args = ['py2exe'],
      windows=[{'script':'Puffader.py'}],
      options = {'py2exe': {'excludes': ['Tkconstants', 'Tkinter'],
							'includes':['email.mime.multipart', 'email.mime.image'],
							'bundle_files':1
                            },
                 },
		zipfile = None,
		)
