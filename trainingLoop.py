import os
import math
import time
import torch
import random
import numpy as np
import pandas as pd

from torch.utils.data import DataLoader, ConcatDataset
from IPython.display import clear_output


from trainLoop import running_mean, training_loop, trainTestSplit, plot_grad_flow
from Model_inn import RepNet
from Dataset import getCombinedDataset
from SyntheticDataset import SyntheticDataset
from BlenderDataset import BlenderDataset

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print("Cuda availability : " + str(device))
#device = torch.device("cpu")

frame_per_vid = 64
multiple = False

folderName = 'content/DatasetFiles03/DatasetFiles/'
folderName = input("Enter Dataset Folder Name")

testDatasetC = getCombinedDataset('countix/countix_test.csv',
                                   folderName+'testvids',
                                   'test', folderName)
testDatasetS = SyntheticDataset(folderName+'synthvids', 'train*', 'mp4', 2000)

testList = [testDatasetC, testDatasetS]
random.shuffle(testList)
testDataset = ConcatDataset(testList)



trainDatasetC = getCombinedDataset('countix/countix_train.csv',
                                   folderName+'trainvids',
                                   'train', folderName)
#trainDatasetS1 = SyntheticDataset('/home/saurabh/Downloads/HP72','HP72', 'mp4', 500,
#                                   frame_per_vid=frame_per_vid)
#trainDatasetS2 = SyntheticDataset('/home/saurabh/Downloads', '1917', 'mkv', 500,
#                                   frame_per_vid=frame_per_vid)
trainDatasetS3 = SyntheticDataset(folderName+'synthvids', 'train*', 'mp4', 3000)
#trainDatasetS4 = SyntheticDataset('/home/saurabh/Downloads', 'HP6', 'mkv', 500,
#                                   frame_per_vid=frame_per_vid)
trainDatasetB = BlenderDataset(folderName+'blendervids', 'videos', 'annotations', frame_per_vid)

trainList = [trainDatasetC, trainDatasetS3] #, trainDatasetB]
random.shuffle(trainList)
trainDataset = ConcatDataset(trainList)

model =  RepNet(frame_per_vid)
model = model.to(device)

print("done")

"""Testing the training loop with sample datasets"""
 
sampleDatasetA = torch.utils.data.Subset(trainDataset, range(0, len(trainDataset)))
sampleDatasetB = torch.utils.data.Subset(testDataset, range(0,  len(testDataset)))

print(len(sampleDatasetA))

trLoss, valLoss = training_loop(  10,
                                  model,
                                  sampleDatasetA,
                                  sampleDatasetB,
                                  1,
                                  6e-5,
                                  'x3dbb',
                                  use_count_error=True,
                                  saveCkpt = 1,
                                  train = 1,
                                  validate = 1,
                                  lastCkptPath = None #'checkpoint/blender_no_mha_yes5.pt'
                               )