# test_conn1.py
"""
Created on Sun Jun  3 12:16:22 2018

@author: Wentao Huang
"""
from collections import OrderedDict
import torch as tc
import infonets as it

PARAMS = OrderedDict()
PARAMS['eps'] = 1e-6
PARAMS['seed'] = -1
PARAMS['max_epoches'] = 200

PARAMS['denoise'] = 1 # -1, 0, 1, 2, 3
PARAMS['energy_ratio'] = 0.05#.99
PARAMS['iscent'] = True
PARAMS['ridge'] = None

PARAMS['out_zoom'] = -1 # -1, 0
PARAMS['outsize'] = 100

PARAMS['momentum_decay']= 0.9
PARAMS['save_history'] = True #False#
PARAMS['display'] = 10 #0 # 1, ... # None
PARAMS['beta'] = 2.0
PARAMS['bias_requires_grad'] = True
PARAMS['ith_cls'] = 0
PARAMS['balance_factor'] = 0.5
PARAMS['margin'] = 0.5

PARAMS['save_inter_vals'] = False
PARAMS['save_bases_filters'] = True

###############################################################################
if __name__ == "__main__":
    rootdir1 = it.utils.get_rootdir()

    fname = it.utils.path_join(rootdir1, 'data', 'MNIST', 'new', 'train.pt')#'CIFAR10'
    ds = tc.load(fname)

    ds = it.utils.Ordered2DPatches(ds.cls_list[0:3], kernel_size=None,
                                   extraction_step=5, indent=0,
                                   max_patches=5e+4)
    ds.view_(-1)

    F = it.nn.Conn1(input=ds, learning_method='srelu2', params=PARAMS) #

    weight, bias, beta, margin, history = F.train_exe()

    # %%
#    for dd, label in ds:
#        print('Size = {}, label = {}'.format(dd.shape, label))
#    ds.reiter()

    W =  F.bases# F.filters# F.layers[0].U.t()#
    W = it.utils.sort_weights(W)
    images = it.utils.make_grid_2d(W, padding=1,scale_each=True, pad_value=0)
    it.utils.imshow(images)
    it.utils.show1d(history, title='Objective History', xlabel='Iteration', ylabel='Objective')

