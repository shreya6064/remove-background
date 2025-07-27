import bpy
import os
import sys

    
import torch
from torch.autograd import Variable
import numpy as np
from PIL import Image
from torchvision import transforms

import tempfile

from .model import U2NET
from .data_loader import RescaleT, ToTensorLab, SalObjDataset
from .colour_transfer import apply_color_transfer


def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)
    return (d - mi) / (ma - mi + 1e-8)


def save_output(image_path, pred, output_path):
    predict_np = pred.squeeze().cpu().data.numpy()
    im = Image.fromarray((predict_np * 255).astype(np.uint8)).convert('RGB')

    original = Image.open(image_path)
    im_resized = im.resize(original.size, resample=Image.BILINEAR)

    im_resized.save(output_path)
    print(f"Saved: {output_path}")


def run_u2net_on_image(image_path, output_path, model_path):
    #transform
    transform = transforms.Compose([
        RescaleT(320),
        ToTensorLab(flag=0)
        #ToTensorLab()

    ])

    #wrap image
    dataset = SalObjDataset(
        img_name_list=[image_path],
        lbl_name_list=[],
        transform=transform
    )

    loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)

    #load the model
    net = U2NET(3, 1)
    net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    net.eval()

    for i, data in enumerate(loader):
        input_tensor = data['image'].type(torch.FloatTensor)
        input_tensor = Variable(input_tensor)

        with torch.no_grad():
            d1, *_ = net(input_tensor)
            pred = normPRED(d1[:, 0, :, :])
            save_output(image_path, pred, output_path)

        break  #run once



def load_output_mask_as_internal_image(output_path, original_bpy_image):
    
    original_name = original_bpy_image.name.split('.')[0]

    
    new_image_name = f"{original_name}_alpha"

    #load alpha mask as internal blender image
    img = bpy.data.images.load(output_path)
    img.name = new_image_name
    img.alpha_mode = 'CHANNEL_PACKED'  #preserve alpha

    print(f"Loaded U²-Net mask as: {new_image_name}")
    return img

    
    
class U2NET_OT_RunBackgroundRemoval(bpy.types.Operator):
    """Run U2Net Background Removal"""
    bl_idname = "u2net.run_removal"
    bl_label = "Generate Alpha"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    




    def execute(self, context):
        
        
        #node = bpy.context.active_node if bpy.context.active_node and bpy.context.active_node.type == 'TEX_IMAGE' else None
        node = None
        
        try:
            if bpy.context.active_node and bpy.context.active_node.type == 'TEX_IMAGE':
                node = bpy.context.active_node
        except:
            node = None
            
            
        space = bpy.context.space_data

        
        
        
        image = None

        if node:
            image = node.image
        elif space.type == 'IMAGE_EDITOR':
            image = space.image

        if not image:
            self.report({'ERROR'}, "No image found.")
            return {'CANCELLED'}

        
        temp_input_path = os.path.join(tempfile.gettempdir(), "_temp_input.png")
        image.save_render(filepath=temp_input_path)
        
    
        output_path = os.path.join(tempfile.gettempdir(), f"{image.name.split('.')[0]}_alpha.png")

        addon_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(addon_dir, "saved_models", "u2net", "u2net.pth")

        run_u2net_on_image(temp_input_path, output_path, model_path)
        
        original_image = image #context.scene.u2net_image
        alpha_image = load_output_mask_as_internal_image(output_path, original_image)
        
        
        
        if node:
            
            
            
            node_tree = node.id_data
            alpha_node = node_tree.nodes.new(type='ShaderNodeTexImage')
            alpha_node.image = alpha_image
            alpha_node.location.x = node.location.x
            alpha_node.location.y = node.location.y - 300
            
            #Check for Principled BSDF connected to original node
            output_links = node.outputs['Color'].links
            principled_node = None
            for link in output_links:
                to_node = link.to_node
                if to_node and to_node.type == 'BSDF_PRINCIPLED':
                    principled_node = to_node
                    break
                
            #Add ColorRamp node
            color_ramp = node_tree.nodes.new(type='ShaderNodeValToRGB')
            color_ramp.location.x = alpha_node.location.x + 300
            color_ramp.location.y = alpha_node.location.y
            
            
            #Link alpha image output to ColorRamp input
            node_tree.links.new(alpha_node.outputs['Color'], color_ramp.inputs[0])

            if principled_node:
                #Replace existing alpha input link
                if principled_node.inputs['Alpha'].is_linked:
                    old_link = principled_node.inputs['Alpha'].links[0]
                    node_tree.links.remove(old_link)

                node_tree.links.new(color_ramp.outputs['Color'], principled_node.inputs['Alpha'])
            
            alpha_node.hide = True
            
           
            
        else:
            space.image = alpha_image
            
        self.report({'INFO'}, f"Alpha Generated")
        return {'FINISHED'}




class U2NET_OT_ColorTransfer(bpy.types.Operator):
    """Apply Color Transfer to Active Image Texture"""
    bl_idname = "u2net.color_transfer"
    bl_label = "Colour Transfer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #from .color_transfer import apply_color_transfer  # 📦 Your new file

        node = bpy.context.active_node
        source_image = context.scene.u2net_transfer_from

        if not node or node.type != 'TEX_IMAGE':
            self.report({'ERROR'}, "No image texture node selected.")
            return {'CANCELLED'}
        if not source_image:
            self.report({'ERROR'}, "No transfer-from image selected.")
            return {'CANCELLED'}

        target_image = node.image
        if not target_image:
            self.report({'ERROR'}, "Target image texture node has no image.")
            return {'CANCELLED'}

        # Save both images to temp
        temp_dir = tempfile.gettempdir()
        target_path = os.path.join(temp_dir, "_target_image.png")
        source_path = os.path.join(temp_dir, "_source_image.png")
        output_path = os.path.join(temp_dir, f"{target_image.name}_recolor.png")

        target_image.save_render(target_path)
        source_image.save_render(source_path)

        # Run color transfer
        apply_color_transfer(source_path, target_path, output_path)

        # Load result
        result_img = bpy.data.images.load(output_path)
        result_img.name = f"{target_image.name}_recolor"



        # Add recolored image node
        node_tree = node.id_data
        new_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        new_node.image = result_img
        new_node.location.x = node.location.x
        new_node.location.y = node.location.y + 300

        # Add Mix node
        mix_node = node_tree.nodes.new(type='ShaderNodeMix')
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = 'MIX'
        mix_node.location.x = node.location.x + 300
        mix_node.location.y = node.location.y + 100
        mix_node.inputs[0].default_value = 1.0

        
        """
        # Connect mix output to whatever the original was connected to
        for link in node.outputs['Color'].links:
            node_tree.links.new(mix_node.outputs[0], link.to_socket)
            #node_tree.links.remove(link)

        """
               
        original_links = list(node.outputs['Color'].links)
        #print(original_links)
        for link in original_links:
            print(link.to_socket)
            print(link.from_socket)
            target_socket = link.to_socket
            node_tree.links.remove(link)
            node_tree.links.new(mix_node.outputs[2], target_socket)



        # Connect original image to input 1, recolored to input 2
        node_tree.links.new(node.outputs['Color'], mix_node.inputs[6])  # Input 1
        node_tree.links.new(new_node.outputs['Color'], mix_node.inputs[7])  # Input 2

        self.report({'INFO'}, f"Color transfer done: {result_img.name}")
        return {'FINISHED'}




    
    
class U2NET_PT_BackgroundRemovalPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport Sidebar"""
    bl_label = "Background Removal"
    bl_idname = "U2NET_PT_panel"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        #layout.prop(context.scene, "u2net_image", text="Input Image")
        #layout.operator("u2net.run_removal")
        
        #layout.prop(context.scene, "u2net_image", text="Internal Image")
        layout.operator("u2net.run_removal", icon='IMAGE_ZDEPTH')




class U2NET_PT_ShaderEditorPanel(bpy.types.Panel):
    """Panel for U2Net Background Removal in the Shader Editor"""
    bl_label = "Remove Background"
    bl_idname = "U2NET_PT_shader_editor_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.operator("u2net.run_removal", icon='IMAGE_ZDEPTH')
        layout.separator()
        layout.label(text="Colour Transfer:")
        layout.prop(context.scene, "u2net_transfer_from", text="Transfer From")
        layout.operator("u2net.color_transfer", icon='COLOR')