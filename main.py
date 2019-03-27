from PIL import Image
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.models import load_model
import matplotlib.pyplot as plt
from array import array
import os,sys
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import make_captcha,solve_it
import crawler

def remove_file(train_img_path):
    data_list = os.listdir(train_img_path)
    for file in data_list:
        os.remove(train_img_path + file)

def get_my_train_img(times):
    for i in range(times):
        name,mig = make_captcha.get_train_img()
        mig = solve_it.clear_train_img(mig)
        mig.save('real_do_img/{}.png'.format(name))


def get_my_test_img(times):
    for i in range(times):
        name,mig = make_captcha.get_train_img()
        mig = solve_it.clear_train_img(mig)
        mig.save('test_imgs/{}.png'.format(name))

# get_my_train_img(500)
# get_my_test_img(50)

def get_xy():
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    train_img_path = 'train_imgs/'
    test_img_path = 'test_imgs/'
    data_list = os.listdir(train_img_path)
    data_list1 = os.listdir(test_img_path)
    for file in data_list:
        if file != '.DS_Store':
            img = Image.open(train_img_path + file)
            x = make_captcha.get_mode(img)
            x_train.append(x)
            y_train.append(ord(file[0])-65)

    for file in data_list1:
        if file != '.DS_Store':
            img = Image.open(test_img_path + file)
            x = make_captcha.get_mode(img)
            x_test.append(x)
            y_test.append(ord(file[0])-65)
    return map(np.array,[x_train,y_train,x_test,y_test])


def train_model():
    x_train,y_train,x_test,y_test = get_xy()
    a = np.array([x_train,y_train,x_test,y_test])
    np.save("npmode/xytt.npy",a)

    x_train,y_train,x_test,y_test = np.load("npmode/xytt.npy").tolist()
    x_train = x_train.reshape(x_train.shape[0],-1)
    x_test = x_test.reshape(x_test.shape[0],-1)
    # print(x_train.shape,y_train.shape)


    y_train = np_utils.to_categorical(y_train,num_classes=26)
    y_test = np_utils.to_categorical(y_test,num_classes=26)


    # 训练完成 导入模型
    model = load_model('model.h5')


    # 全连接模型
    # model = Sequential()


    # model.add(Dense(units=256,input_dim=960,bias_initializer='one',activation='tanh'))
    # model.add(Dropout(0.2))
    # model.add(Dense(units=128,activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Dense(units=26,activation='softmax'))

    # model.summary()

    # 损失函数使用交叉熵
    sgd = SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy',
            optimizer=sgd,
            metrics=['accuracy'])
    #模型估计
    model.fit(x_train, y_train, epochs=10, batch_size=64)
    loss,accuracy = model.evaluate(x_test,y_test)
    print('loss:',loss)
    print('accuracy:',accuracy)

    model.save('model.h5')


for i in range(601):
    # try:
    crawler.trains(120)
    train_model()
    if i%3 == 0:
        remove_file('train_imgs/')
        remove_file('test_imgs/')
    # except Exception as e:
    #     print(e)
    #     f = open('log.txt','a')
    #     f.write(str(e) + '\n')
    #     f.close()
