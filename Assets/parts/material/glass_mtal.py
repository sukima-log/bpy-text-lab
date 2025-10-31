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


# ==================================================================
# ▼ マテリアル
# ==================================================================
def mtal_glass_00(
    mtal_name="base_material"       # Materila Name
,   mix_shader_name="TX_Mix_Shader_00"  # Shader Name
,   base_position=-200                  # Node Position
,   IOR=1.45                            # 屈折の調整(硝子1.4~1.6)
,   Roughness=0.1                       # 粗さ
):
    # Save : Curren Mode
    current_mode = bpy.context.object.mode
    # Add Mix Shader (Mix)
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeMixShader"
    ,   texture_node_name=mix_shader_name
    ,   node_location=(base_position, -100)
    )
    base_position = base_position - 200
    # Add Glass BSDF (硝子)
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeBsdfGlass"
    ,   texture_node_name="TX_Glass_Bsdf_00"
    ,   node_location=(base_position, -100)
    )
    # Add Trasparent BSDF (透過)
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeBsdfTransparent"
    ,   texture_node_name="TX_Transparent_Bsdf_00"
    ,   node_location=(base_position, 0)
    )
    # Add Fresnel (フレネル)
    mtal_cm_lib.add_new_texture(
        material_name=mtal_name
    ,   texture_name="ShaderNodeFresnel"
    ,   texture_node_name="TX_Fresnel_00"
    ,   node_location=(base_position, 100)
    )
    # --------------------
    # - Connect
    # --------------------
    # Link Node
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Fresnel_00"
    ,   texture_node_name_in=mix_shader_name
    ,   output_link="Fac"
    ,   input_link="Fac"
    )
    # Link Node
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Transparent_Bsdf_00"
    ,   texture_node_name_in=mix_shader_name
    ,   output_link="BSDF"
    ,   input_link=1    # Shader[1]
    )
    # Link Node
    mtal_cm_lib.node_link_func(
        material_name=mtal_name
    ,   texture_node_name_out="TX_Glass_Bsdf_00"
    ,   texture_node_name_in=mix_shader_name
    ,   output_link="BSDF"
    ,   input_link=2    # Shader[2]
    )

    # Change Node Value
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Fresnel_00"
    ,   element_name="IOR"
    ,   set_value=IOR
    )
    # Change Node Value
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Glass_Bsdf_00"
    ,   element_name="IOR"
    ,   set_value=IOR
    )
    # Change Node Value
    mtal_cm_lib.node_value_change(
        material_name=mtal_name
    ,   node_name="TX_Glass_Bsdf_00"
    ,   element_name="Roughness"
    ,   set_value=Roughness
    )
    # Change Origin Mode
    bpy.ops.object.mode_set(mode=current_mode)

