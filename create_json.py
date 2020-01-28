#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS
import os
import json
import collections as cl
import time

def get_exif_of_image(file):
    img = Image.open(file)

    try:
        exif = img._getexif()
    except AttributeError:
        return -1

    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value
    return exif_table

def get_exif_rotation(orientation_num):
    if orientation_num == 0:
        return 0
    elif orientation_num == 1:
        return 0
    elif orientation_num == 2:
        return 0
    elif orientation_num == 3:
        return 180
    elif orientation_num == 4:
        return 180
    elif orientation_num == 5:
        return 270
    elif orientation_num == 6:
        return 270
    elif orientation_num == 7:
        return 90
    elif orientation_num == 8:
        return 90
    else:
        return 0


def rotation_img(exif, path, source_dir):
    to_save_path = source_dir + '\\' + path

    if exif == -1:
        rotate = 0
    elif 'Orientation' in exif:
        rotate = get_exif_rotation(exif['Orientation'])
    else:
        rotate = 0

    if rotate != 0:
        with Image.open(source_dir + path) as img:
            data = img.getdata()
            mode = img.mode
            size = img.size

            with Image.new(mode, size) as dst:
                dst.putdata(data)                    
                dst = dst.rotate(rotate, expand=True)
                dst.save(to_save_path)

    return 0


def main():
    #while(1):
        source_dir = 'a' # Dropboxと連携して写真が保存されるフォルダ
        img_list_file = 'imgList.json' # 写真リスト

        with open(img_list_file, mode='r') as f:
            file_datas = json.load(f)
            img_jsons = [a["src"] for a in file_datas]

        imgs = os.listdir(source_dir)

        if len(img_jsons) > 0:
            add_imgs = list(set(imgs) - set(img_jsons))
        else:
            add_imgs = imgs

        if len(add_imgs) > 0:
            print("a")
            # 画像を回転させる
        #     for img_path in add_imgs:
        #         try:
        #             exif = get_exif_of_image(source_dir + '\\' + img_path)
        #         except:
        #             os.remove(source_dir + '\\' + img_path)
        #             imgs.remove(img_path)
        #             print('remove')
        #         else:
        #             rotation_img(exif, img_path, source_dir)

        add_jsons = []
        for i in range(len(imgs)):
            imgData = cl.OrderedDict()
            imgData["src"] = imgs[i]
            add_jsons.append(imgData)
        print(add_jsons)

        if len(add_imgs) > 0:
            with open(img_list_file, mode='w') as f:
                json.dump(add_jsons, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                print('write')

        # time.sleep(1)


if __name__ == '__main__':
    main()