# Python包离线安装指南

## 适用场景
- 内网环境无法访问外网
- 网络连接不稳定导致安装失败
- 需要批量部署相同环境

## 完整流程

### 第一步：在外网机器上下载包

1. **在外网机器上运行**：
   ```cmd
   .\download_packages.bat
   ```

2. **下载完成后**：
   - 会创建 `packages` 目录
   - 包含所有必需的 `.whl` 文件
   - 文件大小约 200-500MB

3. **传输到内网**：
   - 将整个 `packages` 文件夹复制到内网机器
   - 可以使用U盘、网络共享等方式

### 第二步：在内网机器上安装

1. **确保Python已安装**：
   ```cmd
   python --version
   ```

2. **运行离线安装脚本**：
   ```cmd
   .\install_offline_packages.bat
   ```

3. **验证安装**：
   ```cmd
   .\check_system_dependencies.bat
   ```

### 第三步：开始打包

安装完成后，可以开始打包：
```cmd
.\build_quick.bat
```

## 手动下载方法

如果自动下载脚本有问题，可以手动下载：

### 在外网机器上执行：
```cmd
# 创建下载目录
mkdir packages
cd packages

# 下载核心包
pip download opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download pygame -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download requests -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download psutil -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 下载依赖包
pip download numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip download wheel -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 在内网机器上安装：
```cmd
# 进入packages目录
cd packages

# 按顺序安装
pip install setuptools*.whl
pip install wheel*.whl
pip install numpy*.whl
pip install *.whl
```

## 文件清单

下载完成后，`packages` 目录应包含：

### 核心包
- `opencv_python-*.whl`
- `ultralytics-*.whl`
- `pygame-*.whl`
- `pyinstaller-*.whl`
- `Pillow-*.whl`
- `requests-*.whl`
- `PyYAML-*.whl`
- `psutil-*.whl`

### 依赖包
- `numpy-*.whl`
- `setuptools-*.whl`
- `wheel-*.whl`
- 以及其他自动下载的依赖包

## 常见问题

### 问题1：下载失败
**解决方案**：
- 使用不同的镜像源
- 检查网络连接
- 分批次下载

### 问题2：安装失败
**解决方案**：
- 确保Python版本匹配
- 按依赖顺序安装
- 检查文件完整性

### 问题3：DLL错误
**解决方案**：
- 确保安装了Visual C++ Redistributable
- 检查Python环境完整性
- 重新安装Python

## 优势

✅ **完全离线**：无需网络连接
✅ **可重复使用**：一次下载，多次安装
✅ **版本固定**：避免版本兼容性问题
✅ **批量部署**：适合多台机器部署

## 总结

离线安装是解决内网环境依赖问题的最佳方案：
1. 在外网下载所有包
2. 传输到内网
3. 离线安装
4. 开始打包 