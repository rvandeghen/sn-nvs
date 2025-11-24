# SoccerNet Novel View Synthesis - SN-NVS
Novel view synthesis has transformed 3D scene reconstruction, enabling the rendering of photorealistic perspectives from sparse observations and democratizing immersive content creation. Soccer broadcasts can offer a interesting application for novel view synthesis (NVS), as they provide multiple camera angles of dynamic scenes with complex interactions. However, the gap between broadcast point of view and novel viewpoints using the point of view of a player or a referee remains significant, making it challenging to generate high-quality novel views in soccer scenarios.

## Dataset
The dataset contains 5 scenes generated with the Blender game engine, featuring different soccer actions. Each scene is divided in 2 different sets: train and challenge. The train set includes broacasted images and camera parameters using COLMAP with known poses. For the challenge set, only the poses of the novel views are provided, but not the ground truth images. However, for the sake of compatibility with existing NVS methods, we provide dummy images (black images) in the challenge set.

The dataset follow the structure below:
```text
SoccerNet-NVS/
├── scene-1/
│   ├── images/
│   ├── images_2/
│   ├── images_4/
│   ├── images_8/
│   └── sparse/
│       └── 0/
│           ├── cameras.bin
│           ├── images.bin
│           ├── points3D.bin
│           └── points3D.ply
├── scene-2/
```

Note that the original `images/` have a 4K resolution (4096x2160), and the other folders contain downsampled versions. Participants are free to use any of these resolutions for training, but the evaluation will be performed at a resolution of 2048x1080 (i.e., `images_2/`).

The dataset is available at our Hugging Face repository: [https://huggingface.co/datasets/SoccerNet/SN-NVS-2026/tree/main](https://huggingface.co/datasets/SoccerNet/SN-NVS-2026/tree/main)

## Evaluation
We evaluate the reconstruction quality using the PSNR following standard practices. However, we also encourage the participants to keep track of other metrics such as SSIM and LPIPS, as they provide complementary information about the reconstruction quality of the generated images. We will evaluate the images using a resolution of 2048x1080 (equivalent to `images_2`). 

## Baselines

We evaluated 2 baseline methods: 3D Gaussian Splatting [3DGS](https://github.com/graphdeco-inria/gaussian-splatting) and Triangle Splatting [TS](https://github.com/trianglesplatting/triangle-splatting/tree/main).  
The results on the challenge set are the the following:
| Method | PSNR ↑  | SSIM ↑ | LPIPS ↓ |
|--------|---------|--------|---------|
| 3DGS   | **26.74**   | 0.75   | 0.41    |
| TS     | 26.43   | **0.757**  | **0.359**   |

## Training the Baselines

After you have downloaded the dataset and installed the chosen method, you can train the baseline methods using the following commands.

### Installing the repository

Here are the basic steps to install the 3DGS repository (same for TS) from this repository, as submodules:

```bash
git clone https://github.com/SoccerNet/sn-nvs --recursive
cd submodules/gaussian-splatting

conda env create --file environment.yml
conda activate gaussian_splatting
```

### Training

```bash
cd submodules/gaussian-splatting
conda activate gaussian_splatting
python train.py -s <path_to_scene> -i images_2 -r 1 -m <path_to_save_model> --eval --extra_flags
```

with `--extra_flags` being related to the specific method.

### Rendering

```bash
cd submodules/gaussian-splatting
conda activate gaussian_splatting
python render.py -s <path_to_scene> -m <path_to_trained_model> --eval --skip_train
```

### Validation set metrics

```bash
cd submodules/gaussian-splatting
conda activate gaussian_splatting
python metrics.py -m <path_to_trained_model>
```

## Codabench

For the challenge submission, we use Codabench as the submission platform. You can find the challenge page here: [https://www.codabench.org/competitions/11339/](https://www.codabench.org/competitions/11339/).  

For the challenge submission, participants should use the provided `render_challenge.py` script (equivalent to `render.py` from 3DGS). To use it, you need to specify the model path you used during training, but you need to specify the challenge scene path. An example can be found below, using the 3DGS method:
```bash
cd submodules/gaussian-splatting
conda activate gaussian_splatting
python render_challenge.py -s <path_to_challenge_scene> -m <path_to_trained_model> -i images_2 -r 1
```

Depending on the method you use, you may need to change the `render` function.

The participants need to submit their results in a zip file with the following structure:
```text
├── scene-1-challenge/
│   ├── renders/
│   │   ├── 000000.png
│   │   ├── 000001.png
│   │   └── ...
├── scene-2-challenge/
│   ├── renders/
│   │   ├── 000000.png
│   │   ├── 000001.png
│   │   └── ...
```

The baseline results can be found in the Hugging Face repository: [https://huggingface.co/datasets/SoccerNet/SN-NVS-2026/tree/main](https://huggingface.co/datasets/SoccerNet/SN-NVS-2026/tree/main)

## Additional Information

If your method is based on the 3D Gaussian Splatting codebase, do not forget to use both `-i images_2` and `-r 1` flags to ensure the correct resolution and to disable the automatic rescaling during training.