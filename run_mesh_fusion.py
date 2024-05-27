import os
import trimesh

# in_off_mesh_dir = 'examples/0_in'
# scaled_mesh_dir = 'examples/1_scaled'
# depth_mesh_dir = 'examples/2_depth'
# watertight_mesh_dir = 'examples/2_watertight'
# output_dir = 'examples/3_out'

in_obj_mesh_dir = 'data/MOW/data/models'
in_off_mesh_dir = 'tmp_exp_out/0_off_models'
scaled_mesh_dir = 'tmp_exp_out/1_scaled'
depth_mesh_dir = 'tmp_exp_out/2_depth'
watertight_mesh_dir = 'tmp_exp_out/2_watertight'
output_dir = 'data/MOW/data/watertight_models_fine'
num_processing = 10
n_views = 1000

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


while len(os.listdir(in_obj_mesh_dir)) != len(os.listdir(output_dir)):
    if not os.path.exists(in_off_mesh_dir):
        os.makedirs(in_off_mesh_dir)

    already_done = os.listdir(output_dir)


    # Convert obj files to off files
    count = 0
    for each_mesh in os.listdir(in_obj_mesh_dir):
        if each_mesh not in already_done:
            if count > num_processing:
                continue
            mesh = trimesh.load(os.path.join(in_obj_mesh_dir, each_mesh), force='mesh', process=False, validate=True)

            # Pass errorneous mesh
            if each_mesh in ['packing_v_NCIyd-Q80io_frame000132.obj', 'boardgame_v_otBlDwvDEwE_frame000257.obj', 'drink_v_DsA9B9dSIKQ_frame000048.obj', 'study_v_rN7Q1Lg-TD0_frame000204.obj', 'gardening_v_LiQ1htwLUXw_frame000207.obj', 'food_v_BfAaOmM2ds8_frame000082.obj', 'food_v_BfAaOmM2ds8_frame000082.obj', 'food_v_BfAaOmM2ds8_frame000082.obj', 'furniture_v_0CFuQ_zDwfY_frame000152.obj', 'study_v_oHzeN9ZrDRM_frame000824.obj', 'gardening_v_LiQ1htwLUXw_frame000218.obj']:
                continue
            else:
                _ = mesh.export(os.path.join(in_off_mesh_dir, each_mesh.replace('.obj', '.off')))
                count += 1


    # Run mesh-fusion
    os.system(f'python 1_scale.py --in_dir={in_off_mesh_dir} --out_dir={scaled_mesh_dir}')
    os.system(f'xvfb-run -a python 2_fusion.py --mode=render --in_dir={scaled_mesh_dir} --depth_dir={depth_mesh_dir} --out_dir={watertight_mesh_dir} --n_views={n_views}')
    os.system(f'python 2_fusion.py --mode=fuse --in_dir={scaled_mesh_dir} --depth_dir={depth_mesh_dir} --out_dir={watertight_mesh_dir} --n_views={n_views}')
    os.system(f'xvfb-run -a python 3_simplify.py --in_dir={watertight_mesh_dir} --out_dir={output_dir}')


    # Convert off files to obj files
    for each_mesh in os.listdir(output_dir):
        if '.off' in each_mesh:
            each_mesh_dir = os.path.join(output_dir, each_mesh)
            mesh = trimesh.load(each_mesh_dir, force='mesh')
            _ = mesh.export(each_mesh_dir.replace('.off', '.obj'))
            os.system(f'rm -rf {each_mesh_dir}')


    # Remove temporary directory
    os.system('rm -rf tmp_exp_out')

    import gc
    import torch
    torch.cuda.empty_cache()
    gc.collect()