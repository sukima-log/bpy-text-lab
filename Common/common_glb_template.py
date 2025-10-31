#------------------------------------------------
# Global Parameter
#------------------------------------------------

#------------------------------------------------
# Objects
#------------------------------------------------
# Sample Light
base_light      = "base_light"
# Create Object
sample_obj      = "sample_obj"
# Armature

#------------------------------------------------
# Material
#------------------------------------------------
MT_SAMPLE       = "MT_SAMPLE"

#------------------------------------------------
# Animation/Action
#------------------------------------------------

#------------------------------------------------
# Generation Flag
#------------------------------------------------
def glb_require_new_objects(
    obj_list=[]
,   flg_name="flg_name"
):
    if (len(obj_list) == 0):
        global base_light_flg
        base_light_flg = \
        mm_cm_lib.require_new_objects(
            obj_list=[base_light]
        ,   gen_flag=False
        )
        # Sample
        global sample_obj_flg
        sample_obj_flg = \
        mm_cm_lib.require_new_objects(
            obj_list=[sample_obj]
        ,   gen_flag=False
        )
    else:
        if  (flg_name == "sample_obj_flg_judge"):
            global sample_obj_flg_judge
            sample_obj_flg_judge = \
            mm_cm_lib.require_new_objects(
                obj_list=obj_list
            ,   gen_flag=False
            )

