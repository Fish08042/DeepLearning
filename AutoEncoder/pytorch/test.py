import os
import sys
import argparse
import numpy as np

import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision
from torchvision import datasets, transforms
from torch.utils.data.sampler import SubsetRandomSampler

from utils import dataloader, imshow
from autoencoder import Encoder, Decoder, AutoEncoder


def main(args):
    model = AutoEncoder()
    use_gpu = torch.cuda.is_available()
    if use_gpu:
        print('cuda is available!')
        model.cuda()

    weight_file = args.path_weight_file

    model = AutoEncoder()
    model.load_state_dict(
        torch.load(weight_file, map_location=lambda storage, loc: storage))

    test_dataset = dataloader('dogs_cats', 'test')
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=args.batch_size, shuffle=False)

    images, _ = iter(test_loader).next()
    images = Variable(images, volatile=True)

    imshow(torchvision.utils.make_grid(images.data[:25], nrow=5))
    outputs = model(images)
    imshow(torchvision.utils.make_grid(outputs.data[:25], nrow=5))


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--n_epochs', type=int, help='Number of epochs', default=500)
    parser.add_argument(
        '--batch_size', type=int, help='Number of batch size', default=8)
    parser.add_argument(
        '--path_weight_file', type=str, help='Path to weight file')

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))