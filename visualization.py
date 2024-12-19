import os

from utils.io_utils import create_folder_if_not_exists, save_numpy_array_as_image, return_folder_file_list
from utils.vis_utils import convert_hdf5_to_image


hdf5_folder = "./output/grid_scenario_grid_new/"
color_output_folder = "./output_colors/grid_scenario_rgb_new/"
create_folder_if_not_exists(color_output_folder)

hdf5_file_list = return_folder_file_list(hdf5_folder)
for hdf5_file_name in hdf5_file_list:
    print(f"Processing {hdf5_file_name}")
    hdf5_file_path = os.path.join(hdf5_folder, hdf5_file_name)
    rgb_image_path = os.path.join(color_output_folder, hdf5_file_name.replace(".hdf5", ".png"))
    convert_hdf5_to_image(hdf5_file_path, "colors", rgb_image_path)
