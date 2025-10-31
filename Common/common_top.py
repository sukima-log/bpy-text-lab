#------------------------------------------------------------------
# = Define (環境毎に変更)
#------------------------------------------------------------------
# Extensions Download Dir
__addon_directory = "C:/Users/..."
#------------------------------------------------------------------
# = Import
#------------------------------------------------------------------
import bpy
import math
import random
import numpy as np
from mathutils import Matrix, Vector
import mathutils
import os
import sys
import bmesh
import requests
import urllib.request
import zipfile
import importlib
import time
import json
import pkgutil
import subprocess
#------------------------------------------------------------------
# = Set Path
#------------------------------------------------------------------
# Get File Path
script_path = bpy.path.abspath(bpy.context.space_data.text.filepath)
script_dir = os.path.dirname(script_path)
# Get Git Root
git_root = subprocess.run(
    ["git", "-C", script_dir, "rev-parse", "--show-toplevel"],
    stdout=subprocess.PIPE, text=True
).stdout.strip()
# Add the parent directory of the root to sys.path
if git_root:
    parent = os.path.dirname(git_root)
    if parent not in sys.path:
        sys.path.append(parent)

# Common Lib
from BPY_3DCG_ENV.Mylib import  (
    mdl_cm_lib
,   mtal_cm_lib
,   mm_cm_lib
,   ani_cm_lib
)
#------------------------------------------------------------------
# = Auto Reload
#------------------------------------------------------------------
def get_latest_mtime_in_dir(directory):
    latest_mtime = 0
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py"):
                full_path = os.path.join(root, f)
                mtime = os.path.getmtime(full_path)
                if mtime > latest_mtime:
                    latest_mtime = mtime
    return latest_mtime

def _auto_reload_modules(modules):
    this_mod = sys.modules[__name__]
    if not hasattr(this_mod, "_file_mtimes"):
        this_mod._file_mtimes = {}

    def reload_if_changed(mod):
        path = getattr(mod, "__file__", None)
        if not path:
            return

        if os.path.basename(path) in ("__init__.py", "__init__.pyc"):
            mtime = get_latest_mtime_in_dir(os.path.dirname(path))
        else:
            mtime = os.path.getmtime(path)

        if mtime != this_mod._file_mtimes.get(path):
            importlib.reload(mod)
            this_mod._file_mtimes[path] = mtime

    for mod in modules:
        reload_if_changed(mod)

        # If it's a package, also reload its submodules
        if hasattr(mod, "__path__"):  
            for _, subname, ispkg in pkgutil.walk_packages(mod.__path__, mod.__name__ + "."):
                if subname in sys.modules:
                    reload_if_changed(sys.modules[subname])
#------------------------------------------------------------------
# = Pre Process
#------------------------------------------------------------------
