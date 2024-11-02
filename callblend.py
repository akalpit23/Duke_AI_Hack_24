import bpy
import numpy as np
import os

import sys
sys.path.append("/Users/akalpitdawkhar/Desktop/School/SEM_3/Data_HACK")
import blendgraph



def export_scene_to_dae(filepath):
    # Ensure the file has a .dae extension
    if not filepath.lower().endswith('.dae'):
        filepath += '.dae'
    
    # Export the scene to DAE format
    bpy.ops.wm.collada_export(
        filepath=filepath,
        check_existing=True,
        filter_glob="*.dae",
        apply_modifiers=True,
        selected=False,
        include_children=True,
        include_armatures=True,
        include_shapekeys=True,
        use_texture_copies=True
    )
    
    print(f"Exported to: {filepath}")

# Set the export path (change this to your desired location)
export_path = bpy.path.abspath("/Users/akalpitdawkhar/Desktop/School/SEM_3/Data_HACK//untitled.dae")

# Export the scene
export_scene_to_dae(export_path)
