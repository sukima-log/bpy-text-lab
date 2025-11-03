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
# マテリアル 土壌
# =====================================================
def mtal_soil_00(
    mtal_name="mtal_name"
,   TX_Noise_00_Detail=15
,   TX_Noise_00_Scale=16
):
    # Save : Curren Mode
    current_mode = bpy.context.object.mode
    # 質感を変更する
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexNoise"
    ,   texture_node_name="TX_Noise_00"
    ,   node_location=(-400, 300)
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeBump"
    ,   texture_node_name="Bump_00"
    ,   node_location=(-200, 300)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Noise_00"
    ,   texture_node_name_in="Bump_00"
    ,   output_link="Fac"
    ,   input_link="Height"
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Bump_00"
    ,   texture_node_name_in="Principled BSDF"
    ,   output_link="Normal"
    ,   input_link="Normal"
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeMapping"
    ,   texture_node_name="Mapping_00"
    ,   node_location=(-600, 300)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Mapping_00"
    ,   texture_node_name_in="TX_Noise_00"
    ,   output_link="Vector"
    ,   input_link="Vector"
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexCoord"
    ,   texture_node_name="TX_Coord_00"
    ,   node_location=(-800, 300)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Coord_00"
    ,   texture_node_name_in="Mapping_00"
    ,   output_link="Object"
    ,   input_link="Vector"
    )
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Noise_00"
    ,   element_name="Detail"
    ,   set_value=TX_Noise_00_Detail
    )
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Noise_00"
    ,   element_name="Scale"
    ,   set_value=TX_Noise_00_Scale
    )
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)
