import os
from distutils.core import setup
import py2exe

mydata_files = [('resources', ['resources/background.jpg'])]
mydata_files.append(('resources', ['resources/blood_splat.png']))
mydata_files.append(('resources', ['resources/bullet.png']))
mydata_files.append(('resources', ['resources/graveyard.png']))
mydata_files.append(('resources', ['resources/supplies.png']))
mydata_files.append(('resources', ['resources/survivor.png']))
mydata_files.append(('resources', ['resources/survivor_dead.png']))
mydata_files.append(('resources', ['resources/survivor_hit.png']))
mydata_files.append(('resources', ['resources/zombie.png']))

origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in \
        ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"):
        return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one

setup(
    console=['outbreak_z.py'], 
    options = {'py2exe': {'bundle_files': 1}},
    data_files=mydata_files
)