import solve_it.cut_img
import solve_it.de_line
import solve_it.de_point


def mode_img(mode,background=None):
    return solve_it.cut_img.mode_to_img(mode,background=None)

def mode_white_img(mode):
    return solve_it.cut_img.mode_to_img(mode,background=255)

def dele_noise(image, N, Z):
    return solve_it.de_point.clear_noise(image, N, Z)

def dele_line(image, N, pans=None):
    return solve_it.de_line.clear_line(image, N, pans=None)

def clear_train_img(image):
    return solve_it.de_line.clear_my_train_img(image)

def clear_lib_line(image):
    return solve_it.de_line.clear_my_line(image)

def cut_img_to_mode_list(image,max_width):
    return solve_it.cut_img.cut_img(image,max_width)

def cut_img_to_img_list(image,max_width,background=None):
    if background:
        mode_list = solve_it.cut_img.cut_img(image,max_width)
        return map(mode_white_img,mode_list)
    else:
        img_mode_list = solve_it.cut_img.cut_img(image,max_width)
        return map(mode_img,img_mode_list)