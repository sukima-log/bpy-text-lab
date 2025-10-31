import bpy

#-----------------------------------------------------
# 選択された頂点、エッジ、面のインデックスを取得して表示
#-----------------------------------------------------
def get_selected_elements():
    # アクティブオブジェクト取得
    obj = bpy.context.object

    if obj and obj.type == 'MESH':
        # メッシュデータ取得
        mesh = obj.data

        # Mode切り替え
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # 選択された頂点のインデックス取得
        selected_vertex_indices = [v.index for v in mesh.vertices if v.select]

        # 選択されたエッジのインデックス取得
        selected_edge_indices = [e.index for e in mesh.edges if e.select]

        # 選択された面のインデックス取得
        selected_face_indices = [f.index for f in mesh.polygons if f.select]

        # 選択された頂点、エッジ、面のインデックス表示
        print("--------------------------------------------------------------")
        print("Selected Vertex Indices:", selected_vertex_indices)
        print("--------------------------------------------------------------")
        print("Selected Edge Indices:", selected_edge_indices)
        print("--------------------------------------------------------------")
        print("Selected Face Indices:", selected_face_indices)

        # 選択されていない場合のメッセージ
        if not selected_vertex_indices and not selected_edge_indices and not selected_face_indices:
            print("No vertices, edges, or faces selected.")
    else:
        print("No mesh object selected.")

# 実行
get_selected_elements()