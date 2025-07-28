# macOS Python包离线安装指南

## 适用场景
- 在macOS上为Windows内网环境准备离线包
- 网络连接不稳定导致安装失败
- 需要批量部署相同环境

## 完整流程

### 第一步：在macOS上下载包

1. **给脚本添加执行权限**：
   ```bash
   chmod +x download_packages_mac.sh
   ```

2. **运行下载脚本**：
   ```bash
   ./download_packages_mac.sh
   ```

3. **下载完成后**：
   - 会创建 `packages` 目录
   - 包含所有必需的 `.whl` 文件
   - 文件大小约 200-500MB

4. **传输到Windows内网**：
   - 将整个 `packages` 文件夹复制到Windows机器
   - 可以使用U盘、网络共享等方式

### 第二步：在Windows内网机器上安装

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

### 在macOS上执行：
```bash
# 创建下载目录
mkdir packages
cd packages

# 下载核心包
pip3 download opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download pygame -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download requests -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download psutil -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 下载依赖包
pip3 download numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download wheel -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 下载macOS特定依赖
pip3 download pyobjc-core -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip3 download pyobjc-framework-Cocoa -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## macOS特定说明

### 权限设置
```bash
# 给所有脚本添加执行权限
chmod +x *.sh
```

### Python版本
```bash
# 检查Python版本
python3 --version

# 如果使用Homebrew安装的Python
brew install python@3.10
```

### 依赖管理
```bash
# 使用pip3而不是pip
pip3 install package_name

# 或者使用虚拟环境
python3 -m venv venv
source venv/bin/activate
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
- `pyobjc-core-*.whl`
- `pyobjc-framework-Cocoa-*.whl`

## 常见问题

### 问题1：权限问题
**解决方案**：
```bash
chmod +x download_packages_mac.sh
chmod +x install_offline_packages_mac.sh
chmod +x build_quick_mac.sh
```

### 问题2：Python路径问题
**解决方案**：
```bash
# 检查Python路径
which python3

# 使用完整路径
/usr/bin/python3 download_packages_mac.sh
```

### 问题3：依赖冲突
**解决方案**：
```bash
# 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
./download_packages_mac.sh
```

## 优势

✅ **跨平台兼容**：macOS下载，Windows安装
✅ **完全离线**：无需网络连接
✅ **可重复使用**：一次下载，多次安装
✅ **版本固定**：避免版本兼容性问题

## 总结

macOS离线安装方案：
1. 在macOS上下载所有包
2. 传输到Windows内网
3. 在Windows上离线安装
4. 开始打包

这样就能充分利用macOS的网络环境，为Windows内网准备离线包！ 