import bpy, os, sys, subprocess
# スクリプトディレクトリ（Text Editorのファイルパス基準）
script_path = bpy.path.abspath(bpy.context.space_data.text.filepath)
script_dir = os.path.dirname(script_path)
# Gitルート取得
git_root = subprocess.run(
    ["git", "-C", script_dir, "rev-parse", "--show-toplevel"],
    stdout=subprocess.PIPE, text=True
).stdout.strip()
# ルートの1つ上をsys.pathへ
if git_root and git_root not in sys.path:
    sys.path.append(git_root)
# 共通設定
from Common.common_top import *
#========================================================================================


# ========================================================================
# = ▼ Select Active Object
# ========================================================================
def active_object_select(object_name_list=[]):
    # 指定されたオブジェクトを選択し、最後に見つかったオブジェクトをアクティブにする
    # アクティブオブジェクトが存在しなくても安全に動作
    # Save current mode safely
    current_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'

    # Ensure OBJECT mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    active_obj = None
    for obj_name in object_name_list:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.select_set(True)
            active_obj = obj  # 最後に見つかったオブジェクトを保存

    # Set the last found object as active
    if active_obj:
        bpy.context.view_layer.objects.active = active_obj

    # Restore previous mode
    if bpy.context.object and bpy.context.object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass

    return active_obj

# ========================================================================
# = ▼ Select Active Object recursively hierarchy 再帰的 親子関係選択
# ========================================================================
def active_object_select_recursively(object_name_list=[]):
    # Select objects by name.
    # - If an object has children, select it and all its hierarchy.
    # - If no children, select only itself.
    # Returns the last active object.
    def select_hierarchy(obj):
        # Recursively select object and its children
        obj.select_set(True)
        for child in obj.children:
            select_hierarchy(child)

    # Save current mode (if object exists)
    current_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'

    # Ensure OBJECT mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all first
    bpy.ops.object.select_all(action='DESELECT')

    myobject = None
    for object_name in object_name_list:
        myobject = bpy.data.objects.get(object_name)
        if myobject:
            if myobject.children:  
                # Has children → select full hierarchy
                select_hierarchy(myobject)
            else:
                # No children → select only itself
                myobject.select_set(True)

            # Set active to the object itself (not child)
            bpy.context.view_layer.objects.active = myobject

    # Restore previous mode if the active object is not Empty
    if bpy.context.active_object and bpy.context.active_object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass

    return myobject

# ========================================================================
# = ▼ Rename Object at key word (recursively/hierarchy) 再帰的 親子関係選択
# ========================================================================
def rename_hierarchy_recursively(base_name: str, new_base_name: str):
    # Rename duplicated objects after bpy.ops.object.duplicate_move().
    # - Replace base_name with new_base_name
    # - Remove Blender's auto suffix (.001, .002...)
    for obj in bpy.context.selected_objects:
        if obj.name.startswith(base_name):
            # サフィックスを取り除き、置換
            clean_name = obj.name.split(".")[0]  
            new_name = clean_name.replace(base_name, new_base_name)
            obj.name = new_name


# ========================================================================
# = ▼ 辺、面、頂点 選択
# ========================================================================
def element_select(
        element_list                # 要素 Index List
,       select_mode                 # Mode（VERT/EDGE/FACE）
,       object_name_list=["NaN"]    # Object Name List
,       loop_select=False           # Loop選択
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Ensure OBJECT mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    # Deselect all first
    bpy.ops.object.select_all(action='DESELECT')
    if (object_name_list[0] != "NaN"):
        # Current Active Object
        for i in range(len(object_name_list)):
            object_name = object_name_list[i]
            obj = bpy.data.objects.get(object_name)
            if obj:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
    # Get Active Object
    obj = bpy.context.object
    # Check Mesh
    if obj and obj.type == 'MESH':
        mesh = obj.data
        # Change Mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type=select_mode)
        # Release Select Index
        bpy.ops.mesh.select_all(action='DESELECT')
        # Change Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # Select Element
        if ((len(element_list) >= 1) and (element_list[0] == "all")):
            # Select All
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type=select_mode)
            bpy.ops.mesh.select_all(action='SELECT')
        else:
            # Select Element
            for i in range(len(element_list)):
                target_ele_index = element_list[i]
                if (select_mode == "FACE"):
                    mesh.polygons[target_ele_index].select = True
                elif (select_mode == "EDGE"):
                    mesh.edges[target_ele_index].select = True
                elif (select_mode == "VERT"):
                    mesh.vertices[target_ele_index].select = True
        # Change Mode
        bpy.ops.object.mode_set(mode='EDIT')
        if (loop_select == True):
            # Loop Select (Alt+Click)
            bpy.ops.mesh.loop_multi_select(ring=False)
    else:
        print("No mesh object selected.")
    # Return Mode
    bpy.ops.object.mode_set(mode=current_mode)

# ========================================================================
# 辺、面、頂点選択解除
# ========================================================================
def element_deselect(
        object_name_list    # Object Name List
    ,   element_list        # Index List
    ,   select_mode         # Mode  ("VERT", "EDGE", "FACE")
):
    if not object_name_list or not object_name_list[0]:
        print("Invalid object_name_list.")
        return
    obj = bpy.data.objects.get(object_name_list[0])
    if not obj or obj.type != 'MESH':
        print(f"{object_name_list[0]} is not a valid mesh object.")
        return
    bpy.context.view_layer.objects.active = obj
    # Change Mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Get BMesh
    bm = bmesh.from_edit_mesh(obj.data)
    # Update Index Table
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    # Release
    if select_mode == "VERT":
        for index in element_list:
            if 0 <= index < len(bm.verts):
                bm.verts[index].select = False
    elif select_mode == "EDGE":
        for index in element_list:
            if 0 <= index < len(bm.edges):
                bm.edges[index].select = False
    elif select_mode == "FACE":
        for index in element_list:
            if 0 <= index < len(bm.faces):
                bm.faces[index].select = False
    else:
        print(f"Invalid select_mode: {select_mode}")
        return
    # Update Mesh & Update
    bmesh.update_edit_mesh(obj.data, loop_triangles=True)



# ========================================================================
# 視点をZ視点真上に変更
# ========================================================================
def set_view_custom_position(
    point=(0, 0, 0)
,   rotate=(0, 0, 0)
,   distance=3
):
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    region_3d = space.region_3d
                    region_3d.view_perspective = 'ORTHO' # 'PERSP'/'CAMERA'
                    # 視点位置/向き設定
                    region_3d.view_location = mathutils.Vector(point)                   # 位置
                    region_3d.view_distance = distance                                  # 距離
                    region_3d.view_rotation = mathutils.Euler(rotate).to_quaternion()   # 回転
                    # View更新
                    bpy.context.view_layer.update()

# ========================================================================
# = ▼ オブジェクトの表示/非表示
# ========================================================================
def hide_obj_tgl(
    object_list=[]
,   key=False
):
    for i in range(len(object_list)):
        obj = bpy.data.objects.get(object_list[i])
        obj.hide_set(key)


# ========================================================================
# = ▼ プレビュー切り替え
# ========================================================================
def change_preview(key='SOLID'):
    # 'SOLID'       : ソリッドプレビュー
    # 'MATERIAL'    : マテリアルプレビュー
    # 'RENDERED'    : レンダープレビュー
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = key
                    return


# ========================================================================
# = ▼ オブジェクト/メッシュ回転
# ========================================================================
def object_rotate_func(
        object_list=["mesh"]                        # 回転対象 Object List
    ,   transform_pivot_point='INDIVIDUAL_ORIGINS'  # 回転中心 (ピボットポイント)
    ,   radians_num=0                               # 回転角度 (度)
    ,   orient_axis="Z"                             # 回転軸
    ,   orient_type="GLOBAL"                        # 回転軸座標
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Check Mesh
    if (object_list[0] != "mesh"):
        # Change Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # Release All Object
        bpy.ops.object.select_all(action='DESELECT')
        # Select Active Object
        my_active_element = active_object_select(object_name_list=object_list)
        # オブジェクトのオリジンをジオメトリの中心に移動
        # オブジェクト中心(回転の中心)をオブジェクトに追従させる
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    # Set Pivot point
    #-------------------------------------------------
    # Options
    # bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'        # オブジェクトの中点（複数オブジェクトの中心）
    # bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'      # アクティブなオブジェクトの中心
    # bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'              # 3Dカーソル位置
    # bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'  # 個々のオブジェクトの中心
    # bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER' # バウンディングボックスと呼ばれる枠の中心
    #-------------------------------------------------
    bpy.context.scene.tool_settings.transform_pivot_point = transform_pivot_point
    # Rotate Object
    bpy.ops.transform.rotate(
        value=math.radians(radians_num)
    ,   orient_axis=orient_axis
    ,   orient_type=orient_type
    )
    # Change Original Mode
    if bpy.context.active_object and bpy.context.active_object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass


# ========================================================================
# = ▼ 面押し出し インデックス固定
# ========================================================================
def fix_index_extrude_region(
    vert_idx_list=[0,1,2,3]     # Index List
,   mv_value=(-5,0,0)           # Move Value
,   object_name="obj_name"      # Active Object Name
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    # Get Number of Angles (角数)
    li_len = len(vert_idx_list)
    # Save Data
    ei_a=[] # Extrude Index
    # Vert Extrude
    for i in range(li_len):
        # Select Element
        element_select(
            element_list=[vert_idx_list[i]]
        ,   select_mode="VERT"
        ,   object_name_list=[object_name]
        )
        # 押し出し、引き込み
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={
            }, 
            TRANSFORM_OT_translate={
                "value":mv_value
            ,   "orient_type":'GLOBAL'
        })
        # Select Add Vertex Index (追加された頂点 選択)
        new_vertex_index = len(bpy.context.object.data.vertices) - 1
        bpy.context.object.data.vertices[new_vertex_index].select = True
        # Update Mesh
        bpy.context.view_layer.objects.active = bpy.context.object
        # Change Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        # Get Active Object
        obj = bpy.context.object
        # Get Mesh Data
        mesh = obj.data
        # Get the index of the selected vertex
        selected_vertex_indices = [v.index for v in mesh.vertices if v.select]
        # Add List
        ei_a.append(selected_vertex_indices[0])
    # Add Face
    for i in range(li_len-1):
        element_select(
            element_list=[vert_idx_list[i], ei_a[i], vert_idx_list[i+1], ei_a[i+1]]
        ,   select_mode="VERT"
        ,   object_name_list=[object_name]
        )
        # 面 追加・埋める・貼る (F)
        bpy.ops.mesh.edge_face_add()
    # Add Face
    element_select(
        element_list=[vert_idx_list[0], ei_a[0], vert_idx_list[li_len-1], ei_a[li_len-1]]
    ,   select_mode="VERT"
    ,   object_name_list=[object_name]
    )
    # Add Face (面 追加・埋める・貼る) (F)
    bpy.ops.mesh.edge_face_add()
    # Add Face
    element_select(
        element_list=ei_a
    ,   select_mode="VERT"
    ,   object_name_list=[object_name]
    )
    # Add Face (面 追加・埋める・貼る) (F)
    bpy.ops.mesh.edge_face_add()
    # Delete Face
    element_select(
        element_list=vert_idx_list
    ,   select_mode="VERT"
    ,   object_name_list=[object_name]
    )
    bpy.ops.mesh.delete(type='FACE')
    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)

# ========================================================================
# = ▼ 面押し出し インデックス固定 円系
# ========================================================================
def fix_index_extrude_region_move(
    obj_name="obj_name"         # Object Name
,   represent_edge=0            # Represent Edge Index (代表エッジ)
,   resize_values=(1, 1, 1)     # Change Size Value
,   move_values=(0, 0, 0)       # Move Value
,   face_add_flag=True          # If True: Add Face
,   loop_flag=True              # ?
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    # Select Element
    element_select(
        element_list=[represent_edge]
    ,   select_mode="EDGE"
    ,   object_name_list=[obj_name]
    )
    if (loop_flag):
        # エッジループ 選択 ループ選択(Alt+Click)
        bpy.ops.mesh.loop_multi_select(ring=False)
    # Change Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    # Get Mesh Data
    mesh = bpy.context.object.data
    # Get the index of the selected vertex
    selected_vertex_indices = [v.index for v in mesh.vertices if v.select]
    # Change Mode
    bpy.ops.object.mode_set(mode='EDIT')
    tmp_l=[]
    for i in range(len(selected_vertex_indices)):
        # Select Element
        element_select(
            element_list=[selected_vertex_indices[i]]
        ,   select_mode="VERT"
        ,   object_name_list=[obj_name]
        )
        # Create Face (面の作成 外/内側へ拡大(押し込み(押し出し)引き込み/差し込み))
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={}, 
            TRANSFORM_OT_translate={
            }
        )
        # Change Mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')
        # Get Mesh Data
        mesh = bpy.context.object.data
        # Get the index of the selected vertex
        tmp_l.append([v.index for v in mesh.vertices if v.select][0])
        # Change Mode
        bpy.ops.object.mode_set(mode='EDIT')
    # Select Element
    element_select(
        element_list=tmp_l
    ,   select_mode="VERT"
    ,   object_name_list=[obj_name]
    )
    # Change Size
    bpy.ops.transform.resize(
        value=resize_values
    ,   orient_type='GLOBAL'
    )
    # Move Object/Element
    bpy.ops.transform.translate(
        value=move_values
    ,   orient_type='GLOBAL'
    )
    # Add Face
    if (face_add_flag):
        for i in range(1, len(tmp_l)):
            # Select Element
            element_select(
                element_list=[tmp_l[i], selected_vertex_indices[i], tmp_l[i-1], selected_vertex_indices[i-1]]
            ,   select_mode="VERT"
            ,   object_name_list=[obj_name]
            )
            # Add Face (面 追加・埋める・貼る) (F)
            bpy.ops.mesh.edge_face_add()
        if (loop_flag):
            # Connect First and Last Point (最初と最後部分をつなぐ)
            element_select(
                element_list=[tmp_l[0], selected_vertex_indices[0], tmp_l[len(tmp_l)-1], selected_vertex_indices[len(tmp_l)-1]]
            ,   select_mode="VERT"
            ,   object_name_list=[obj_name]
            )
            # Add Face (面 追加・埋める・貼る) (F)
            bpy.ops.mesh.edge_face_add()
    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)


# ========================================================================
# = ▼ 筒状 面指定 面貼り インデックス固定
# ========================================================================
def fix_index_connect_vert(
    vert_list_1=[0,1,2,3]       # Vertex Index 1
,   vert_list_2=[0,1,2,3]       # Vertex Index 2
,   object_name="object_name"   # Object Name
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    # Delete Face
    element_select(
        element_list=vert_list_1
    ,   select_mode="VERT"
    ,   object_name_list=[object_name]
    )
    bpy.ops.mesh.delete(type='FACE')
    element_select(
        element_list=vert_list_2
    ,   select_mode="VERT"
    ,   object_name_list=[object_name]
    )
    bpy.ops.mesh.delete(type='FACE')
    # Add Face
    for i in range(len(vert_list_1)-1):
        element_select(
            element_list=[vert_list_1[i], vert_list_2[i], vert_list_1[i+1], vert_list_2[i+1]]
        ,   select_mode="VERT"
        ,   object_name_list=[object_name]
        )
        # Add Face (面 追加・埋める・貼る) (F)
        bpy.ops.mesh.edge_face_add()
    # Add Face
    element_select(
        element_list=[vert_list_1[0], vert_list_2[0], vert_list_1[-1], vert_list_2[-1]]
    ,   select_mode="VERT"
    ,   object_name_list=[object_name]
    )
    # Add Face (面 追加・埋める・貼る) (F)
    bpy.ops.mesh.edge_face_add()
    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)

# ========================================================================
# = ▼ ループカット 数値指定 複数
# ========================================================================
def multi_value_loopcut_slide(
    bl=20                                                               # Target Edge Size
,   i_a=[0]                                                             # Index List
,   s_a=[0]                                                             # Slide Value List
,   d_a=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,]    # direction List (1 or -1)
):
    bl_tmp = bl
    for i in range(len(i_a)):
        # Calculation Ration (割合)
        ratio = bl_tmp / bl
        # Calculation Move Point (移動位置計算)
        value = ((1/((bl*ratio)/2)) * s_a[i]) - 1
        # Calculation Update Value更新
        bl_tmp = bl - (bl - s_a[i])
        # Loop Cut
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut={
                "number_cuts":1             # 追加ループ数
            ,   "smoothness":0              # 0~1：スムージング強さ
            ,   "falloff":'INVERSE_SQUARE'  # カット減衰 "INVERSE_SQUARE":逆2乗フォールオフ（例：SHARP）
            ,   "object_index":0            # オブジェクトインデックス(通常0：最初のオブジェクト)
            ,   "edge_index":i_a[i]         # エッジインデックス
            }
        ,   TRANSFORM_OT_edge_slide={
                "value":value*d_a[i]        # スライド位置（0:スライドなし） 
            ,   "single_side":False         # 片側スライド（False:両側スライド）
            ,   "use_even":False            # スライド均等（False:均等にしない）
            }
        )


# ========================================================================
# = ▼ 指定頂点 絶対座標取得
# ========================================================================
def get_vert_point(vert_index=0):
    obj = bpy.context.active_object
    if not obj or obj.type != 'MESH':
        print("メッシュオブジェクトが選択されていません。")
        return None
    # Save Current Mode
    current_mode = obj.mode
    # Chaneg Mode
    if current_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    # Index Check
    if vert_index < 0 or vert_index >= len(obj.data.vertices):
        print(f"頂点インデックス {vert_index} は存在しません")
        if current_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=current_mode)
        return None
    # Local coordinate -> World coordinate (指定インデックスのローカル座標を取得し、ワールド座標に変換)
    v = obj.data.vertices[vert_index]
    world_co = obj.matrix_world @ v.co
    point_list = [round(world_co.x, 7), round(world_co.y, 7), round(world_co.z, 7)]
    # Change Original Mode
    if bpy.context.active_object and bpy.context.active_object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass
    return point_list


# ========================================================================
# = ▼ 指定したオブジェクト頂点間 距離取得
# ========================================================================
def point_diff_length(
    obj1_name="obj1_name"   # オブジェクト名またはEmpty名
,   obj1_point=0            # Vert Index（メッシュの場合のみ使用）
,   obj2_name="obj2_name"   # オブジェクト名またはEmpty名
,   obj2_point=0            # Vert Index（メッシュの場合のみ使用）
,   coordinate="X"          # X, Y, Z
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    # Save: Get Current Active Object
    current_obj = bpy.context.object
    # -------------------------
    # Get Point (OBJ1)
    # -------------------------
    obj1 = bpy.data.objects[obj1_name]
    if obj1.type == 'MESH':
        active_object_select([obj1_name])
        point1 = get_vert_point(vert_index=obj1_point)
    else:
        # Emptyやカメラなど → オブジェクト原点を使用
        point1 = obj1.matrix_world.translatio
    # -------------------------
    # Get Point (OBJ2)
    # -------------------------
    obj2 = bpy.data.objects[obj2_name]
    if obj2.type == 'MESH':
        active_object_select([obj2_name])
        point2 = get_vert_point(vert_index=obj2_point)
    else:
        point2 = obj2.matrix_world.translation
    # -------------------------
    # Get Diff Length
    # -------------------------
    coord_idx = {"X": 0, "Y": 1, "Z": 2}
    if coordinate not in coord_idx:
        print("Error: coordinate must be X, Y, or Z")
        return None
    axis = coord_idx[coordinate]
    diff_length = abs(point1[axis] - point2[axis])
    # -------------------------
    # Return Status
    # -------------------------
    bpy.ops.object.select_all(action='DESELECT')
    current_obj.select_set(True)
    bpy.context.view_layer.objects.active = current_obj
    # Return Mode
    if bpy.context.active_object and bpy.context.active_object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass

    return diff_length



# ========================================================================
# = ▼ ベジェ曲線/ベジエ曲線のハンドル/コントロールポイント選択
# ========================================================================
def bezier_point_select(
    element_list                 # Point or Handle List
,   select_mode='CONTROL_POINT'  # Mode（CONTROL_POINT/HANDLE_LEFT/HANDLE_RIGHT）
,   object_name_list=["NaN"]     # Object Name
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    if object_name_list[0] != "NaN":
        for object_name in object_name_list:
            # Select Current Active Object
            obj = bpy.data.objects.get(object_name)
            if obj:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
    # Get Active Object
    obj = bpy.context.object
    # Check Curve Object
    if obj and obj.type == 'CURVE':
        # Change Mode
        bpy.ops.object.mode_set(mode='EDIT')
        # Get Object Data
        curve = obj.data
        # Release Point
        for spline in curve.splines:
            if spline.type == 'BEZIER':
                for bezier_point in spline.bezier_points:
                    bezier_point.select_control_point = False
                    bezier_point.select_left_handle = False
                    bezier_point.select_right_handle = False
        # Select Point or Handle
        for idx in element_list:
            for spline in curve.splines:
                if spline.type == 'BEZIER':
                    if idx < len(spline.bezier_points):
                        bezier_point = spline.bezier_points[idx]
                        if select_mode == 'CONTROL_POINT':
                            bezier_point.select_control_point = True
                        elif select_mode == 'HANDLE_LEFT':
                            bezier_point.select_left_handle = True
                        elif select_mode == 'HANDLE_RIGHT':
                            bezier_point.select_right_handle = True
        # Change Mode
        bpy.ops.object.mode_set(mode='EDIT')
    else:
        print("No curve object selected.")
    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)



# ========================================================================
# = ▼ 長方形 オブジェクト頂点移動
# ========================================================================
def make_cube_move_relative_position(
    cube_name="default_name"                    # Object Name
,   cube_size=(0.1, 0.1, 1.0)                   # Object Size
,   cube_vert=6                                 # Vert Index
,   destination_obj_name="destination_obj_name" # Base Object Name
,   destination_vert=0                          # Vert Index
):
    # Save: Current Mode
    current_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    # Release Select
    bpy.ops.object.select_all(action='DESELECT')
    # Add Cube
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    cube_obj = bpy.context.object
    cube_obj.name = cube_name
    # Change Size
    bpy.ops.transform.resize(value=cube_size, orient_type='GLOBAL')
    bpy.ops.object.transform_apply(scale=True)  # スケール適用（頂点座標に反映）
    # Get Destination Object
    des_obj = bpy.data.objects.get(destination_obj_name)
    if not des_obj:
        print(f"Object '{destination_obj_name}' not found.")
        return
    # Get World coordinate (ワールド座標取得)
    des_vert = des_obj.data.vertices[destination_vert]
    des_world_co = des_obj.matrix_world @ des_vert.co
    cube_vert_co = cube_obj.data.vertices[cube_vert].co
    cube_world_co = cube_obj.matrix_world @ cube_vert_co
    # 相対移動量
    dx = des_world_co.x - cube_world_co.x
    dy = des_world_co.y - cube_world_co.y
    dz = des_world_co.z - cube_world_co.z
    # 編集モードに入って頂点移動
    bpy.context.view_layer.objects.active = cube_obj
    cube_obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(cube_obj.data)
    for v in bm.verts:
        v.co.x += dx
        v.co.y += dy
        v.co.z += dz
    bmesh.update_edit_mesh(cube_obj.data)

    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)

# ========================================================================
# = ▼ オブジェクトの位置, サイズ, 回転, 中心点初期化(全適用)
# ========================================================================
def initialize_transform_apply(
    object_name_list=[] # object_name_list
):
    # Change List
    if not isinstance(object_name_list, list):
        object_name_list = [object_name_list]
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    # Activate Object
    active_object_select(
        object_name_list=object_name_list
    )
    # All Transforms（全トランスフォーム）(適用)
    bpy.ops.object.transform_apply(
        location=True   # 位置適用、現在の位置が新しい基準点(原点)
    ,   rotation=True   # 回転適用、現在の回転が新しい基準点(0度)
    ,   scale=True      # スケール適用、現在のスケールが新しい基準点(1.0)
    )
    # 0度ローテーション -> オブジェクトの原点を中心に移動
    object_rotate_func(
        object_list=object_name_list
    ,   radians_num=0
    )
    # Change Original Mode
    # Return Mode
    if bpy.context.active_object and bpy.context.active_object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass


# ========================================================================
# = ▼ 左半分の頂点を全て選択
# ========================================================================
def select_left_half_vertices(obj_name):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    obj = bpy.data.objects[obj_name]
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    active_object_select(
        object_name_list=obj_name
    )
    bpy.ops.object.mode_set(mode='EDIT')
    # Release All Vertex
    bpy.ops.mesh.select_all(action='DESELECT')
    # Change Mode
    bpy.ops.mesh.select_mode(type='VERT')
    # Get Vertex Point
    bm = bmesh.from_edit_mesh(obj.data)
    for vert in bm.verts:
        if vert.co.x < -0.00001:    # 調整
            vert.select = True
    # Update
    bmesh.update_edit_mesh(obj.data)
    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)



# ========================================================================
# オブジェクトに以下のクリーンアップを実行
# ・大きさ０を融解：面積が０の面を削除し、１つの頂点にまとめる
# ・孤立を削除：どの面にもつながっていない辺や頂点を削除する
# ・重複頂点を削除：重複している頂点を１つの頂点にまとめる
# 引数   arg_objectname：指定オブジェクト名
# ========================================================================
def cleanup_mesh_object():
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    # 頂点をSelect Allした状態とする
    bpy.ops.mesh.select_all(action='SELECT') 
    # 大きさ0を融解（結合距離 0.0001）
    bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)
    # 変更を反映するため再び頂点をSelect All
    bpy.ops.mesh.select_all(action='SELECT') 
    # 孤立を削除（頂点、辺のみ）
    bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)
    # 孤立を削除でSelect Allが解除されるので再び頂点をSelect All
    bpy.ops.mesh.select_all() 
    # 重複頂点を削除（結合距離 0.0001、非選択部の結合無効）
    bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)
    # オブジェクトモードに移行する
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    # Change Original Mode
    # Return Mode
    if bpy.context.active_object and bpy.context.active_object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass
    return




# ========================================================================
# = 選択頂点どうしをつなぐ辺を追加
# ========================================================================
def add_edge_between_vert(
    obj_name="obj_name"
,   index_list=[[1,0], [2,3]]
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Get Object
    obj = bpy.data.objects.get(obj_name)
    if obj is None:
        raise ValueError(f"オブジェクト '{obj_name}' が見つかりません。")
    if obj.type != 'MESH':
        raise ValueError(f"オブジェクト '{obj_name}' はメッシュではありません。")
    # Change Mode
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    mesh = obj.data
    # Get Edge List
    existing_edges = set(tuple(sorted(e.vertices)) for e in mesh.edges)
    # New Edge List
    new_edges = []
    for pair in index_list:
        # Index Check
        if pair[0] >= len(mesh.vertices) or pair[1] >= len(mesh.vertices):
            print(f"エラー: インデックス {pair} が範囲外です。")
            continue
        # Sort Check
        edge_key = tuple(sorted(pair))
        if edge_key not in existing_edges:
            new_edges.append(pair)
        else:
            print(f"頂点 {pair[0]} と {pair[1]} は既に辺で結ばれています。")
    # Add Edge
    if new_edges:
        mesh.edges.add(len(new_edges))
        for i, edge in enumerate(new_edges):
            mesh.edges[-len(new_edges) + i].vertices = edge
    else:
        print("新しい辺は追加されませんでした。")
    # Update Mesh Data
    mesh.update()
    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)


# ========================================================================
# = 辺を削除して面を統合
# ========================================================================
def dissolve_edges(
    obj_name=None       # Object Name
,   index_list=[]       # Delete Index
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    element_select(
        element_list=index_list
    ,   select_mode="EDGE"
    ,   object_name_list=[obj_name]
    )
    # Change Mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Dissolve Edge and Merge Face
    bpy.ops.mesh.dissolve_edges()
    # Change Original Mode
    bpy.ops.object.mode_set(mode=current_mode)


# ========================================================================
# 頂点間の相対距離を求める
# ========================================================================
def get_relative_distance():
    # Get Active Object
    obj = bpy.context.active_object
    if obj is None or obj.type != 'MESH':
        print("エラー: アクティブなメッシュオブジェクトがありません。")
        return
    # Change Mode
    if bpy.context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')
    # Get BMesh
    bm = bmesh.from_edit_mesh(obj.data)
    # Get Select Vertex Point
    selected_verts = [v for v in bm.verts if v.select]
    if len(selected_verts) != 2:
        print("エラー: 2つの頂点を選択してください。")
        return
    # Get Vertex coordinate
    co1 = selected_verts[1].co
    co2 = selected_verts[0].co
    # Calucurate Distance
    dx = co2.x - co1.x
    dy = co2.y - co1.y
    dz = co2.z - co1.z
    # Output
    print("")
    print(f"X方向の相対距離: {dx}")
    print(f"Y方向の相対距離: {dy}")
    print(f"Z方向の相対距離: {dz}")
    return dx, dy, dz


# ========================================================================
# アンカー用 Emptyの追加 結びつけ
# ========================================================================
def add_object_anchor_empty(
    obj_name="obj_name"
,   location=(0,0,0)
,   suffix="_anchor"
):
    # Save Current Mode
    current_mode = bpy.context.object.mode
    # Change Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    # ============================
    # Add Base Empty
    # ============================
    empty_name = obj_name + suffix
    empty = bpy.data.objects.new(empty_name, None)
    bpy.context.collection.objects.link(empty)
    empty.location = location
    # Parent-Child 親子付け（Emptyを親とする）
    active_object_select(object_name_list=[obj_name])
    bpy.context.object.parent = empty
    active_object_select(object_name_list=[obj_name])
    # Change Original Mode
    if bpy.context.active_object and bpy.context.active_object.type != 'EMPTY':
        try:
            bpy.ops.object.mode_set(mode=current_mode)
        except RuntimeError:
            pass


# ========================================================================
#  既存のEmptyに既存のオブジェクトを追加して親子関係を設定する
#  （元の親がEmptyで子がいなくなった場合は自動削除）
# ========================================================================
def add_objects_to_existing_empty(empty_name, obj_name_list):
    target_empty = bpy.data.objects.get(empty_name)
    if not target_empty:
        return

    # Switch to OBJECT mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    for obj_name in obj_name_list:
        obj = bpy.data.objects.get(obj_name)
        if not obj:
            continue

        # Clear previous parent if exists
        if obj.parent:
            prev_parent = obj.parent
            obj.parent = None
            # Delete Empty if it has no children left
            if prev_parent.type == 'EMPTY' and len(prev_parent.children) == 0:
                bpy.data.objects.remove(prev_parent)

        # Select the object to be parented
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)

        # Activate the target Empty as parent
        target_empty.select_set(True)
        bpy.context.view_layer.objects.active = target_empty

        # Set parent while keeping transforms
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
    

# ========================================================================
# 1. オブジェクトをまとめる処理（親子関係にする）
# ========================================================================
def group_objects_under_base(base_name: str, object_name_list: list[str]) -> dict:
    # 指定したオブジェクトをベースオブジェクトの子にまとめる。
    # まとめる前の親子関係を辞書で返す。
    base_obj = bpy.data.objects.get(base_name)
    if not base_obj:
        print(f"Base object '{base_name}' not found.")
        return {}

    # Change Object Mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    base_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_obj

    # 元の親子関係を記録
    original_parent_map = {}

    for name in object_name_list:
        obj = bpy.data.objects.get(name)
        if obj and obj != base_obj:
            original_parent_map[obj.name] = obj.parent.name if obj.parent else None
            obj.select_set(True)

    # 親子付け（ワールド座標を維持）
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    return original_parent_map


# ========================================================================
# 2. オブジェクトを元の親子関係に戻す処理
# ========================================================================
def ungroup_objects(original_parent_map: dict):
    # group_objects_under_base() 前の親子関係に戻す。
    if not original_parent_map:
        print("No original parent map provided.")
        return

    # Ensure OBJECT mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    for obj_name, parent_name in original_parent_map.items():
        obj = bpy.data.objects.get(obj_name)
        if not obj:
            continue

        if parent_name:
            parent_obj = bpy.data.objects.get(parent_name)
            if parent_obj:
                # 元の位置を保つために parent_set を使う
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = parent_obj
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        else:
            # 親を解除（見た目の位置を保つ）
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

