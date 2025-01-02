#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=blender_arr

# Remove one # to uncommment
#SBATCH --output=%x-%j.log

# Define, how many nodes you need. Here, we ask for 1 node.
#SBATCH -N 1 #nodes
#SBATCH -n 1 #tasks
#SBATCH --cpus-per-task=80
#SBATCH --mem=400G
#SBATCH --time=0-6:00:00    # Run for 6 hours
#SBATCH --gres=gpu:10
#SBATCH --partition=gpu                  # Partition with GPU access


# Define and create a unique scratch directory for this job
# tag=aug14_curriculum;
# OUT_DIRECTORY='output/'${tag}
# mkdir ${OUT_DIRECTORY};

# Submit jobs.

# module load cuda/12.6
# module load /n/fs/pci-sharedt/chengzh/blender-4.2.0-linux-x64/blender/4.2.0
# blender -b -P blender_run.py --cycles-device CUDA
# /n/fs/pci-sharedt/chengzh/blender-4.2.0-linux-x64/blender -b -P blender_run.py > %x-%j.stdout 2>&1
/n/fs/pci-sharedt/chengzh/blender-4.2.0-linux-x64/blender -b /n/fs/pci-sharedt/chengzh/pine_forest/polyhaven_pine_fir_forest.blend -P blender_run.py
wait; #Make sure to wait till all the runs have completed.

# Finish the script
# exit 0