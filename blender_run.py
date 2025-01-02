import bpy
import os
import sys

def generate_array_offset(cam_row, cam_col, cam_distance):
    cam_offsets = []
    for i in range(cam_row):
        for j in range(cam_col):
            # if rot_z = 0 deg
            # cam_offsets.append((j*cam_distance, 0, i*cam_distance))
            # if rot_z = 90 deg
            cam_offsets.append((0, j*cam_distance, i*cam_distance))
    return cam_offsets

def render_array_imgs(cam_loc, cam_rot, cam_offsets, frame, base_cam):

    for i, cam_offset in enumerate(cam_offsets):

        new_cam_data = base_cam.data.copy()
        new_cam_data.name = f"TempCamData_{frame}_{i}"
        new_cam_obj = bpy.data.objects.new(
            name=f"TempCamObj_{frame}_{i}",
            object_data=new_cam_data
        )
        camera_location = [
            cam_loc[0] + cam_offset[0],
            cam_loc[1] + cam_offset[1],
            cam_loc[2] + cam_offset[2]
        ]
        new_cam_obj.location = camera_location
        new_cam_obj.rotation_euler = cam_rot

        scene.collection.objects.link(new_cam_obj)
        scene.camera = new_cam_obj


        # print('updated camera location:', camera_location)
        # bpy.context.scene.camera.location = camera_location
        # Set the output file path for this frame
        scene.render.filepath = os.path.join(output_dir, f"frame_{frame:03d}_cam{i}.png")
        
        # Render the scene and save the image
        bpy.ops.render.render(write_still=True)

        bpy.data.objects.remove(new_cam_obj, do_unlink=True)
        bpy.data.cameras.remove(new_cam_data, do_unlink=True)


# Print available compute devices
print("Available Devices:")
sys.stdout.flush() 
for device in bpy.context.preferences.addons['cycles'].preferences.devices:
    print(f"Device: {device.name}, Type: {device.type}, Enabled: {device.use}")
    sys.stdout.flush() 

# Define the output directory for rendered images
output_dir = "/n/fs/pci-sharedt/chengzh/rendered_imgs/forest"  # Replace with your desired path
os.makedirs(output_dir, exist_ok=True)
# bpy.ops.wm.open_mainfile(filepath="/n/fs/pci-sharedt/chengzh/pine_forest/polyhaven_pine_fir_forest.blend")
bpy.ops.preferences.addon_enable(module='cycles')

# Enable Cycles render engine
bpy.context.scene.render.engine = 'CYCLES'

# Set GPU as the rendering device
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'OPTIX'  # Use 'OPTIX' if supported

# Select the GPUs to use
for device in bpy.context.preferences.addons['cycles'].preferences.devices:
    if device.type == 'CUDA' or device.type == 'OPTIX':  # Adjust for your device type
        device.use = True

# Optional: Adjust render settings for performance
bpy.context.scene.cycles.device = 'GPU'  # Ensure GPU rendering is active

# Get the scene
scene = bpy.context.scene
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100

# The camera with animation. Must be an Object, not just Camera data.
base_cam = scene.camera  
if base_cam is None:
    raise RuntimeError("No active camera set in scene!")
# Keep track of the original scene camera so we can restore it at the end
original_scene_camera = scene.camera

# Get the frame range for the animation
frame_start = 56 #scene.frame_start
frame_end = scene.frame_end
print('The start and end frames are:', frame_start, frame_end)

# Set the render settings for PNG format
scene.render.image_settings.file_format = 'PNG'

# Iterate over all frames in the animation
for frame in range(frame_start, frame_end + 1):
    # Set the current frame
    scene.frame_set(frame)

    base_loc = base_cam.location.copy()
    base_rot = base_cam.rotation_euler.copy()
    cam_offsets = generate_array_offset(cam_row=2, cam_col=3, cam_distance=3.75/1000)

    render_array_imgs(base_loc, base_rot, cam_offsets, frame, base_cam)

scene.camera = original_scene_camera
print(f"Rendered frames saved to {output_dir}")
