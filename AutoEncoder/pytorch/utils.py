import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torchvision
from torchvision import datasets, transforms


def dataloader(dataset_sub_dir, data_sub_dir):
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, 'dataset', dataset_sub_dir)
    target_dir = os.path.join(data_dir, data_sub_dir)

    preprocess = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    return datasets.ImageFolder(target_dir,preprocess)


def imshow(images, file_name):
    images = images.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    images = std * images + mean
    images = np.clip(images, 0, 1)
    plt.imshow(images)
    plt.savefig('{}.png'.format(file_name))