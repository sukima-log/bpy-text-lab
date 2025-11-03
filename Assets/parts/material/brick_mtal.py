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
# マテリアル レンガ
# =====================================================
def mtal_brick_00(
    mtal_name="mtal_name"
,   Color1=(0.802, 0.619, 0.433, 1)
,   Color2=(0.402, 0.176, 0.095, 1)
,   Mortar=(0.06, 0.04, 0.035, 1)
,   Mortar_Size=0.005
):
    # Save : Curren Mode
    current_mode = bpy.context.object.mode
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexBrick"
    ,   texture_node_name="TX_Brick_00"
    ,   node_location=(-200, 300)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Brick_00"
    ,   texture_node_name_in="Principled BSDF"
    ,   output_link="Color"
    ,   input_link="Base Color"
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeMapping"
    ,   texture_node_name="Mapping_00"
    ,   node_location=(-400, 300)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Mapping_00"
    ,   texture_node_name_in="TX_Brick_00"
    ,   output_link="Vector"
    ,   input_link="Vector"
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexCoord"
    ,   texture_node_name="TX_Coord_00"
    ,   node_location=(-600, 300)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Coord_00"
    ,   texture_node_name_in="Mapping_00"
    ,   output_link="Object"
    ,   input_link="Vector"
    )
    # 溝のサイズ
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Brick_00"
    ,   element_name="Mortar Size"
    ,   set_value=Mortar_Size
    )
    # レンガの色変更
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Brick_00"
    ,   element_name="Color1"
    ,   set_value=Color1
    )
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Brick_00"
    ,   element_name="Color2"
    ,   set_value=Color2
    )
    # 溝の色
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Brick_00"
    ,   element_name="Mortar"
    ,   set_value=Mortar
    )
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)


    