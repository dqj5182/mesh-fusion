import os

in_mesh_dir = 'data/MOW/data/models/board_food_v_LUS1jeTGc68_frame000082.obj'

os.system('python 1_scale.py --in_dir=examples/0_in/ --out_dir=examples/1_scaled/')
os.system('xvfb-run -a python 2_fusion.py --mode=render --in_dir=examples/1_scaled/ --depth_dir=examples/2_depth/ --out_dir=examples/2_watertight/')
os.system('python 2_fusion.py --mode=fuse --in_dir=examples/1_scaled/ --depth_dir=examples/2_depth/ --out_dir=examples/2_watertight/')
os.system('xvfb-run -a python 3_simplify.py --in_dir=examples/2_watertight/ --out_dir=examples/3_out/')