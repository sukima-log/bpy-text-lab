import bpy
import json
import os
import sys

# Get the current script being executed
script_text = bpy.context.space_data.text

# Get the directory of the current script
script_dir = os.path.dirname(bpy.path.abspath(script_text.filepath))

#=================================
# Output Vertex Position Differences
#=================================
def compare_vertex_positions(filepath, output_path):
    # Store the current mode (e.g., OBJECT, EDIT, etc.)
    current_mode = bpy.context.object.mode

    # Switch to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    obj = bpy.context.active_object
    if not obj or obj.type != 'MESH':
        print("No mesh object is selected.")
        return

    if not os.path.exists(filepath):
        print("Saved vertex file not found.")
        return

    # Load the previously saved vertex positions (as a dictionary)
    with open(filepath, 'r', encoding='utf-8') as f:
        old_coords_dict = json.load(f)

    current_coords = obj.data.vertices
    i_array, x_array, y_array, z_array = [], [], [], []

    for i, v in enumerate(current_coords):
        key = str(i)
        if key in old_coords_dict:
            old = old_coords_dict[key]

            # Convert local coordinates to world coordinates
            world_co = obj.matrix_world @ v.co

            # Calculate the difference
            dx = round(world_co.x - old['x'], 4)
            dy = round(world_co.y - old['y'], 4)
            dz = round(world_co.z - old['z'], 4)

            # Correct floating-point rounding errors (treat < ±0.0001 as 0)
            dx = 0.0 if abs(dx) < 1e-4 else dx
            dy = 0.0 if abs(dy) < 1e-4 else dy
            dz = 0.0 if abs(dz) < 1e-4 else dz

            # Support multi-digit indices and align to 7 characters
            # Ensures clean alignment for output formatting
            if (dx != 0) or (dy != 0) or (dz != 0):
                i_array.append(f"{i:<7},")     # Index aligned to 7 characters
                x_array.append(f"{dx:+.4f},")  # X coordinate
                y_array.append(f"{dy:+.4f},")  # Y coordinate
                z_array.append(f"{dz:+.4f},")  # Z coordinate

    # Format and join all arrays for clean output
    def format_array(name, array):
        joined = "".join(array).rstrip(", ")
        return f"{name}=[" + joined + "]\n"

    # Write all arrays to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(format_array("i_array", i_array))
        f.write(format_array("x_array", x_array))
        f.write(format_array("y_array", y_array))
        f.write(format_array("z_array", z_array))

    # print(f"Differences have been written to file: {output_path}")
    # Restore the original mode
    bpy.ops.object.mode_set(mode=current_mode)


filepath = os.path.join(script_dir, "point.json")
output_path = os.path.join(script_dir, "move.py")

# Run this after manually editing vertex positions
compare_vertex_positions(filepath, output_path)