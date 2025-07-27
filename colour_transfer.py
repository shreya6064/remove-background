import cv2
import numpy as np

def apply_color_transfer(source_path, target_path, output_path):
    src = cv2.imread(source_path)
    tgt = cv2.imread(target_path)

    src = cv2.resize(src, (tgt.shape[1], tgt.shape[0]))

    # Convert to LAB
    src_lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(np.float32)
    tgt_lab = cv2.cvtColor(tgt, cv2.COLOR_BGR2LAB).astype(np.float32)

    # Channel-wise mean/std
    for i in range(3):
        s_mean, s_std = src_lab[:, :, i].mean(), src_lab[:, :, i].std()
        t_mean, t_std = tgt_lab[:, :, i].mean(), tgt_lab[:, :, i].std()
        tgt_lab[:, :, i] = (tgt_lab[:, :, i] - t_mean) * (s_std / (t_std + 1e-8)) + s_mean

    tgt_lab = np.clip(tgt_lab, 0, 255).astype(np.uint8)
    result = cv2.cvtColor(tgt_lab, cv2.COLOR_LAB2BGR)

    cv2.imwrite(output_path, result)
