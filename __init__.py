bl_info = {
    "name": "Remove Background",
    "blender": (4, 4, 3),
    "category": "Image Editor",
    "author": "Shreya Punjabi",
    "version": (1, 0, 0)
}

import os
import sys
import bpy

#addon directory
addon_dir = os.path.dirname(os.path.realpath(__file__))
modules_dir = os.path.join(addon_dir, "modules")

#update sys path
if modules_dir not in sys.path:
    sys.path.insert(0, modules_dir)
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)


from .main import U2NET_PT_BackgroundRemovalPanel, U2NET_OT_RunBackgroundRemoval





# --- Registration ---
def register():
    bpy.utils.register_class(U2NET_PT_BackgroundRemovalPanel)
    bpy.utils.register_class(U2NET_OT_RunBackgroundRemoval)
    bpy.types.Scene.u2net_image = bpy.props.PointerProperty(type=bpy.types.Image)

def unregister():
    bpy.utils.unregister_class(U2NET_PT_BackgroundRemovalPanel)
    bpy.utils.unregister_class(U2NET_OT_RunBackgroundRemoval)
    del bpy.types.Scene.u2net_image
