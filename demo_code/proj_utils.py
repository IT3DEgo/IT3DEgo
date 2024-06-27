import os
import sys
import numpy as np
import cv2

sys.path.insert(0, "your path to hl2ss")
import hl2ss
import hl2ss_3dcv
import utils


def to_homogeneous(array):
    return np.concatenate((array.reshape(3, 1), np.ones((1, 1), dtype=array.dtype)), axis=0)


def compute_depth_scale_map_wrapper(frame, seq_name, hw, depth_pose=None, rgb_pose=None):
    depth_fname = frame.replace("pv", "depth_ahat")
    # load raw depth
    raw_depth = cv2.imread(depth_fname, cv2.IMREAD_UNCHANGED)
    
    # load depth calib
    calibration_path = "/".join(frame.split("/")[:-3])
    ahat_calibration = hl2ss_3dcv._load_calibration_rm_depth_ahat(os.path.join(calibration_path, "calibrations", "rm_depth_ahat"))
    pv_calibration = utils._load_calibration_pv_yz(os.path.join(calibration_path, "calibrations", "personal_video"))

    ahat_to_pv_image = hl2ss_3dcv.camera_to_rignode(ahat_calibration.extrinsics) \
                       @ hl2ss_3dcv.rignode_to_camera(pv_calibration.extrinsics) \
                       @ pv_calibration.intrinsics

    uv, xyz = compute_depth_scale_map(raw_depth, ahat_calibration, ahat_to_pv_image)

    reproj_xyz_map = np.zeros(hw['image']+ (3,)).astype(np.float32) # same shape as pv img, each pixel element is the 3D coord in the depth camera space 

    u = uv[..., 0].astype(int).reshape(-1)
    v = uv[..., 1].astype(int).reshape(-1)

    keep = (u >= 0) & (u < hw['image'][1]) & (v >= 0) & (v < hw['image'][0])

    reproj_xyz_map[v[keep], u[keep], :] = xyz.reshape(-1, 3)[keep]

    return reproj_xyz_map


def compute_depth_scale_map(raw_depth, ahat_calibration, ahat_to_pv_image):
    uv2xy = ahat_calibration.uv2xy 
    xy1 = hl2ss_3dcv.to_homogeneous(uv2xy)
    scale = np.linalg.norm(xy1, axis=2) * (ahat_calibration.scale / hl2ss.Parameters_RM_DEPTH_AHAT.FACTOR)

    depth = raw_depth / scale 
    xyz = xy1 * depth[:, :, np.newaxis] # in depth coordinate, 
    xyz1 = hl2ss_3dcv.to_homogeneous(xyz)

    uv, _ = hl2ss_3dcv.project_to_image(xyz1, ahat_to_pv_image)

    return uv, xyz


def pv_bbox2depth_unproj(bbox, reproj_xyz_map):
    '''
        bbox format: XYXY_ABS
    '''
    start_x, start_y, stop_x, stop_y = bbox

    # check whether the depth is invalid
    xyz = reproj_xyz_map[int(start_y):int(stop_y), int(start_x):int(stop_x), :] # M x N x 3
    # get all non-zero z index
    y_idx, x_idx = xyz[..., 2].nonzero()

    if len(x_idx) == 0:
        # no valid depth in the bbox region
        return None, 0
    else:
        # pick the index closest to the center of the bbox
        c_y, c_x = int((stop_y - start_y)/2.), int((stop_x - start_x)/2.)
        sel_idx = (np.abs(y_idx - c_y) + np.abs(x_idx - c_x)).argmin()
        valid_y, valid_x = y_idx[sel_idx], x_idx[sel_idx]
        return xyz[valid_y, valid_x], 1
