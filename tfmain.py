from PIL import Image
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.models import load_model
from array import array
import os,sys
import numpy as np
from PIL import Image
from io import BytesIO
import requests

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



import make_captcha,solve_it




# 导入模型
model = load_model('model.h5')

# 图像处理
def test_lib_img():
    url = 'http://210.35.251.243/reader/captcha.php'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img



def chr_num(num):
    return chr(num+65)

def pred_ans(mode):
    x_test = mode.reshape(mode.shape[0],-1)
    ans = model.predict_classes(x_test)
    return ans


def break_capt(img):
    img = solve_it.dele_noise(img, N=2, Z=1)
    img = solve_it.clear_lib_line(img)
    # img.show()
    mode_list = solve_it.cut_img_to_mode_list(img,30)

    test_x = np.array(mode_list)
    ans = pred_ans(test_x)
    res = ''.join(map(chr_num,ans.tolist()))
    return res

# img.show()
# print(break_capt(img))