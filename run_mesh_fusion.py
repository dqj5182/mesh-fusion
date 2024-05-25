import os

in_off_mesh_dir = 'examples/0_in'
scaled_mesh_dir = 'examples/1_scaled'
depth_mesh_dir = 'examples/2_depth'
watertight_mesh_dir = 'examples/2_watertight'
output_dir = 'examples/3_out'

os.system(f'python 1_scale.py --in_dir={in_off_mesh_dir} --out_dir={scaled_mesh_dir}')
os.system(f'xvfb-run -a python 2_fusion.py --mode=render --in_dir={scaled_mesh_dir} --depth_dir={depth_mesh_dir} --out_dir={watertight_mesh_dir}')
os.system(f'python 2_fusion.py --mode=fuse --in_dir={scaled_mesh_dir} --depth_dir={depth_mesh_dir} --out_dir={watertight_mesh_dir}')
os.system(f'xvfb-run -a python 3_simplify.py --in_dir={watertight_mesh_dir} --out_dir={output_dir}')