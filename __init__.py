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
import subprocess
import ctypes
import getpass



python_bin = sys.executable
print("Python found", python_bin)
target_dir = os.path.join(os.path.dirname(__file__), "modules")
print("Target dir for modules:", target_dir)



requirements = [
    "torch==2.7.1",
    "torchvision==0.22.1",
    "pillow==11.2.1",
    "scikit-image==0.25.2"
]



extra_index = "https://download.pytorch.org/whl/cpu"



def fix_permissions_windows(path):
    """Grant full control to the current user for the given folder and contents."""
    try:
        username = getpass.getuser()
        print(username)
        cmd = f'''icacls "{path}" /grant "{username}:(OI)(CI)F" /T /C'''
        print(f"🔐 Fixing permissions with: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("⚠️ Permission fix error:", result.stderr)
        else:
            print("✅ Permissions fixed.")
    except Exception as e:
        print(f"❌ Failed to fix permissions: {e}")




# Install packages
def install_dependencies():
    if os.path.exists(target_dir) and os.listdir(target_dir):
        print("Modules already installed")
        return

    os.makedirs(target_dir, exist_ok=True)

    for pkg in requirements:
        print(f"🚀 Installing {pkg} into {target_dir}...")
        subprocess.check_call([
            python_bin, "-m", "pip", "install",
            pkg,
            "--target", target_dir,
            "--upgrade",
            "-f", extra_index
        ])
    print("✅ All packages installed.")
    fix_permissions_windows(target_dir)






#addon directory

addon_dir = os.path.dirname(os.path.realpath(__file__))
#modules_dir = os.path.join(addon_dir, "modules")

#update sys path
if target_dir not in sys.path:
    sys.path.insert(0, target_dir)
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)






from .main import U2NET_PT_BackgroundRemovalPanel, U2NET_OT_RunBackgroundRemoval

def attempt_imports_temp():

    
    import torch
    from torch.autograd import Variable
    import numpy as np
    from PIL import Image
    from torchvision import transforms

    import tempfile

    from .model import U2NET
    from .data_loader import RescaleT, ToTensorLab, SalObjDataset
    print("imports done")



# --- Registration ---
def register():
    install_dependencies()
    #attempt_imports_temp()
    
    bpy.utils.register_class(U2NET_PT_BackgroundRemovalPanel)
    bpy.utils.register_class(U2NET_OT_RunBackgroundRemoval)
    bpy.types.Scene.u2net_image = bpy.props.PointerProperty(type=bpy.types.Image)
    

def unregister():

    bpy.utils.unregister_class(U2NET_PT_BackgroundRemovalPanel)
    bpy.utils.unregister_class(U2NET_OT_RunBackgroundRemoval)
    del bpy.types.Scene.u2net_image
