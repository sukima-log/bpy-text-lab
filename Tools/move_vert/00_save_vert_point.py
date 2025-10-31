import bpy
import json
import os
import sys

# Get the current script being executed
script_text = bpy.context.space_data.text
# Get the directory of the current script
script_dir = os.path.dirname(bpy.path.abspath(script_text.filepath))

#=================================
# Save Vertex Positions
#=================================
def save_vertex_positions(filepath):
    # Store the current mode (e.g. OBJECT, EDIT, etc.)
    current_mode = bpy.context.object.mode
    # Switch to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    obj = bpy.context.active_object
    if not obj or obj.type != 'MESH':
        print("No mesh object is selected.")
        return

    # Ensure we are in Object Mode
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    coords = {}
    for i, v in enumerate(obj.data.vertices):
        world_co = obj.matrix_world @ v.co  # Convert to world space coordinates
        coords[str(i)] = {
            "x": round(world_co.x, 6),
            "y": round(world_co.y, 6),
            "z": round(world_co.z, 6)
        }

    with open(filepath, 'w') as f:
        json.dump(coords, f, indent=4)

    # print(f"Vertex positions saved to: {filepath}")
    # Restore the original mode
    bpy.ops.object.mode_set(mode=current_mode)

filepath = os.path.join(script_dir, "point.json")

# Run once to save the vertex positions
save_vertex_positions(filepath)