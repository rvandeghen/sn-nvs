#
# The original code is under the following copyright:
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact george.drettakis@inria.fr


import torch
import os
from tqdm import tqdm
from os import makedirs
import torchvision
from argparse import ArgumentParser
import sys

def render_set(model_path, name, iteration, views, primitives, pipeline, background):
    render_path = os.path.join(model_path, name, "ours_{}".format(iteration), "renders")
    gts_path = os.path.join(model_path, name, "ours_{}".format(iteration), "gt")

    makedirs(render_path, exist_ok=True)
    makedirs(gts_path, exist_ok=True)

    for idx, view in enumerate(tqdm(views, desc="Rendering progress")):
        rendering = render(view, primitives, pipeline, background)["render"]
        gt = view.original_image[0:3, :, :]
        torchvision.utils.save_image(rendering, os.path.join(render_path, '{0:05d}'.format(idx) + ".png"))
        torchvision.utils.save_image(gt, os.path.join(gts_path, '{0:05d}'.format(idx) + ".png"))

def render_sets(dataset, iteration, pipeline, method):
    with torch.no_grad():
        dataset.eval = False
        if method == "ts":
            primitives = TriangleModel(dataset.sh_degree)
            scene = Scene(args=dataset,
                        triangles=primitives,
                        init_opacity=None,
                        init_size=None,
                        nb_points=None,
                        set_sigma=None,
                        no_dome=False,
                        load_iteration=iteration,
                        shuffle=False)
        elif method == "3dgs":
            primitives = GaussianModel(dataset.sh_degree)
            scene = Scene(dataset, primitives, load_iteration=iteration, shuffle=False)

        bg_color = [1,1,1] if dataset.white_background else [0, 0, 0]
        background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")

        render_set(dataset.model_path, "challenge", scene.loaded_iter, scene.getTrainCameras(), primitives, pipeline, background)

if __name__ == "__main__":
    import sys
    method = sys.argv[1]

    if method == "ts":
        sys.path.append("submodules/triangle-splatting/")
        from utils.general_utils import safe_state
        from arguments import ModelParams, PipelineParams, get_combined_args
        from triangle_renderer import render, TriangleModel
        from scene import Scene
    elif method == "3dgs":
        sys.path.append("submodules/gaussian-splatting/")
        from utils.general_utils import safe_state
        from arguments import ModelParams, PipelineParams, get_combined_args
        from gaussian_renderer import render, GaussianModel
        from scene import Scene

    parser = ArgumentParser(description="Testing script parameters")
    model = ModelParams(parser, sentinel=True)
    pipeline = PipelineParams(parser)
    parser.add_argument("method", help="Rendering method")
    parser.add_argument("--iteration", default=-1, type=int)
    parser.add_argument("--quiet", action="store_true")
    args = get_combined_args(parser)
    print("Rendering " + args.model_path)

    # Initialize system state (RNG)
    safe_state(args.quiet)

    render_sets(model.extract(args), args.iteration, pipeline.extract(args), method)