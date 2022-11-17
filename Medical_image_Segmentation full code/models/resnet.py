# -*- coding: utf-8 -*-
"""resnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19TshNmkE_tGzwG1N9HWOY57soCYpIs_W
"""

from functools import reduce

import torch
import torch.nn as nn
from torchvision.models import resnet50_32x4d, resnet101_32x8d

class LambdaBase(nn.Sequential):
    def __init__(self, fn, *args):
        super(LambdaBase, self).__init__(*args)
        self.lambda_func = fn

    def forward_prepare(self, input):
        output = []
        for module in self._modules.values():
            output.append(module(input))
        return output if output else input

class Lambda(LambdaBase):
    def forward(self, input):
        return self.lambda_func(self.forward_prepare(input))

class LambdaMap(LambdaBase):
    def forward(self, input):
        return list(map(self.lambda_func, self.forward_prepare(input)))

class LambdaReduce(LambdaBase):
    def forward(self, input):
        return reduce(self.lambda_func, self.forward_prepare(input))

def resnet50():
    model  = resnet50_32x4d()
    model.conv1 = nn.Conv2d(1, 64, (7, 7), (2, 2), (3, 3), 1, 1, bias = False)
    model.avgpool = nn.AvgPool2d((7,7), (1, 1))
    model.fc = nn.Sequential(
        Lambda(lambda  x: x.view(x.size(0), -1)),
        Lambda(lambda  x: x.view(1, -1) if 1 == len(x.size()) else x),
        nn.Linear(2048, 1000)
    )
    return model 

def resnet101():
    model  = resnet101_32x8d()
    model.conv1 = nn.Conv2d(1, 64, (7, 7), (2, 2), (3, 3), 1, 1, bias = False)
    model.avgpool = nn.AvgPool2d((7,7), (1, 1))
    model.fc = nn.Sequential(
        Lambda(lambda  x: x.view(x.size(0), -1)),
        Lambda(lambda  x: x.view(1, -1) if 1 == len(x.size()) else x),
        nn.Linear(2048, 1000)
    )
    return model