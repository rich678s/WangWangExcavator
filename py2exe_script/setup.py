from distutils.core import setup
import py2exe
setup(
        console=["C:\TDDOWNLOAD\WangWangExcavator\TrapForBB.py"],
        #zipfile="library.zip",
        options={
            "py2exe":{
                "unbuffered":True,
                "optimize":2,
                "compressed":True,
                "bundle_files":2,
                }
            }
        ),