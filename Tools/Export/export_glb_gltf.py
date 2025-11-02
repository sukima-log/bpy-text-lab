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


def prepare_for_export():
    """Ensure all transforms, modifiers, and visibility are correct before GLTF/GLB export."""
    bpy.ops.object.mode_set(mode='OBJECT')

    # 1. 全オブジェクトのトランスフォームを適用
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # 2. Armature 以外のモディファイアを適用（確実にシェイプキーを出力するため）
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type != 'ARMATURE':
                    try:
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                    except Exception as e:
                        print(f"Failed to apply modifier: {mod.name} on {obj.name} -> {e}")

    # ==========================
    # 3. 複数マテリアルのメッシュを結合
    # ==========================
    # すべてのメッシュを選択
    for obj in bpy.context.scene.objects:
        obj.select_set(False)  # 選択を一旦クリア

    mesh_objs = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if mesh_objs:
        for obj in mesh_objs:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = mesh_objs[0]
        bpy.ops.object.join()  # 結合
        
    # 3. 非表示オブジェクトを全て表示（use_visible=True を有効にする前提）
    for obj in bpy.context.scene.objects:
        obj.hide_set(False)
        obj.hide_render = False

    # 4. シェイプキー確認・有効化
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj.data.shape_keys:
            for key_block in obj.data.shape_keys.key_blocks:
                key_block.mute = False  # すべて有効化
                key_block.value = 0.0   # 初期値は 0 にしておく

    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            if obj.data.shape_keys:
                print(obj.name, [k.name for k in obj.data.shape_keys.key_blocks])
            else:
                print(obj.name, "No shape keys")



def export_model(filepath, export_format='GLB'):
    prepare_for_export()

    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format=export_format,     # 'GLB' or 'GLTF_SEPARATE'
        export_apply=False,              # Apply modifiers
        export_skins=True,               # Armature
        export_animations=True,          # Include animations
        export_morph=True,               # ← export_shape_keys 代替
        export_morph_normal=True,        # Include normals for morph targets
        export_morph_tangent=True,       # Include tangents for morph targets
        export_materials='EXPORT',       # Include materials
        export_yup=True,                 # Y-up coordinate system
        use_selection=False,             # Export all visible
        use_visible=True,                # Only visible objects
        export_texcoords=True,
        export_normals=True,
        export_tangents=True,
        # export_colors=True, ← 削除
        export_lights=False,             # Usually lights not needed
        export_cameras=False,            # Usually cameras not needed
        export_current_frame=False,      # Export full animation, not current frame only
        will_save_settings=False
    )

    print(f"[OK] Export completed: {filepath}")


# === 実行例 ===
output_directory = os.path.join(bpy.path.abspath(git_root + "/Output"), "exports")
os.makedirs(output_directory, exist_ok=True)

# GLBファイル出力
glb_filepath = os.path.join(output_directory, "my_model.glb")
export_model(glb_filepath, export_format='GLB')

# 分離GLTF出力したい場合
#gltf_filepath = os.path.join(output_directory, "my_model.gltf")
#export_model(gltf_filepath, export_format='GLTF_SEPARATE')