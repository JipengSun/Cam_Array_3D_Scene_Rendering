import blenderproc as bproc
import numpy as np
import os
import itertools

bproc.init()

# Load your scene objects once
objs_path = './assets/namaqualand/Namaqualand.blend'
objs = bproc.loader.load_blend(objs_path)

# Create a point light above the scene
light = bproc.types.Light()
light.set_location([2, -2, 10])
light.set_energy(300)


def construct_camera_rotation_list(angle_step):
    camera_rotations = []
    for angle in np.arange(0, 2 * np.pi, angle_step):
        camera_rotations.append([-np.pi/2, 0, angle])
    return camera_rotations

def construct_camera_location_list(x_start, x_end, step_num_x, y_start, y_end, step_num_y, z_start, z_end, step_num_z):
    camera_locations = []
    for x in np.linspace(x_start, x_end, step_num_x):
        for y in np.linspace(y_start, y_end, step_num_y):
            for z in np.linspace(z_start, z_end, step_num_z):
                camera_locations.append([x, y, z])
    return camera_locations

def create_camera_array(rows=2, cols=3, focal_length=3.6, resolution=(180, 180), gap_mm=3.75,
                        center_location=[0, -5, 5], center_rotation=[np.pi / 2, 0, 0]):

    # Convert gap from mm to m
    gap = gap_mm / 1000.0
    
    # Set camera resolution
    bproc.camera.set_resolution(resolution[0], resolution[1])
    
    # Set camera intrinsics
    bproc.camera.set_intrinsics_from_blender_params(
        lens=focal_length,
        lens_unit="MILLIMETERS"
    )
    
    # Compute offsets
    col_offsets = [(c - (cols - 1)/2) * gap for c in range(cols)]
    row_offsets = [-(r - (rows - 1)/2) * gap for r in range(rows)]
    
    # Add camera poses
    for r in range(rows):
        for c in range(cols):
            cam_loc = [
                center_location[0] + col_offsets[c],
                center_location[1],
                center_location[2] + row_offsets[r]
            ]
            cam_pose = bproc.math.build_transformation_mat(cam_loc, center_rotation)
            bproc.camera.add_camera_pose(cam_pose)


# Example lists of center locations and rotations
'''
center_locations = [
    [0, -5, 5],
    [1, -5, 5],
    [0, -4, 5]
]

camera_rotations = [
    [np.pi / 2, 0, 0],
    [np.pi / 3, 0, 0]
]
'''

#center_locations = construct_camera_location_list(-15, 15, 7, -15, 15, 7, 3, 5, 3)
center_locations = construct_camera_location_list(0, 0, 1, -5, -5, 1, 5, 5, 1)
camera_rotations = construct_camera_rotation_list(2*np.pi)

# Iterate over all combinations of center_locations and camera_rotations
for i, (loc, rot) in enumerate(itertools.product(center_locations, camera_rotations)):
    # Overwrite any existing camera poses with an empty set
    # This effectively clears previously added poses.
    #bproc.camera.load_camera_poses({"camera": {"poses": []}})
    
    # Create the camera array for the given location and rotation
    create_camera_array(
        rows=2,
        cols=3,
        focal_length=3.6,     # mm
        resolution=(180, 180),
        gap_mm=3.75,          # mm
        center_location=loc,
        center_rotation=rot
    )

# Render the scene
data = bproc.renderer.render()

# Create a unique output directory for this scenario
output_dir = f"output/grid_scenario_test/"
os.makedirs(output_dir, exist_ok=True)

# Write the rendering into a hdf5 file
bproc.writer.write_hdf5(output_dir, data)
