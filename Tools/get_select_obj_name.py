import bpy
def get_selected_object_names():
    # 選択されているオブジェクト名をリストで取得して返す。
    # 表示時は '' や "" を付けずに出力する。
    selected_objects = bpy.context.selected_objects
    object_names = [obj.name for obj in selected_objects]

    # デバッグ用に表示（クォートなしで）
    print("--------------------------------------------------------------")
    if object_names:
        print("Selected Objects:", ", ".join(object_names))
    else:
        print("No objects selected.")
    print("--------------------------------------------------------------")

    return object_names

# 実行例
names = get_selected_object_names()