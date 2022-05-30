from PIL import Image
import make_captcha.noise
import make_captcha.make_capt

# 图像转化为01 np数组 Threshold为阀值
def get_mode(img,Threshold=100):
    return make_captcha.make_capt.get_modes(img,Threshold)


# 将01 np数组转化为黑白图片
def mode_to_img(mode):
    return make_captcha.noise.mode_to_draw(mode)


# 将np数组噪点处理，mode 数组，N是加噪率（边缘存在1个以上的黑点那么这个点有一点概率变黑） Z 加噪次数 返回数组
def show_noise_mode(mode, N, Z):
    return make_captcha.noise.more_noise(mode, N, Z)


# 将np数组噪点处理，mode 数组，N是加噪率（边缘存在1个以上的黑点那么这个点有一点概率变黑） Z 加噪次数 返回图片
def show_noise_img(mode, N, Z):
    return make_captcha.noise.more_noise(mode, N, Z, to_img='toimg')


# 偏移 传入np数组，横向偏移(默认右移)，纵向偏移，传出新的mode
def mode_pan(mode,width_x,height_y):
    return make_captcha.make_capt.img_pan(mode,width_x,height_y)


# 生成验证码 长宽 字符串个数 背景颜色 一般要上线用的话看源码改一改就好了
def make_capt_img(width,height,num_of_str,gray_value=255):
    return make_captcha.make_capt.get_captcha(
        width, height, num_of_str, gray_value=255
    )


# 生成简单的大写字母训练集图片
def get_train_img():
    file_name,image = make_captcha.make_capt.make_captcha.make_capt.train_img()
    return file_name,image

# 自定义生成训练图片
# def my_train_img():
