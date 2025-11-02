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
# マテリアル 木素材 フローリング
# =====================================================
def mtal_wood_00(
    mtal_name="mtal_name"
,   TX_Brick_00_Color1=(0.802, 0.619, 0.433, 1)
,   TX_Brick_00_Color2=(0.402, 0.176, 0.095, 1)
,   TX_Brick_00_Mortar=(0.06, 0.04, 0.035, 1)
,   TX_Brick_00_Mortar_Size=0.005
,   Mapping_01_Scale=(1, 1, 0.2)
,   TX_Noise_00_Scale=16.5
,   TX_Noise_00_Distortion=2.2
,   TX_Noise_00_Detail=15
,   Mix_RGB_00_Factor=1.0
,   Bump_00_Strength=0.15
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
    ,   set_value=TX_Brick_00_Mortar_Size
    )
    # レンガの色変更
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Brick_00"
    ,   element_name="Color1"
    ,   set_value=TX_Brick_00_Color1
    )
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Brick_00"
    ,   element_name="Color2"
    ,   set_value=TX_Brick_00_Color2
    )
    # 溝の色
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Brick_00"
    ,   element_name="Mortar"
    ,   set_value=TX_Brick_00_Mortar
    )
    # --------------------
    # 木の模様を付ける
    # --------------------
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexNoise"
    ,   texture_node_name="TX_Noise_00"
    ,   node_location=(-200, -100)
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeMix"
    ,   texture_node_name="Mix_RGB_00"
    ,   node_location=(0, -100)
    ,   settings=[{"name": "data_type", "value": 'RGBA'}]
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Brick_00"
    ,   texture_node_name_in="Mix_RGB_00"
    ,   output_link="Color"
    ,   input_link="A"
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Mix_RGB_00"
    ,   texture_node_name_in="Principled BSDF"
    ,   output_link="Result"
    ,   input_link="Base Color"
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Noise_00"
    ,   texture_node_name_in="Mix_RGB_00"
    ,   output_link="Fac"
    ,   input_link="B"
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeMapping"
    ,   texture_node_name="Mapping_01"
    ,   node_location=(-400, -100)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Mapping_01"
    ,   texture_node_name_in="TX_Noise_00"
    ,   output_link="Vector"
    ,   input_link="Vector"
    )
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexCoord"
    ,   texture_node_name="TX_Coord_01"
    ,   node_location=(-600, -100)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Coord_01"
    ,   texture_node_name_in="Mapping_01"
    ,   output_link="Object"
    ,   input_link="Vector"
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Mapping_01"
    ,   texture_node_name_in="TX_Noise_00"
    ,   output_link="Vector"
    ,   input_link="Vector"
    )
    # -----------------------------
    # 木目のような歪みを追加する
    # -----------------------------
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="Mapping_01"
    ,   element_name="Scale"
    ,   set_value=Mapping_01_Scale
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
    ,   node_name="TX_Noise_00"
    ,   element_name="Distortion"
    ,   set_value=TX_Noise_00_Distortion
    )
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Noise_00"
    ,   element_name="Detail"
    ,   set_value=TX_Noise_00_Detail
    )
    # Mix
    bpy.data.materials[mtal_name].node_tree.nodes["Mix_RGB_00"].blend_type = 'OVERLAY'
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="Mix_RGB_00"
    ,   element_name="Factor"
    ,   set_value=Mix_RGB_00_Factor
    )
    # ----------------------------
    # 木目の質感を加える
    # ----------------------------
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeBump"
    ,   texture_node_name="Bump_00"
    ,   node_location=(200, -100)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Mix_RGB_00"
    ,   texture_node_name_in="Bump_00"
    ,   output_link="Result"
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
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="Bump_00"
    ,   element_name="Strength"
    ,   set_value=Bump_00_Strength
    )
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)


# =====================================================
# マテリアル 木素材 一枚板
# =====================================================
def mtal_wood_01(
    mtal_name="mtal_name"
,   Mapping_00_Scale=(1, 8.0, 1)
,   TX_Noise_00_Distortion=2.1
,   TX_Noise_00_Detail=13
,   Color_Ramp_00_color_0=(0.176,0.113,0.106,1)
,   Color_Ramp_00_color_1=(0.279,0.227,0.148,1)
,   Color_Ramp_00_position_0=0
,   Color_Ramp_00_position_1=1
,   Bump_00_Strength=0.15
):
    # Save : Curren Mode
    current_mode = bpy.context.object.mode
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeTexNoise"
    ,   texture_node_name="TX_Noise_00"
    ,   node_location=(-400, 200)
    )

    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeValToRGB"
    ,   texture_node_name="Color_Ramp_00"
    ,   node_location=(-300, 500)
    )

    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Noise_00"
    ,   texture_node_name_in="Color_Ramp_00"
    ,   output_link="Fac"
    ,   input_link="Fac"
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Color_Ramp_00"
    ,   texture_node_name_in="Principled BSDF"
    ,   output_link="Color"
    ,   input_link="Base Color"
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
    # 木目を付ける
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="Mapping_00"
    ,   element_name="Scale"
    ,   set_value=Mapping_00_Scale
    )
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Noise_00"
    ,   element_name="Distortion"
    ,   set_value=TX_Noise_00_Distortion
    )
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Noise_00"
    ,   element_name="Detail"
    ,   set_value=TX_Noise_00_Detail
    )
    # 色の変更
    # Color_Ramp 色変更
    mtal_cm_lib.node_color_ramp_setting(
        material_name=mtal_name
    ,   node_name="Color_Ramp_00"
    ,   color_0=Color_Ramp_00_color_0 #(0.176,0.113,0.106,1)
    ,   color_1=Color_Ramp_00_color_1 #(0.279,0.227,0.148,1)
    ,   position_0=Color_Ramp_00_position_0 # 0
    ,   position_1=Color_Ramp_00_position_1 # 1
    ,   interpolation="LINEAR"
    )
    # 木の質感表現
    # テクスチャ追加
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeBump"
    ,   texture_node_name="Bump_00"
    ,   node_location=(-200, 0)
    )
    # ノードのリンク
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="Color_Ramp_00"
    ,   texture_node_name_in="Bump_00"
    ,   output_link="Color"
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
    # ノード 値変更
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="Bump_00"
    ,   element_name="Strength"
    ,   set_value=Bump_00_Strength # 0.15
    )
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)
