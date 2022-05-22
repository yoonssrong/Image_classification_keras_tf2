#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt #모형 학습시 accuracy와 loss를 저장하기 위한 라이브러리입니다.

"""시드 고정을 위한 라이브러리"""
import random
import numpy as np

"""전처리를 위한 라이브러리"""
import os
import pandas as pd

"""Keras 라이브러리"""
import tensorflow.keras as keras #keras 라이브러리입니다.
from tensorflow.keras.preprocessing.image import ImageDataGenerator #이미지 데이터를 tensor로 변한하기 위해 활용되는 라이브러리입니다.
from tensorflow.keras.layers import Dense #학습 모형을 구축하기 위해 활용되는 라이브러리입니다.
from tensorflow.keras import Sequential #학습 모형을 구축하기 위해 활용되는 라이브러리 입니다.

from tensorflow.keras.applications.resnet import ResNet50, ResNet101, ResNet152
from tensorflow.keras.applications.resnet_v2 import ResNet50V2, ResNet101V2, ResNet152V2
from tensorflow.keras.applications.densenet import DenseNet121, DenseNet169, DenseNet201
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.applications.efficientnet import EfficientNetB0
from tensorflow.keras.utils import multi_gpu_model
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf
import tensorflow.keras.backend as K


seed = 2

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

class Import_data:
    def __init__(self, train_path):
        self.train_path = train_path

    def train(self):
        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           featurewise_std_normalization=True,
                                           zoom_range=0.2,
                                           channel_shift_range=0.1,
                                           rotation_range=20,
                                           width_shift_range=0.2,
                                           height_shift_range=0.2,
                                           horizontal_flip=True,
                                           validation_split=0.2
                                           )
        train_generator = train_datagen.flow_from_directory(
            self.train_path,
            target_size=(224, 224),
            batch_size=8,
            # interpolation = 'box',
            # class_mode='categorical',
            subset='training'
        )
        val_generator = train_datagen.flow_from_directory(
            self.train_path,
            target_size=(224, 224),
            batch_size=8,
            subset='validation'
        )

        return train_generator, val_generator

class Load_model:
    def __init__(self, train_path, model_name):
        self.num_class = len(os.listdir(train_path))
        self.model_name = model_name

    def resnet_v1_50(self):
        network = ResNet50(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                           pooling='avg')
        return network

    def resnet_v1_101(self):
        network = ResNet101(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                            pooling='avg')
        return network

    def resnet_v1_152(self):
        network = ResNet152(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                            pooling='avg')
        return network

    def resnet_v2_50(self):
        network = ResNet50V2(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                             pooling='avg')
        return network

    def resnet_v2_101(self):
        network = ResNet101V2(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg')
        return network

    def resnet_v2_152(self):
        network = ResNet152V2(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg')
        return network

    def densenet_121(self):
        network = DenseNet121(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg')
        return network

    def densenet_169(self):
        network = DenseNet169(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg')
        return network

    def densenet_201(self):
        network = DenseNet201(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg')
        return network

    def inception_v3(self):
        network = InceptionV3(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg')
        return network

    def inception_v4(self):
        network = InceptionResNetV2(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                                    pooling='avg')
        return network

    def efficientnet(self):
        network = EfficientNetB0(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                                 pooling='avg')
        return network


    def build_network(self):
        if self.model_name == 'resnet_v1_50':
            network = self.resnet_v1_50()
        elif self.model_name == 'resnet_v1_101':
            network = self.resnet_v1_101()
        elif self.model_name == 'resnet_v1_152':
            network = self.resnet_v1_152()
        elif self.model_name == 'resnet_v2_50':
            network = self.resnet_v2_50()
        elif self.model_name == 'resnet_v2_101':
            network = self.resnet_v2_101()
        elif self.model_name == 'resnet_v2_152':
            network = self.resnet_v2_152()
        elif self.model_name == 'densenet_121':
            network = self.densenet_121()
        elif self.model_name == 'densenet_169':
            network = self.densenet_169()
        elif self.model_name == 'densenet_201':
            network = self.densenet_201()
        elif self.model_name == 'inception_v3':
            network = self.inception_v3()
        elif self.model_name == 'inception_v4':
            network = self.inception_v4()
        elif self.model_name == 'efficientnet':
            network = self.efficientnet()

        model = Sequential()
        model.add(network)
        model.add(Dense(2048, activation='relu'))
        model.add(Dense(self.num_class, activation='softmax'))
        model.summary()

        return model

class Fine_tunning:
    def __init__(self, train_path, model_name, epoch, multi_gpu=0):
        self.data = Import_data(train_path)
        self.train_data, self.val_data = self.data.train()
        self.load_model = Load_model(train_path, model_name)
        self.multi_gpu = multi_gpu
        self.epoch = epoch
        self.model_name = model_name
        self.train_path = train_path

    def training(self):
        data_name = self.train_path.split('/')
        data_name = data_name[len(data_name)-2]
        optimizer = tf.keras.optimizers.SGD(learning_rate=0.001, decay=1e-5, momentum=0.999, nesterov=True)
        model = self.load_model.build_network()
        save_folder = './model_saved/' + data_name + '/' + self.model_name + '_' + str(self.epoch) + '/'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        check_point = ModelCheckpoint(save_folder + 'model-{epoch:03d}-{acc:03f}-{val_acc:03f}.h5', verbose=1,
                                      monitor='val_acc', save_best_only=True, mode='auto')
        if self.multi_gpu==0:
            model.compile(loss='categorical_crossentropy',
                          optimizer=optimizer,
                          metrics=['acc'])
            history = model.fit_generator(
                self.train_data,
                steps_per_epoch=self.train_data.samples / self.train_data.batch_size,
                epochs=self.epoch,
                validation_data=self.val_data,
                validation_steps=self.val_data.samples / self.val_data.batch_size,
                callbacks=[check_point],
                verbose=1)
        else:
            with tf.device('/cpu:0'):
                cpu_model = model
            model = multi_gpu_model(cpu_model, gpus=self.multi_gpu)
            model.summary()
            model.compile(loss='categorical_crossentropy',
                          optimizer=optimizer,
                          metrics=['acc'])
            history = model.fit_generator(
                self.train_data,
                steps_per_epoch=self.train_data.samples / self.train_data.batch_size,
                epochs=self.epoch,
                validation_data=self.val_data,
                validation_steps=self.val_data.samples / self.val_data.batch_size,
                callbacks=[check_point],
                verbose=1)
        return history

    def save_accuracy(self, history):
        data_name = self.train_path.split('/')
        data_name = data_name[len(data_name)-2]
        save_folder = './model_saved/' + data_name + '/' + self.model_name + '_' + str(self.epoch) + '/'
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs = range(len(acc))
        epoch_list = list(epochs)

        df = pd.DataFrame({'epoch': epoch_list, 'train_accuracy': acc, 'validation_accuracy': val_acc},
                          columns=['epoch', 'train_accuracy', 'validation_accuracy'])
        df_save_path = save_folder + 'accuracy.csv'
        df.to_csv(df_save_path, index=False, encoding='euc-kr')

        plt.plot(epochs, acc, 'b', label='Training acc')
        plt.plot(epochs, val_acc, 'r', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.legend()
        save_path = save_folder + 'accuracy.png'
        plt.savefig(save_path)
        plt.cla()

        plt.plot(epochs, loss, 'b', label='Training loss')
        plt.plot(epochs, val_loss, 'r', label='Validation loss')
        plt.title('Training and validation loss')
        plt.legend()
        save_path = save_folder + 'loss.png'
        plt.savefig(save_path)
        plt.cla()

        name_list = os.listdir(save_folder)
        h5_list = []
        for name in name_list:
            if '.h5' in name:
                h5_list.append(name)
        h5_list.sort()
        h5_list = [save_folder + name for name in h5_list]
        for path in h5_list[:len(h5_list) - 1]:
            os.remove(path)
        K.clear_session()
