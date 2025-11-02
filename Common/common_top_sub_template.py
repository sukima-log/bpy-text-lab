# Sub Code
import bpy, os, sys, subprocess
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
# Common Setting
from bpy_text_lab.Common.common_top import *
#========================================================================================
