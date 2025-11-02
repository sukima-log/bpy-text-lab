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
#------------------------------------------------
# Exist Flag
#------------------------------------------------
# [[obj_name1, obj_name2, ...], True/False] のリスト形式
#  True: 全て存在, False: 存在しないものがある
EXIST_FLAG_LIST = []

#------------------------------------------------
# Global Parameter
#------------------------------------------------
GP_CUBE_SIZE    = 0.3   # 30 cm * 30 cm * 30 cm

#------------------------------------------------
# Objects
#------------------------------------------------
# Sample Light
base_light      = "base_light"
# Create Object
sukima_logo     = "sukima_logo"
# Armature
sukima_logo_bone    = "sukima_logo_bone"

#------------------------------------------------
# Material
#------------------------------------------------
# sukima_logo
MT_SUKIMA_LOGO_BASE         = "MT_SUKIMA_LOGO_BASE"
MT_SUKIMA_LOGO_BLACK        = "MT_SUKIMA_LOGO_BLACK"
MT_SUKIMA_LOGO_ORANGE       = "MT_SUKIMA_LOGO_ORANGE"
MT_SUKIMA_LOGO_GRAY         = "MT_SUKIMA_LOGO_GRAY"
MT_SUKIMA_LOGO_LIGHT_GREEN  = "MT_SUKIMA_LOGO_LIGHT_GREEN"
MT_SUKIMA_LOGO_GREEN        = "MT_SUKIMA_LOGO_GREEN"
#------------------------------------------------
# Animation/Action
#------------------------------------------------
# sukima_logo
ANI_SUKIMA_LOGO_BONE_RUN    = "ANI_SUKIMA_LOGO_BONE_RUN"
#------------------------------------------------
# Generation Flag
#------------------------------------------------
def glb_require_new_objects(
    obj_list=[]
,   flg_name="flg_name"
):
    if (len(obj_list) == 0):
        return
    else:
        if  (flg_name == "sample_obj_flg_judge"):
            global sample_obj_flg_judge
            sample_obj_flg_judge = \
            mm_cm_lib.require_new_objects(
                obj_list=obj_list
            ,   gen_flag=False
            )

#------------------------------------------------
# Object Existence Check
#------------------------------------------------
def glb_exist_obj_chk(
    obj_list=["object_name"],   # Object Name List
    gen_flag=False              # オブジェクト生成タイミングフラグ
):
    """
    指定したオブジェクト群が既に存在するかどうかを確認し、
    生成前と生成後で異なる動作を行う。

    Parameters
    ----------
    obj_list : list[str]
        対象となるオブジェクト名のリスト
    gen_flag : bool
        True  の場合 → 生成直後の存在確認（初期登録）
        False の場合 → 生成前に存在していたかの確認（後判定）

    Returns
    -------
    bool
        True  → 新規生成 or 変形処理が必要
        False → 既存利用または変形不要
    """

    # -----------------------------------------------------------
    # グローバルリスト（存在フラグ記録用）
    # -----------------------------------------------------------
    exist_flag_list = EXIST_FLAG_LIST

    # -----------------------------------------------------------
    # 内部ヘルパー: オブジェクトの存在確認
    # -----------------------------------------------------------
    def all_exist(obj_names):
        """すべてのオブジェクトが存在しているか"""
        for name in obj_names:
            obj = bpy.data.objects.get(name)
            if obj is None or name not in bpy.context.scene.objects:
                return False
        return True

    # -----------------------------------------------------------
    # - gen_flag = True  → オブジェクト生成直後に存在確認
    # -----------------------------------------------------------
    if gen_flag:
        all_exists = all_exist(obj_list)
        exist_flag_list.append([obj_list, all_exists])

        if all_exists:
            # すでに全て存在 → 新規生成不要
            return False
        else:
            # 存在していないものがある → 新規生成が必要
            return True

    # -----------------------------------------------------------
    # - gen_flag = False → 生成処理前に存在していたか確認
    # -----------------------------------------------------------
    else:
        # EXIST_FLAG_LIST から obj_list に一致する要素を探す
        for rec in exist_flag_list:
            if rec[0] == obj_list:
                # False → 以前存在しなかった → 変形処理必要
                if rec[1] is False:
                    return True
                # True → 以前存在していた → 変形処理不要
                else:
                    return False

        # 該当記録なし → 存在確認して登録
        all_exists = all_exist(obj_list)
        exist_flag_list.append([obj_list, all_exists])

        # 存在しなければ変形必要、存在していれば不要
        return not all_exists

