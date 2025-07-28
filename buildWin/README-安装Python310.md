# 手动安装Python 3.10.11指南

## 方法一：使用自动安装脚本（推荐）

```cmd
# 在buildWin目录运行
.\install_python310.bat
```

## 方法二：手动下载安装

### 步骤1：下载Python 3.10.11

1. **访问官方下载页面**：
   - 链接：https://www.python.org/downloads/release/python-31011/

2. **下载Windows安装包**：
   - **64位系统**：https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
   - **32位系统**：https://www.python.org/ftp/python/3.10.11/python-3.10.11.exe

3. **保存到本地**：
   - 将文件保存到 `buildWin` 目录
   - 文件名：`python-3.10.11-amd64.exe`

### 步骤2：安装Python 3.10.11

#### 选项A：静默安装（推荐）
```cmd
# 在buildWin目录运行
python-3.10.11-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
```

#### 选项B：交互式安装
```cmd
# 双击运行安装包
python-3.10.11-amd64.exe
```

**安装选项**：
- ✅ **Add Python 3.10 to PATH**（重要！）
- ✅ **Install for all users**
- ✅ **Install pip**
- ❌ **Install test suite**（可选）

### 步骤3：验证安装

```cmd
# 检查Python版本
python --version
# 应该显示: Python 3.10.11

# 检查pip
pip --version

# 检查Python路径
where python
```

## 方法三：使用conda安装

如果您已经安装了Anaconda或Miniconda：

```cmd
# 创建Python 3.10.11环境
conda create -n python310 python=3.10.11

# 激活环境
conda activate python310

# 验证版本
python --version
```

## 安装后的配置

### 1. 设置环境变量
确保Python在系统PATH中：
```cmd
# 检查PATH
echo %PATH% | findstr python

# 如果没有，手动添加到PATH
# 通常路径：C:\Users\[用户名]\AppData\Local\Programs\Python\Python310\
```

### 2. 升级pip
```cmd
python -m pip install --upgrade pip
```

### 3. 配置pip镜像源
```cmd
# 创建pip配置文件
mkdir %USERPROFILE%\pip
echo [global] > %USERPROFILE%\pip\pip.conf
echo index-url = https://pypi.tuna.tsinghua.edu.cn/simple/ >> %USERPROFILE%\pip\pip.conf
```

## 验证安装

### 基本验证
```cmd
# 检查Python版本
python --version

# 检查pip
pip --version

# 测试Python
python -c "print('Python 3.10.11 installed successfully!')"
```

### 功能验证
```cmd
# 测试基本功能
python -c "import sys; print('Python path:', sys.executable)"
python -c "import pip; print('Pip version:', pip.__version__)"
```

## 常见问题

### 问题1：Python不在PATH中
**解决方案**：
```cmd
# 方法1：重新安装并勾选"Add to PATH"
# 方法2：手动添加到PATH环境变量
# 方法3：使用完整路径
C:\Users\[用户名]\AppData\Local\Programs\Python\Python310\python.exe --version
```

### 问题2：权限问题
**解决方案**：
```cmd
# 以管理员身份运行命令提示符
# 或者使用用户安装
python-3.10.11-amd64.exe /quiet InstallAllUsers=0 PrependPath=1
```

### 问题3：下载失败
**解决方案**：
1. 使用VPN或代理
2. 使用国内镜像源
3. 手动下载安装包

## 安装完成后的下一步

1. **重启命令提示符**
2. **验证Python安装**：
   ```cmd
   python --version
   ```
3. **创建UV环境**：
   ```cmd
   .\setup_uv_with_local_python.bat
   ```

## 总结

安装Python 3.10.11后，您就可以：
- ✅ 使用 `uv venv --python 3.10.11` 创建虚拟环境
- ✅ 避免网络下载问题
- ✅ 获得最佳的依赖包兼容性
- ✅ 确保应用程序的稳定运行 