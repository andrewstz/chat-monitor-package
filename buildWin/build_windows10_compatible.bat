@echo off
echo 正在构建Windows 10兼容版本...

REM 激活虚拟环境
call ..\.venv\Scripts\activate.bat

REM 清理之前的构建
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM 安装兼容的依赖版本
echo 安装兼容的依赖包...
uv pip install opencv-python==4.8.1.78 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install numpy==1.24.3 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install ultralytics==8.0.196 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install Pillow==10.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install requests==2.31.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install PyYAML==6.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install psutil==5.9.5 -i https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install lap==0.4.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/

REM 安装PyInstaller
uv pip install pyinstaller==5.13.2 -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo 开始打包...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name ChatMonitor ^
    --add-data "..\sounds;sounds" ^
    --add-data "..\models;models" ^
    --add-data "..\config_with_yolo.yaml;." ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import ultralytics ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageTk ^
    --hidden-import requests ^
    --hidden-import yaml ^
    --hidden-import psutil ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import threading ^
    --hidden-import queue ^
    --hidden-import time ^
    --hidden-import os ^
    --hidden-import sys ^
    --hidden-import json ^
    --hidden-import re ^
    --hidden-import subprocess ^
    --hidden-import platform ^
    --hidden-import socket ^
    --hidden-import urllib3 ^
    --hidden-import charset_normalizer ^
    --hidden-import idna ^
    --hidden-import certifi ^
    --collect-all numpy ^
    --collect-all cv2 ^
    --collect-all ultralytics ^
    --collect-all PIL ^
    --collect-all requests ^
    --collect-all yaml ^
    --collect-all psutil ^
    --collect-all tkinter ^
    --collect-all lap ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module pandas ^
    --exclude-module jupyter ^
    --exclude-module IPython ^
    --exclude-module notebook ^
    --exclude-module sphinx ^
    --exclude-module docutils ^
    --exclude-module setuptools ^
    --exclude-module pip ^
    --exclude-module wheel ^
    --exclude-module pkg_resources ^
    --exclude-module distutils ^
    --exclude-module unittest ^
    --exclude-module test ^
    --exclude-module tests ^
    --exclude-module _pytest ^
    --exclude-module pytest ^
    --exclude-module tox ^
    --exclude-module coverage ^
    --exclude-module flake8 ^
    --exclude-module black ^
    --exclude-module isort ^
    --exclude-module mypy ^
    --exclude-module pylint ^
    --exclude-module autopep8 ^
    --exclude-module yapf ^
    --exclude-module bandit ^
    --exclude-module safety ^
    --exclude-module pipdeptree ^
    --exclude-module pip-tools ^
    --exclude-module pipenv ^
    --exclude-module poetry ^
    --exclude-module conda ^
    --exclude-module anaconda ^
    --exclude-module miniconda ^
    --exclude-module virtualenv ^
    --exclude-module venv ^
    --exclude-module pyenv ^
    --exclude-module asdf ^
    --exclude-module rtx ^
    --exclude-module direnv ^
    --exclude-module autoenv ^
    --exclude-module dotenv ^
    --exclude-module python-dotenv ^
    --exclude-module python-decouple ^
    --exclude-module dynaconf ^
    --exclude-module hydra ^
    --exclude-module omegaconf ^
    --exclude-module pydantic ^
    --exclude-module pydantic-settings ^
    --exclude-module pydantic-v1 ^
    --exclude-module pydantic-v2 ^
    --exclude-module marshmallow ^
    --exclude-module cerberus ^
    --exclude-module voluptuous ^
    --exclude-module jsonschema ^
    --exclude-module json-schema ^
    --exclude-module json-spec ^
    --exclude-module jsonpath ^
    --exclude-module jsonpath-ng ^
    --exclude-module jsonpath-rw ^
    --exclude-module jsonpath-rw-ext ^
    --exclude-module jsonpointer ^
    --exclude-module jsonpatch ^
    --exclude-module jsonmerge ^
    --exclude-module jsonmerge-python ^
    --exclude-module json-schema-validator ^
    --exclude-module json-schema-generator ^
    --exclude-module json-schema-draft ^
    --exclude-module json-schema-draft4 ^
    --exclude-module json-schema-draft6 ^
    --exclude-module json-schema-draft7 ^
    --exclude-module json-schema-draft2019-09 ^
    --exclude-module json-schema-draft2020-12 ^
    --exclude-module json-schema-draft-next ^
    --exclude-module json-schema-draft-next-2020-12 ^
    --exclude-module json-schema-draft-next-2019-09 ^
    --exclude-module json-schema-draft-next-2019-09-1 ^
    --exclude-module json-schema-draft-next-2019-09-2 ^
    --exclude-module json-schema-draft-next-2019-09-3 ^
    --exclude-module json-schema-draft-next-2019-09-4 ^
    --exclude-module json-schema-draft-next-2019-09-5 ^
    --exclude-module json-schema-draft-next-2019-09-6 ^
    --exclude-module json-schema-draft-next-2019-09-7 ^
    --exclude-module json-schema-draft-next-2019-09-8 ^
    --exclude-module json-schema-draft-next-2019-09-9 ^
    --exclude-module json-schema-draft-next-2019-09-10 ^
    --exclude-module json-schema-draft-next-2019-09-11 ^
    --exclude-module json-schema-draft-next-2019-09-12 ^
    --exclude-module json-schema-draft-next-2019-09-13 ^
    --exclude-module json-schema-draft-next-2019-09-14 ^
    --exclude-module json-schema-draft-next-2019-09-15 ^
    --exclude-module json-schema-draft-next-2019-09-16 ^
    --exclude-module json-schema-draft-next-2019-09-17 ^
    --exclude-module json-schema-draft-next-2019-09-18 ^
    --exclude-module json-schema-draft-next-2019-09-19 ^
    --exclude-module json-schema-draft-next-2019-09-20 ^
    --exclude-module json-schema-draft-next-2019-09-21 ^
    --exclude-module json-schema-draft-next-2019-09-22 ^
    --exclude-module json-schema-draft-next-2019-09-23 ^
    --exclude-module json-schema-draft-next-2019-09-24 ^
    --exclude-module json-schema-draft-next-2019-09-25 ^
    --exclude-module json-schema-draft-next-2019-09-26 ^
    --exclude-module json-schema-draft-next-2019-09-27 ^
    --exclude-module json-schema-draft-next-2019-09-28 ^
    --exclude-module json-schema-draft-next-2019-09-29 ^
    --exclude-module json-schema-draft-next-2019-09-30 ^
    --exclude-module json-schema-draft-next-2019-09-31 ^
    --exclude-module json-schema-draft-next-2019-09-32 ^
    --exclude-module json-schema-draft-next-2019-09-33 ^
    --exclude-module json-schema-draft-next-2019-09-34 ^
    --exclude-module json-schema-draft-next-2019-09-35 ^
    --exclude-module json-schema-draft-next-2019-09-36 ^
    --exclude-module json-schema-draft-next-2019-09-37 ^
    --exclude-module json-schema-draft-next-2019-09-38 ^
    --exclude-module json-schema-draft-next-2019-09-39 ^
    --exclude-module json-schema-draft-next-2019-09-40 ^
    --exclude-module json-schema-draft-next-2019-09-41 ^
    --exclude-module json-schema-draft-next-2019-09-42 ^
    --exclude-module json-schema-draft-next-2019-09-43 ^
    --exclude-module json-schema-draft-next-2019-09-44 ^
    --exclude-module json-schema-draft-next-2019-09-45 ^
    --exclude-module json-schema-draft-next-2019-09-46 ^
    --exclude-module json-schema-draft-next-2019-09-47 ^
    --exclude-module json-schema-draft-next-2019-09-48 ^
    --exclude-module json-schema-draft-next-2019-09-49 ^
    --exclude-module json-schema-draft-next-2019-09-50 ^
    --exclude-module json-schema-draft-next-2019-09-51 ^
    --exclude-module json-schema-draft-next-2019-09-52 ^
    --exclude-module json-schema-draft-next-2019-09-53 ^
    --exclude-module json-schema-draft-next-2019-09-54 ^
    --exclude-module json-schema-draft-next-2019-09-55 ^
    --exclude-module json-schema-draft-next-2019-09-56 ^
    --exclude-module json-schema-draft-next-2019-09-57 ^
    --exclude-module json-schema-draft-next-2019-09-58 ^
    --exclude-module json-schema-draft-next-2019-09-59 ^
    --exclude-module json-schema-draft-next-2019-09-60 ^
    --exclude-module json-schema-draft-next-2019-09-61 ^
    --exclude-module json-schema-draft-next-2019-09-62 ^
    --exclude-module json-schema-draft-next-2019-09-63 ^
    --exclude-module json-schema-draft-next-2019-09-64 ^
    --exclude-module json-schema-draft-next-2019-09-65 ^
    --exclude-module json-schema-draft-next-2019-09-66 ^
    --exclude-module json-schema-draft-next-2019-09-67 ^
    --exclude-module json-schema-draft-next-2019-09-68 ^
    --exclude-module json-schema-draft-next-2019-09-69 ^
    --exclude-module json-schema-draft-next-2019-09-70 ^
    --exclude-module json-schema-draft-next-2019-09-71 ^
    --exclude-module json-schema-draft-next-2019-09-72 ^
    --exclude-module json-schema-draft-next-2019-09-73 ^
    --exclude-module json-schema-draft-next-2019-09-74 ^
    --exclude-module json-schema-draft-next-2019-09-75 ^
    --exclude-module json-schema-draft-next-2019-09-76 ^
    --exclude-module json-schema-draft-next-2019-09-77 ^
    --exclude-module json-schema-draft-next-2019-09-78 ^
    --exclude-module json-schema-draft-next-2019-09-79 ^
    --exclude-module json-schema-draft-next-2019-09-80 ^
    --exclude-module json-schema-draft-next-2019-09-81 ^
    --exclude-module json-schema-draft-next-2019-09-82 ^
    --exclude-module json-schema-draft-next-2019-09-83 ^
    --exclude-module json-schema-draft-next-2019-09-84 ^
    --exclude-module json-schema-draft-next-2019-09-85 ^
    --exclude-module json-schema-draft-next-2019-09-86 ^
    --exclude-module json-schema-draft-next-2019-09-87 ^
    --exclude-module json-schema-draft-next-2019-09-88 ^
    --exclude-module json-schema-draft-next-2019-09-89 ^
    --exclude-module json-schema-draft-next-2019-09-90 ^
    --exclude-module json-schema-draft-next-2019-09-91 ^
    --exclude-module json-schema-draft-next-2019-09-92 ^
    --exclude-module json-schema-draft-next-2019-09-93 ^
    --exclude-module json-schema-draft-next-2019-09-94 ^
    --exclude-module json-schema-draft-next-2019-09-95 ^
    --exclude-module json-schema-draft-next-2019-09-96 ^
    --exclude-module json-schema-draft-next-2019-09-97 ^
    --exclude-module json-schema-draft-next-2019-09-98 ^
    --exclude-module json-schema-draft-next-2019-09-99 ^
    --exclude-module json-schema-draft-next-2019-09-100 ^
    ..\main_monitor_gui_app.py

echo 构建完成！
echo 生成的文件在 dist\ChatMonitor.exe
pause 