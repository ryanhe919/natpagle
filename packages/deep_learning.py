import os
import cv2

count = 36

TRAIN_DATA_DIR = './train_set/'


def make_train_data(x, y):
    global count
    img = cv2.imread('./images/session.png')
    cv2.imwrite(os.path.join(TRAIN_DATA_DIR, 'train_' + str(count) + '.png'), img)
    with open(os.path.join(TRAIN_DATA_DIR, 'labels.csv'), 'a+') as f:
        f.write('train_' + str(count) + '.png' + ', ' + str(x) + ', ' + str(y) + '\n')
    count += 1
