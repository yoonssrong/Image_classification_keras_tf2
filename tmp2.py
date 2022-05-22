import os, glob
import random

PATH = 'D:/project/task1/download/323/'


raw = glob.glob(os.path.join(PATH, '*.jpg'))
raw = [i.replace('\\', '/') for i in raw]
print(raw)
random.shuffle(raw)
print(raw)

# testCnt = int(len(raw) * 0.1)
# valCnt = int(len(raw) * 0.1)
# trainCnt = len(raw) - valCnt - testCnt
#
# print(testCnt)
# print(valCnt)
# print(trainCnt)
#
# print("testCnt")
# for i in range(0, testCnt):
#     print(raw[i])
#
# print("valCnt")
# for i in range(0, valCnt):
#     print(raw[valCnt+i])
#
# print("trainCnt")
# for i in range(0, trainCnt):
#     print(raw[testCnt+valCnt+i])