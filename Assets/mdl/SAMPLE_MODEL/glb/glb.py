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
from BPY_3DCG_ENV.Common.common_top import *
#========================================================================================
#------------------------------------------------
# Global Parameter
#------------------------------------------------
GP_CUBE_SIZE    = 0.3   # 30 cm * 30 cm * 30 cm

#------------------------------------------------
# Objects
#------------------------------------------------
# Sample Light
base_light      = "base_light"
# Create Object
sukima_logo     = "sukima_logo"
# Armature
sukima_logo_bone    = "sukima_logo_bone"

#------------------------------------------------
# Material
#------------------------------------------------
# sukima_logo
MT_SUKIMA_LOGO_BASE         = "MT_SUKIMA_LOGO_BASE"
MT_SUKIMA_LOGO_BLACK        = "MT_SUKIMA_LOGO_BLACK"
MT_SUKIMA_LOGO_ORANGE       = "MT_SUKIMA_LOGO_ORANGE"
MT_SUKIMA_LOGO_GRAY         = "MT_SUKIMA_LOGO_GRAY"
MT_SUKIMA_LOGO_LIGHT_GREEN  = "MT_SUKIMA_LOGO_LIGHT_GREEN"
MT_SUKIMA_LOGO_GREEN        = "MT_SUKIMA_LOGO_GREEN"
#------------------------------------------------
# Animation/Action
#------------------------------------------------
# sukima_logo
ANI_SUKIMA_LOGO_BONE_RUN    = "ANI_SUKIMA_LOGO_BONE_RUN"
#------------------------------------------------
# Generation Flag
#------------------------------------------------
def glb_require_new_objects(
    obj_list=[]
,   flg_name="flg_name"
):
    if (len(obj_list) == 0):
        global base_light_flg
        base_light_flg = \
        mm_cm_lib.require_new_objects(
            obj_list=[base_light]
        ,   gen_flag=False
        )
        global sukima_logo_flg
        sukima_logo_flg = \
        mm_cm_lib.require_new_objects(
            obj_list=[sukima_logo]
        ,   gen_flag=False
        )
        global sukima_logo_bone_flg
        sukima_logo_bone_flg = \
        mm_cm_lib.require_new_objects(
            obj_list=[sukima_logo_bone]
        ,   gen_flag=sukima_logo_flg
        )
    else:
        if  (flg_name == "sample_obj_flg_judge"):
            global sample_obj_flg_judge
            sample_obj_flg_judge = \
            mm_cm_lib.require_new_objects(
                obj_list=obj_list
            ,   gen_flag=False
            )

