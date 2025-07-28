# 手动下载Python 3.10.18安装包指南

## 问题描述
在内网环境中，`uv venv --python 3.10.18` 无法从GitHub下载Python安装包，出现网络连接错误。

## 解决方案

### 方法一：手动下载Python安装包

#### 1. 在外网环境下载Python安装包
访问以下链接下载Python 3.10.18的Windows安装包：
- **官方下载链接**：https://www.python.org/downloads/release/python-31018/
- **Windows installer (64-bit)**：https://www.python.org/ftp/python/3.10.18/python-3.10.18-amd64.exe
- **Windows installer (32-bit)**：https://www.python.org/ftp/python/3.10.18/python-3.10.18.exe

#### 2. 传输到内网环境
将下载的安装包传输到Windows内网机器：
- 使用U盘、网络共享或其他文件传输方式
- 确保文件完整性（可以验证SHA256哈希值）

#### 3. 在内网环境安装Python
```cmd
# 安装Python 3.10.18（静默安装）
python-3.10.18-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# 或者交互式安装
python-3.10.18-amd64.exe
```

#### 4. 验证安装
```cmd
python --version
# 应该显示: Python 3.10.18
```

### 方法二：使用离线Python环境

#### 1. 在外网环境创建完整环境
```cmd
# 在外网机器上
uv venv --python 3.10.18
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics Pillow requests PyYAML psutil pygame pyinstaller
```

#### 2. 打包整个环境
```cmd
# 压缩整个.venv目录
tar -czf python31018_env.tar.gz .venv/
# 或者使用zip
powershell Compress-Archive -Path .venv -DestinationPath python31018_env.zip
```

#### 3. 传输到内网环境
将压缩包传输到内网Windows机器，解压后即可使用。

### 方法三：使用conda环境（推荐）

#### 1. 下载Miniconda安装包
- **Miniconda3 Windows 64-bit**：https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

#### 2. 安装Miniconda
```cmd
# 静默安装
Miniconda3-latest-Windows-x86_64.exe /S /D=C:\Miniconda3

# 或者交互式安装
Miniconda3-latest-Windows-x86_64.exe
```

#### 3. 创建Python 3.10.18环境
```cmd
# 创建环境
conda create -n chatmonitor python=3.10.18

# 激活环境
conda activate chatmonitor

# 安装依赖
conda install -c conda-forge opencv pillow requests pyyaml psutil
pip install ultralytics pygame pyinstaller
```

## 推荐方案

### 对于内网环境，推荐使用以下方案：

1. **方案一**：使用国内镜像源（最简单）
   ```cmd
   # 在buildWin目录运行
   .\setup_uv_with_mirror.bat
   ```

2. **方案二**：使用conda环境（最稳定）
   ```cmd
   conda create -n chatmonitor python=3.10.18
   conda activate chatmonitor
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-python ultralytics pillow requests pyyaml psutil pygame pyinstaller
   ```

3. **方案三**：手动下载Python安装包（如果前两种方案都不可行）

## 验证环境

无论使用哪种方案，都可以用以下命令验证环境：

```cmd
python --version
python -c "import cv2, ultralytics, pygame; print('环境配置成功！')"
```

## 注意事项

1. **网络代理**：如果内网有代理服务器，需要配置代理设置
2. **防火墙**：确保防火墙允许Python和pip的网络访问
3. **权限**：某些操作可能需要管理员权限
4. **路径**：确保Python和pip在系统PATH中 