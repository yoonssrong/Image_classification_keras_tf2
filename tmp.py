import os, glob
import shutil
import random


PATH = 'F:/banet/b/(1)select_partitioning/' #폴더안에 폴더가 있어야됨

folderList = os.listdir(PATH)
print(folderList)
folder = folderList[0]
print(folder)

for folder in folderList:
    raw = glob.glob(os.path.join(PATH, folder, '*.png'))
    raw = [i.replace('\\', '/') for i in raw]
    random.shuffle(raw)

    testCnt = int(len(raw) * 0.1)
    valCnt = int(len(raw) * 0.1)
    trainCnt = len(raw) - valCnt - testCnt

    if not os.path.isdir(PATH + folder + '/' + 'train/'):
        os.mkdir(PATH + folder + '/' + 'train/')
    if not os.path.isdir(PATH + folder + '/' + 'validation/'):
        os.mkdir(PATH + folder + '/' + 'validation/')
    if not os.path.isdir(PATH + folder + '/' + 'test/'):
        os.mkdir(PATH + folder + '/' + 'test/')

    [shutil.move(raw[i], PATH + folder + '/' + 'test/') for i in range(0, testCnt)]
    [shutil.move(raw[valCnt+i], PATH + folder + '/' + 'validation/') for i in range(0, valCnt)]
    [shutil.move(raw[testCnt+valCnt+i], PATH + folder + '/' + 'train/') for i in range(0, trainCnt)]

print("Finish!")