import scipy.io
import numpy as np
import pandas as pd

path_to_old_csv = 'test.csv'
path_to_new_csv = 'test-6500-8000.csv'
path_to_new_mat = '6-12-RL.mat'

replace_range = np.arange(6501, 8001)
test_range = np.concatenate((np.arange(7001,8001),np.arange(8234,8301),np.arange(8834,8901)))

mat = scipy.io.loadmat(path_to_new_mat)

# construct new df of new annotations based on .mat file
# note that the index of images start with 1 instead of 0
# and the old_csv uses relative positions (0-1), but the new pts uses absolute positions (w, h)
w, h = 736, 748
types = ['pts_pos', 'pts_neg', 'pts_pos_o', 'pts_nuc']
pts_data = []
for c in range(len(types)):
    pts = mat[types[c]][0]
    for ind in range(len(pts)):
        # print(pts_neg[ind])
        if len(pts[ind]) > 0:
            for i in range(len(pts[ind][0])):
                pts_data.append([ind + 1, c, pts[ind][0][i][0], pts[ind][0][i][1]])

new_pts = pd.DataFrame(pts_data, columns=['image_index', 'class', 'x', 'y'])
new_pts['x'] = new_pts['x'] / w
new_pts['y'] = new_pts['y'] / h
new_pts['y'] = 1 - new_pts['y']

# Todo: This is not the proper way! Need to find a better way to convert coordinates
# new_pts['y'] = new_pts['y'] + 0.015

new_pts = new_pts[new_pts['image_index'].isin(replace_range)]
new_pts = new_pts.sort_values('image_index', ascending=True, kind='mergesort')
new_pts = new_pts.reset_index(drop=True)

print(len(new_pts))

# pts_pos = mat['pts_pos']
# pts_nuc = mat['pts_nuc']
# pts_pos_o = mat['pts_pos_o']

old_pts = pd.read_csv(path_to_old_csv, delimiter=' ')
old_pts.drop(old_pts[old_pts['image_index'].isin(replace_range)].index, inplace=True)


old_pts = old_pts.append(new_pts, ignore_index=True)
old_pts = old_pts.sort_values('image_index', ascending=True, kind='mergesort')
old_pts = old_pts.reset_index(drop=True)
# print(new_pts)
print(old_pts)

old_pts.to_csv(path_to_new_csv)