import numpy as np
import os

def dump(file_name):
    arr = np.load(file_name)
    arr = arr.ravel()
    fh = open(file_name[:-4] + '.score', 'w')
    for row in xrange(len(arr)):
        fh.write(str(arr[row]))
        fh.write('\n')
    fh.close()

# date_time = '-2016-07-01.npy'
# for i in xrange(20):
#     dump('../../data/res/dbqa/train-epoch' + str(i) + date_time)
#
# dump('../../data/res/dbqa/val' + date_time)
# dump('../../data/res/dbqa/val-answer' + date_time)
# dump('../../data/res/dbqa/test' + date_time)

for parent, dir_names, file_names in os.walk('../../data/res/dbqa/'):
    for name in file_names:
        if name.endswith('.npy'):
            dump(os.path.join(parent, name))
