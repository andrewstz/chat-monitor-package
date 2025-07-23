# Windows 构建脚本说明

这个目录包含了所有Windows平台的构建脚本和工具。

## 📁 文件说明

### 🔧 环境设置脚本

#### `setup_windows.bat`
- **用途**: 基础Windows环境设置
- **功能**: 安装Python依赖，检查Tesseract OCR
- **状态**: 基础版本，使用pip安装依赖

#### `setup_windows_uv.bat`
- **用途**: 使用UV包管理器的Windows环境设置
- **功能**: 使用UV安装依赖，更快的依赖解析
- **状态**: 改进版本，使用UV替代pip

#### `setup_windows_uv_simple.bat`
- **用途**: 简化版UV环境设置
- **功能**: 基础依赖安装，UV环境管理
- **状态**: 推荐使用，最稳定的设置脚本

### 🏗️ 构建脚本

#### `build_windows_app.bat`
- **用途**: 基础Windows应用构建
- **功能**: 使用PyInstaller构建.exe文件
- **状态**: 基础版本，可能遇到playsound问题

#### `build_windows_uv_simple_fixed.bat`
- **用途**: 修复版UV构建脚本
- **功能**: 处理playsound编译问题
- **状态**: 改进版本，尝试解决音频依赖问题

#### `build_windows_no_playsound.bat`
- **用途**: 完全绕过playsound的构建脚本
- **功能**: 使用替代音频方案
- **状态**: 稳定版本，不依赖playsound

#### `build_windows_uv_simple_final.bat`
- **用途**: 最终版UV构建脚本
- **功能**: 使用spec文件构建
- **状态**: 完整版本，包含所有功能

#### `build_windows_uv_simple_final_fixed.bat`
- **用途**: 修复版最终构建脚本
- **功能**: 直接使用PyInstaller命令，避免TOML错误
- **状态**: 最新推荐版本，最稳定

### 🔧 问题修复脚本

#### `fix_playsound_issue.bat`
- **用途**: 修复playsound安装问题
- **功能**: 尝试多种方法安装playsound
- **状态**: 音频依赖修复工具

## 🚀 使用流程

### 1. 环境设置
```bash
# 推荐使用简化版设置
setup_windows_uv_simple.bat
```

### 2. 构建应用
```bash
# 推荐使用修复版构建脚本
build_windows_uv_simple_final_fixed.bat
```

### 3. 如果遇到音频问题
```bash
# 运行修复脚本
fix_playsound_issue.bat
```

## 📋 构建结果

成功构建后会生成：
- `dist\ChatMonitor.exe` - 单文件可执行程序
- `dist\ChatMonitor\` - 便携式应用目录
- `ChatMonitor_Windows_Portable.zip` - 便携式ZIP包

## ⚠️ 注意事项

1. **音频功能**: 如果playsound安装失败，应用会使用PowerShell播放音频
2. **OCR功能**: 需要安装Tesseract OCR，但非必需
3. **依赖管理**: 推荐使用UV环境，更快的依赖解析
4. **构建环境**: 需要Python 3.8+和Windows 10/11

## 🔧 故障排除

### playsound编译错误
- 使用`fix_playsound_issue.bat`修复
- 或使用`build_windows_uv_simple_final_fixed.bat`构建

### TOML解析错误
- 使用`build_windows_uv_simple_final_fixed.bat`
- 避免使用临时pyproject文件

### 依赖安装失败
- 检查网络连接
- 尝试使用`setup_windows_uv_simple.bat`重新设置环境

## 📝 版本历史

- **v1.0**: 基础构建脚本
- **v2.0**: 添加UV支持
- **v3.0**: 修复playsound问题
- **v4.0**: 最终稳定版本 