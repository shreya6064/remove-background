from skimage import io, transform
import torch
from torch.utils.data import Dataset
import numpy as np
from PIL import Image
#from skimage import color


class RescaleT(object):
    def __init__(self, output_size):
        self.output_size = output_size

    def __call__(self, sample):
        imidx, image, label = sample['imidx'], sample['image'], sample['label']


        img = transform.resize(image, (self.output_size, self.output_size), mode='constant')
        lbl = transform.resize(label, (self.output_size, self.output_size), mode='constant', order=0, preserve_range=True)



        



        return {'imidx': imidx, 'image': img, 'label': lbl}


class ToTensorLab(object):
    def __init__(self, flag=0):
        self.flag = flag

    def __call__(self, sample):
        imidx, image, label = sample['imidx'], sample['image'], sample['label']
        tmpLbl = np.zeros(label.shape)

        if np.max(label) >= 1e-6:
            label = label / np.max(label)

        tmpImg = np.zeros((image.shape[0], image.shape[1], 3))
        image = image / np.max(image)
        if image.shape[2] == 1:
            tmpImg[:, :, 0] = tmpImg[:, :, 1] = tmpImg[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
        else:
            tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
            tmpImg[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225

        tmpLbl[:, :, 0] = label[:, :, 0]
        tmpImg = tmpImg.transpose((2, 0, 1))
        tmpLbl = tmpLbl.transpose((2, 0, 1))
        return {'imidx': torch.from_numpy(imidx), 'image': torch.from_numpy(tmpImg), 'label': torch.from_numpy(tmpLbl)}


class SalObjDataset(Dataset):
    def __init__(self, img_name_list, lbl_name_list, transform=None):
        self.image_name_list = img_name_list
        self.label_name_list = lbl_name_list
        self.transform = transform

    def __len__(self):
        return len(self.image_name_list)

    def __getitem__(self, idx):
        image = io.imread(self.image_name_list[idx])
        imidx = np.array([idx])
        label = np.zeros(image.shape)  # dummy label

        if len(image.shape) == 2:
            image = image[:, :, np.newaxis]

        if len(label.shape) == 2:
            label = label[:, :, np.newaxis]

        sample = {'imidx': imidx, 'image': image, 'label': label}
        if self.transform:
            sample = self.transform(sample)
        return sample
