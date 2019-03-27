import solve_it.cut_img
import solve_it.de_line
import solve_it.de_point


def mode_img(mode,background=None):
    img = solve_it.cut_img.mode_to_img(mode,background=None)
    return img

def mode_white_img(mode):
    img = solve_it.cut_img.mode_to_img(mode,background=255)
    return img

def dele_noise(image, N, Z):
    img = solve_it.de_point.clear_noise(image, N, Z)
    return img

def dele_line(image, N, pans=None):
    img = solve_it.de_line.clear_line(image, N, pans=None)
    return img

def clear_train_img(image):
    img = solve_it.de_line.clear_my_train_img(image)
    return img

def clear_lib_line(image):
    img = solve_it.de_line.clear_my_line(image)
    return img

def cut_img_to_mode_list(image,max_width):
    img_mode_list = solve_it.cut_img.cut_img(image,max_width)
    return img_mode_list

def cut_img_to_img_list(image,max_width,background=None):
    if background:
        mode_list = solve_it.cut_img.cut_img(image,max_width)
        img_list = map(mode_white_img,mode_list)
        return img_list
    else:
        img_mode_list = solve_it.cut_img.cut_img(image,max_width)
        return map(mode_img,img_mode_list)