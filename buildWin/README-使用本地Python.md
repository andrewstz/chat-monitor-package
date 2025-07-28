# 使用本地Python 3.10.11创建UV环境

## 快速开始

### 方法一：使用脚本（推荐）
```cmd
# 在buildWin目录运行
.\setup_uv_with_local_python.bat
```

### 方法二：手动命令行操作
```cmd
# 1. 检查Python版本
python --version

# 2. 创建UV环境（使用本地Python）
uv venv --python 3.10.11

# 3. 激活环境
call ..\.venv\Scripts\activate.bat

# 4. 安装依赖（使用国内镜像源）
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil pygame pyinstaller

# 5. 验证安装
python -c "import cv2, ultralytics, pygame; print('环境配置成功！')"
```

## 详细说明

### UV如何使用本地Python

1. **自动检测**：uv会自动检测系统中已安装的Python版本
2. **版本匹配**：`uv venv --python 3.10.11` 会查找系统中已安装的Python 3.10.11
3. **创建虚拟环境**：基于本地Python创建隔离的虚拟环境

### 优势

✅ **无需下载**：不需要从网络下载Python安装包
✅ **快速创建**：直接使用本地Python，速度更快
✅ **版本兼容**：Python 3.10.11与3.10.18基本兼容
✅ **网络友好**：避免网络连接问题

### 验证步骤

```cmd
# 检查Python版本
python --version
# 应该显示: Python 3.10.11

# 检查环境位置
where python
# 应该显示: ..\.venv\Scripts\python.exe

# 验证关键依赖
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import ultralytics; print('Ultralytics:', ultralytics.__version__)"
python -c "import pygame; print('Pygame:', pygame.version.ver)"
```

### 常见问题

#### 问题1：uv找不到Python 3.10.11
**解决方案**：
```cmd
# 方法1：使用系统Python
uv venv --python python

# 方法2：指定完整路径
uv venv --python "C:\Python310\python.exe"

# 方法3：使用python命令
uv venv --python python
```

#### 问题2：依赖安装失败
**解决方案**：
```cmd
# 使用国内镜像源
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ [package_name]

# 或者使用备用镜像
uv pip install -i https://mirrors.aliyun.com/pypi/simple/ [package_name]
```

#### 问题3：权限问题
**解决方案**：
```cmd
# 以管理员身份运行命令提示符
# 或者使用用户安装
uv pip install --user [package_name]
```

### 环境管理

```cmd
# 激活环境
call ..\.venv\Scripts\activate.bat

# 退出环境
deactivate

# 删除环境（重新创建）
rmdir /s /q ..\.venv
uv venv --python 3.10.11
```

### 运行应用

```cmd
# 激活环境
call ..\.venv\Scripts\activate.bat

# 运行主程序
python ..\main_monitor_gui.py

# 或者使用uv run
uv run python ..\main_monitor_gui.py
```

## 总结

使用本地Python 3.10.11创建UV环境是最简单、最可靠的解决方案：

1. **避免网络问题**：不需要下载Python安装包
2. **快速设置**：直接使用现有Python
3. **版本兼容**：3.10.11与3.10.18基本兼容
4. **稳定可靠**：避免网络连接和下载失败问题

推荐使用 `setup_uv_with_local_python.bat` 脚本，它会自动处理所有步骤。 