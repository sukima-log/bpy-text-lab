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

# =====================================================
# マテリアル 漆喰
# =====================================================
def mtal_plaster_00(
    mtal_name="mtal_name"
,   TX_Noise_00_Detail=15
,   TX_Noise_00_Scale=50
,   TX_Bump_00_Strength=0.3
):
    # Save : Curren Mode
    current_mode = bpy.context.object.mode
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeBump"
    ,   texture_node_name="TX_Bump_00"
    ,   node_location=(-200, 100)
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexNoise"
    ,   texture_node_name="TX_Noise_00"
    ,   node_location=(-400, 100)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Noise_00"
    ,   texture_node_name_in="TX_Bump_00"
    ,   output_link="Fac"
    ,   input_link="Height"
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Bump_00"
    ,   texture_node_name_in="Principled BSDF"
    ,   output_link="Normal"
    ,   input_link="Normal"
    )
    # アドオンショートカット -> 手動
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeMapping"
    ,   texture_node_name="Mapping_00"
    ,   node_location=(-600, 100)
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
    ,   node_location=(-800, 100)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Coord_00"
    ,   texture_node_name_in="Mapping_00"
    ,   output_link="Object"
    ,   input_link="Vector"
    )
    # 値変更
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
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Bump_00"
    ,   element_name="Strength"
    ,   set_value=TX_Bump_00_Strength
    )
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)


def mtal_plaster_01(
    mtal_name="mtal_name"
,   TX_Noise_00_Detail=15
,   TX_Noise_00_Scale=50
,   TX_Bump_00_Strength=0.3
):
    # Save : Curren Mode
    current_mode = bpy.context.object.mode
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)