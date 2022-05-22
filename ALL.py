from ops import *

train_path = './data/tmp/' #경로 마지막에 반드시 '/'를 기입해야합니다.
model_name_list = ['resnet_v1_50', 'resnet_v1_101', 'resnet_v1_152',
                   'resnet_v2_50', 'resnet_v2_101', 'resnet_v2_152',
                   'densenet_121', 'densenet_169', 'densenet_201',
                   'inception_v3', 'inception_v4', 'efficientnet']

epoch = 5

if __name__ == '__main__':
    for model_name in model_name_list:
        fine_tunning = Fine_tunning(train_path=train_path,
                                    model_name=model_name,
                                    epoch=epoch)
        history = fine_tunning.training()
        fine_tunning.save_accuracy(history)