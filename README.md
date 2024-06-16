<h2 align="center">
 <b>Instance Tracking in 3D Scenes from Egocentric Videos</b>
</h2>

<h3 align="center">
CVPR 2024
</h3>

<div align="center" margin-bottom="6em">
<a target="_blank" href="https://ics.uci.edu/~yunhaz5/">Yunhan Zhao</a>,
<a target="_blank" href="https://ics.uci.edu/~haoyum3/">Haoyu Ma</a>,
<a target="_blank" href="https://aimerykong.github.io/">Shu Kong</a>,
<a target="_blank" href="https://ics.uci.edu/~fowlkes/">Charless Fowlkes</a>
<br>
[Dataset Download] (Link will be available shortly!)
</div>
&nbsp;

<p align="center">
<img src="images/teaser.png"/>
</p>

Egocentric sensors such as AR/VR devices capture human-object interactions and offer the potential to provide task-assistance by recalling 3D locations of objects of interest in the surrounding environment. This capability requires instance tracking in real-world 3D scenes from egocentric videos (IT3DEgo). We introduce **IT3DEgo** benchmark to develop assistive agents that track the user's environment and provide *contextual guidance* on the **location** of objects of interest. 

## IT3DEgo Benchmark Task Illustration

<p align="center">
<img src="images/pipeline.png"/>
</p>

Given a raw RGB-D video sequence with camera poses and object instances of interest, i.e., either by online enrollment (SVOE) or pre-enrollment (MVPE), the goal of our benchmark task is to output the object instance 3D centers in a predefined world coordinate at each timestamp. Please check the paper for more details regarding the benchmark protocol and dataset.

## Benchmark Dataset

<p align="center">
<img src="images/hololens.png" style="width:525px;" />
</p>

<p align="center">
<img src="images/data_lowRes.gif" style="width:1200px;"/>
</p>

**Benchmark dataset** comes with the following three parts:

- **Raw video sequences.** RGB-D video sequences with per-frame camera pose, captured with HoloLens 2. The video data is organized in the following structure:
```
# Raw video sequence structure

├── Video Seq 1
│   ├── pv                    # rgb camera
│   ├── depth_ahat            # depth camera
│   ├── vlc_ll                # left-left grayscale camera
│   ├── vlc_lf                # left-front grayscale camera
│   ├── vlc_rf                # right-front grayscale camera
│   ├── vlc_rr                # right-right grayscale camera
│   ├── mesh                  # coarse mesh of the surrounding environment
│   ├── pv_pose.json
│   ├── depth_ahat_pose.json
│   ├── vlc_ll_pose.json
│   ├── vlc_lf_pose.json
│   ├── vlc_lf_pose.json
│   └── vlc_rr_pose.json
.
.
.
├── Video Seq N
└── Calibrations
```
Each camera pose JSON file (e.g., pv_pose.json or depth_ahat_pose.json) contains key value pairs of timestamp and the camera matrix. The calibration file specifies the camera parameters and the transformation matrices between each camera (please refer to [hl2ss](https://github.com/jdibenes/hl2ss) for more details).

- **Annotations.** We provide three types of annotations to support the study of the benchmark problem. The annotation data is organized in the following structure:

```
# Annotations structure

├── Video Seq 1
│   ├── labels.csv
│   ├── 3d_center_annot.txt
│   ├── motion_state_annot.txt
│   ├── 2d_bbox_annot
│   │   ├── 0.txt
│   │   .
│   |   .
│   |   .
│   |   └── K.txt
│   └── visuals                 # visual crops of object instances, only for visualization
│       ├── instance_1.png
│       .
│       .
│       .
│       └── instance_K.png
.
.
.
└── Video Seq N
```
Each line in `label.csv` describes the name of object instances to track, such as cup_1. 
The file `motion_state_annot.txt` describes the binary object motion state at each frame. Each line in this file has the format of `instance id, timestamp_start, timestamp_end`. The interval between `timestamp_start` and `timestamp_end` indicates the object remains stationary in this period. In other words, the object instance is being interacted with the user outside of each interval.
Inside the `2d_bbox_annot` folder, we provide the axis-aligned 2D bounding boxes for each object roughly every 5 frames if the object is visible. `0.txt` corresponds to the *first* object instance described in `label.csv`. Each line in `0.txt` has the format of `timestamp, x_min, y_min, x_max, y_max`. 
The `3d_center_annot.txt` file includes the 3D center of each object instance in a **predefined world coordinate**. Each line in this file has the format of `timestamp_start, timestamp_end, instance id, x, y, z, location id`. Location id describes the number of location changes of the current object with zero-based indexing.

- **Enrollment information.** We study two distinct setups to specify object instances of interest: single-view online enrollment (SVOE) and multi-view pre-enrollment (MVPE). Please check our paper for a detailed description of each enrollment. 
<!-- Note that single-view online enrollment (SVOE) is defined as the bounding box on specific video frames, which shares the same folder structure as the annotations. We release the SVOE enrollment inside the annotation folder. -->

```
# Single-view online enrollment (SVOE)

├── Video Seq 1
│   └── svoe.txt
.
.
.
└── Video Seq N

===============================================================

# Multi-view pre-enrollment (MVPE)

├── Instance 1                # folder name corresponds to instance names in label.csv in the annotation folder
│   ├── instance_image_1.png
│   .
│   .
│   .
│   └── instance_image_24.png
.
.
.
└── Instance M
```
Each line in `svoe.txt` file represents `instance id, timestamp, x_min, y_min, x_max, y_max`. Instand id corresponds to the label.csv in the annotation folder with zero-based indexing. In other words, the first object instance in `Annotations/Video Seq 1/label.csv` corresponds to instance 0 in `Video Seq 1/svoe.txt`.

## Run Demo Code

We release the code in jupyter notebook. It includes the step-by-step implementation of our proposed method, utilizing SAM and DINOvs for the benchmark task. Make sure you have installed the following requirements before running the demo code.
- PyTorch 2.0
- [hl2ss](https://github.com/jdibenes/hl2ss)
- [SAM](https://github.com/facebookresearch/segment-anything)
- [DINOv2](https://github.com/facebookresearch/dinov2)

The demo code adopts a slightly modified version of hl2ss and we release the modified code to help run the demo code. If you are interested in moving to the latest version of hl2ss, feel free to adjust accordingly.


## BibTex
```bibtex
@inproceedings{zhao2024instance,
  title={Instance tracking in 3D scenes from egocentric videos},
  author={Zhao, Yunhan and Ma, Haoyu and Kong, Shu and Fowlkes, Charless},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={21933--21944},
  year={2024}
}
```