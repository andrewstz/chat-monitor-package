# Git Actions 构建工具

本目录包含所有与GitHub Actions构建相关的工具脚本和配置文件。

## 📁 目录结构

```
gitActions/
├── audio_windows_fixed.py     # Windows音频播放修复模块
├── config_windows.yaml        # Windows专用配置文件（本地版本）
├── debug_yolo_windows.py      # Windows YOLO调试脚本
├── README_GitHub_Actions.md   # GitHub Actions详细指南
├── HOW_TO_USE.md             # 使用说明
└── README.md                  # 本说明文档
```

## 🔧 工具脚本说明

### 1. audio_windows_fixed.py - Windows音频播放修复
- **功能**: 解决Windows下音频播放问题
- **支持**: PowerShell音频播放、系统提示音
- **用途**: 修复Windows打包版本中的音频播放问题

### 2. config_windows.yaml - Windows专用配置（本地版本）
- **功能**: Windows环境优化的配置文件（本地开发用）
- **特点**: 
  - 降低YOLO置信度阈值
  - 优化检测间隔
  - 启用PowerShell音频播放
  - 优先使用CPU模式

### 3. debug_yolo_windows.py - Windows YOLO调试
- **功能**: 诊断Windows下YOLO模型问题
- **测试项目**:
  - PyTorch和Ultralytics库导入
  - YOLO模型加载和推理
  - OCR相关库检查
  - 音频播放功能测试

## 🚀 使用方法

### Windows问题诊断
```bash
# 在Windows虚拟机上运行
python gitActions/debug_yolo_windows.py
```

### 音频播放测试
```bash
# 测试Windows音频播放
python gitActions/audio_windows_fixed.py
```

### 使用本地Windows配置
```bash
# 复制本地Windows专用配置
cp gitActions/config_windows.yaml config_with_yolo.yaml
```

## 🔍 故障排除

### YOLO模型问题
1. 运行 `debug_yolo_windows.py` 诊断
2. 检查PyTorch和Ultralytics版本
3. 验证模型文件完整性

### 音频播放问题
1. 运行 `audio_windows_fixed.py` 测试
2. 检查PowerShell权限
3. 验证音频驱动

### 配置问题
1. 使用 `config_windows.yaml` 替代默认配置
2. 调整检测参数
3. 启用备用方案

## 📦 构建相关

### GitHub Actions自动配置生成
现在GitHub Actions会在构建过程中自动生成平台专用配置：

#### Windows构建包包含：
- `config_windows.yaml` - Windows优化配置（自动生成）
- `start_monitor_windows.bat` - Windows专用启动脚本
- `config_with_yolo.yaml` - 原始配置文件（备用）

#### Linux构建包包含：
- `config_linux.yaml` - Linux优化配置（自动生成）
- `start_monitor_linux.sh` - Linux专用启动脚本
- `config_with_yolo.yaml` - 原始配置文件（备用）

#### macOS构建包包含：
- `config_macos.yaml` - macOS优化配置（自动生成）
- `start_monitor_macos.sh` - macOS专用启动脚本
- `config_with_yolo.yaml` - 原始配置文件（备用）

### 构建产物
- Windows: `chat_monitor_windows.exe`
- Linux: `chat_monitor_linux`
- macOS: `chat_monitor_macos`

## 🔗 相关文档

- [GitHub Actions 详细指南](README_GitHub_Actions.md)
- [使用说明](HOW_TO_USE.md)
- [快速开始指南](../QUICK_START.md)

## 📝 更新日志

### v1.2.0 (2024-07-26)
- GitHub Actions自动生成平台专用配置
- 添加平台专用启动脚本
- 优化各平台配置参数

### v1.1.0 (2024-07-26)
- 添加Windows音频播放修复模块
- 创建Windows专用配置文件
- 添加Windows YOLO调试脚本
- 优化目录结构

### v1.0.0 (2024-07-26)
- 创建GitHub Actions构建配置
- 支持多平台构建
- 集成YOLO和OCR功能

## 🎯 平台配置差异

### Windows配置特点
- YOLO置信度：0.6（降低以提高检测率）
- 检测间隔：2秒（稍慢）
- 音频：PowerShell播放
- 内存限制：2GB
- CPU优先模式

### Linux配置特点
- YOLO置信度：0.7（平衡）
- 检测间隔：1秒（标准）
- 音频：paplay/aplay
- 内存限制：4GB
- GPU可用

### macOS配置特点
- YOLO置信度：0.75（较高精度）
- 检测间隔：1秒（标准）
- 音频：afplay
- 内存限制：3GB
- GPU可用





