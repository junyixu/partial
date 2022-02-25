#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 junyi <junyi@junyixu0@gmail.com>
# Distributed under terms of the MIT license.
#
#
# TODO
# 1. how to get cursor position
#  我惊奇地发现我把 vim 的 [col("."), line(".")] 给 [x, y] 就行了，这是巧合？不明白为什么
# 2. png 黑色背景 白色文字
#   背景可以用 \pagecolor，文字颜色用什么呢？
# 3. png 大小
#   如果在光标附近，需要根据屏幕上还剩下的距离调整图片的大小，很麻烦
"""
ueberzug
"""

import ueberzug.lib.v0 as ueberzug
import time
import os, sys
import shutil
import subprocess

HOME = os.environ['HOME']
SRC = HOME + '/.vim/scripts/latex_img'
DST = '/tmp/latex_img'
main_filename = 'main'
main_tex = main_filename + '.tex'
main_png = main_filename + '.png'
TIME = 10


def concatenate(main_tex):
    """
    模仿 /usr/bin/cat 连接文件
    """
    if os.path.exists(main_tex):
        os.remove(main_tex)
    with open(main_tex, "a") as f_out:
        for file in ['before.tex', 'formula.txt', 'after.tex']:
            with open(file, "r") as f:
                f_out.write(f.read())


def present(main_png, ns, position=[0, 0]):
    """
    把图片展示出来
    Usage:
        present('xxx.png', how many seconds?, [x, y])
    """
    with ueberzug.Canvas() as c:
        demo = c.create_placement('demo',
                                  x=position[0],
                                  y=position[1],
                                  scaler=ueberzug.ScalerOption.COVER.value)
        demo.path = main_png
        demo.visibility = ueberzug.Visibility.VISIBLE

        with c.lazy_drawing:
            demo.path = main_png
        time.sleep(ns)


if __name__ == '__main__':
    if not os.path.exists(DST):
        shutil.copytree(SRC, DST)
        exit()  # TODO 如果解决 fomular.txt 在没有目录时候不能写的问题

    os.chdir(DST)

    concatenate(main_tex)

    latex_compiling = subprocess.run(
        ['latex', '-shell-escape', 'main.tex'],
        shell=False)  # shell should be set to False
    if latex_compiling.returncode == 0:  # succeed!
        if len(sys.argv) > 1:
            x = int(sys.argv[1])
            y = int(sys.argv[2])
            present(main_png, TIME, [x, y])
        else:
            present(main_png, TIME)
    else:  # failed!
        present('error.png', 1)
