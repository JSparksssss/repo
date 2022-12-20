from PIL import Image
import os


def gen_img(size=1500, target_dir='.', out_dir='out'):
    """
    :param target_dir: 目标文件夹，默认为当前程序所在位置
    :param size: 图片长宽中较大者缩放后的尺寸，输出图像比例保持不变, 默认保持原始尺寸
    :param out_dir: 保存缩放后图像的文件夹
    :return:
    """
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    files = os.listdir(target_dir)
    img_ext = ['.png', '.jpg', '.gif', '.bmp', '.jpeg']
    for file in files:
        file_path = target_dir + os.sep + file
        ext = os.path.splitext(file)[-1].lower()
        if ext in img_ext:
            new_img = img_resize(file_path, size)
            if new_img.mode == 'RGBA':
                alpha = new_img.split()[3]
                new_img = new_img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
                mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                new_img.paste(255, mask)
                new_img.save(out_dir+os.sep+os.path.splitext(file)[0]+'.gif', transparency=255)
            elif 'transparency' in new_img.info:
                transparency = new_img.info['transparency']
                new_img.save(out_dir+os.sep+os.path.splitext(file)[0]+'.gif', 
                            transparency=transparency)
            else:
                new_img.save(out_dir+os.sep+os.path.splitext(file)[0]+'.gif')


def img_resize(file, size=0):
    img = Image.open(file)
    if size == 0:
        scale = 1
    else: 
        scale = max(img.size) / size
    (width, height) = (int(img.width / scale), int(img.height / scale))
    img2 = img.resize((width, height))
    return img2


# 将程序所在位置下的图像等比例缩放，规则为长宽中较长边缩放成第一个参数值，默认保存到当前位置下的 out 文件夹中
gen_img()
