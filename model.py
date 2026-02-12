import torch
import torch.nn as nn

class my_layer(nn.Module):

    def __init__(self, dtype):
        super(my_layer, self).__init__()
        self.horizon = nn.Conv2d(10, 100, kernel_size=(1, 9), stride=(1, 10), dtype=dtype)
        self.vert = nn.Conv2d(10, 100, kernel_size=(9, 1), stride=(10, 1), dtype=dtype)
        self.block = nn.Conv2d(10, 100, kernel_size=(3, 3), stride=(3, 3), dtype=dtype)
        self.lin = nn.Linear(810, 90, dtype=dtype)
        
    def forward(self, x):
        batch = []
        for item in x:
            x1 = self.horizon(item).reshape(1,-1)
            x2 = self.vert(item).reshape(1,-1)
            x3 = self.block(item).reshape(1,-1)
            x4 = self.lin(item.reshape(1, -1))
            x_ = torch.cat((x1, x2, x3, x4), dim=1)
            batch.append(x_)
        res = torch.cat(batch, dim=0)
        return res


class Sudoku_solver(nn.Module):

    def __init__(self, dtype):
        super(Sudoku_solver, self).__init__()
        self.conv = my_layer(dtype=dtype)
        self.l1 = nn.Linear(2700+90, 810, dtype=dtype)
        self.softm = nn.Softmax(dim=2)
        self.my_funct = lambda x: (self.softm(x.reshape(x.shape[0], x.shape[1] // 10, 10))).reshape(x.shape[0], -1)

    def forward(self, x):
        x = self.conv(x)
        x = self.my_funct(self.l1(x))
        return x

"""
Warning: Looks like you're using an outdated `kagglehub` version (installed: 0.3.13), please consider upgrading to the latest version (0.4.3).
Path to dataset files: C:/Users/user/.cache/kagglehub/datasets/bryanpark/sudoku/versions/3/sudoku.csv

Start training of model
Epoch: 0, loss: 0.02664
Epoch: 1, loss: 0.02373
Epoch: 2, loss: 0.02345
Epoch: 3, loss: 0.02326
Epoch: 4, loss: 0.02312
Epoch: 5, loss: 0.02301
Epoch: 6, loss: 0.02293
Epoch: 7, loss: 0.02287
Epoch: 8, loss: 0.02281
Epoch: 9, loss: 0.02276

Start testing of model
Accuracy: 88.61%
"""