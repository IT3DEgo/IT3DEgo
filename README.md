# IT3DEgo

Official repo of the paper

**[Instance Tracking in 3D Scenes from Egocentric Videos](https://arxiv.org/pdf/2312.04117.pdf)**

Yunhan Zhao, Haoyu Ma, Shu Kong, Charless Fowlkes

## Abstract

<p align="center">
<img src="images/teaser.png"/>
</p>

Egocentric sensors such as AR/VR devices capture human-object interactions and offer the potential to provide task-assistance by recalling 3D locations of objects of interest in the surrounding environment. This capability requires instance tracking in real-world 3D scenes from egocentric videos (IT3DEgo). We explore this problem by first introducing a new benchmark dataset, consisting of RGB and depth videos, per-frame camera pose, and instance-level annotations in both 2D camera and 3D world coordinates. We present an evaluation protocol which evaluates tracking performance in 3D coordinates with two settings for enrolling instances to track: (1) single-view **online enrollment** where an instance is specified on-the-fly based on the human wearer's interactions. and (2) multi-view **pre-enrollment** where images of an instance to be tracked are stored in memory ahead of time. To address IT3DEgo, we first re-purpose methods from relevant areas, e.g., single object tracking (SOT) -- running SOT methods to track instances in 2D frames and lifting them to 3D using camera pose and depth. We also present a simple method that leverages pretrained segmentation and detection models to generate proposals from RGB frames and match proposals with enrolled instance images. Perhaps surprisingly, our extensive experiments show that our method (with no finetuning) significantly outperforms SOT-based approaches. We conclude by arguing that the problem of egocentric instance tracking is made easier by leveraging camera pose and using a 3D allocentric (world) coordinate representation.

## IT3DEgo Benchmark Task Illustration

<p align="center">
<img src="images/pipeline.png"/>
</p>

Please check the paper for more details regarding the benchmark protocol and dataset.

## Capture Device and Raw Video Sequences

<p align="center">
<img src="images/hololens.png" style="width:525px;" />
</p>

<p align="center">
<img src="images/data_lowRes.gif" style="width:1200px;"/>
</p>

The dataset and code will be released shortly after the acceptance of the paper. Please stay tuned!
