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
if git_root and git_root not in sys.path:
    sys.path.append(git_root)
# Common Setting
from Common.common_top import *
#========================================================================================

# =====================================================
# マテリアル 金属
# =====================================================
def mtal_metal_00(
    mtal_name="mtal_name"
):
    # Save : Curren Mode
    current_mode = bpy.context.object.mode
    # つやを出す
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="Principled BSDF"
    ,   element_name="Metallic"
    ,   set_value=1.0
    )
    # 値が小さいほど表面が滑らか
    # 値小さい : 鏡面反射に近づく
    # 値大きい : やわらかい明るさを持つ 
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="Principled BSDF"
    ,   element_name="Roughness"
    ,   set_value=0.3
    )
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)

