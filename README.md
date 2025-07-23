# 动态监控系统（精简版）

基于 `main_monitor_dynamic.py` 的聊天监控AI系统，支持配置文件热更新。

## 🎯 精简版特性

- ✅ **轻量级** - 不包含大型AI模型，体积小
- ✅ **快速启动** - 依赖少，安装快
- ✅ **核心功能完整** - 包含所有必要功能
- ✅ **动态配置热更新** - 修改配置文件实时生效
- ✅ **Tesseract OCR** - 文字识别
- ✅ **模糊匹配联系人** - 支持相似度匹配
- ✅ **网络监控** - 智能断网检测
- ✅ **跨平台音频提示** - 多种提示音类型

## 🚀 快速开始

### macOS/Linux
```bash
chmod +x start_monitor.sh
./start_monitor.sh
```

### Windows
```cmd
start_monitor.bat
```

## 📦 可选功能安装

### YOLO模型（弹出框检测）
```bash
# 安装YOLO支持
pip install ultralytics

# 下载YOLO模型
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

### 语义分析模型
```bash
# 安装语义分析支持
pip install torch transformers

# 下载中文BERT模型（约400MB）
python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('hfl/chinese-bert-wwm-ext'); AutoModel.from_pretrained('hfl/chinese-bert-wwm-ext')"
```

## 🔧 配置文件

主要配置文件：`config_with_yolo.yaml`

### 关键配置项

```yaml
chat_app:
  name: "Mango"  # 聊天应用名称
  target_contacts: ["测试", "js_wbmalia-研发部助理"]  # 目标联系人

monitor:
  check_interval: 3    # 检测间隔（秒）
  reply_wait: 60       # 回复等待时间（秒）

network_monitor:
  enabled: true
  check_interval: 60   # 网络检测间隔
  consecutive_failures: 3  # 连续失败阈值
  tolerance_minutes: 15    # 容错时间
```

## 🛠️ 系统要求

- **Python 3.8+** - 核心运行环境
- **Tesseract OCR** - 文字识别引擎
- **屏幕录制权限** - 截图功能
- **网络连接** - 网络监控功能

## 📦 安装指南

### Windows 应用构建

完整的Windows构建工具和脚本位于 `buildWin/` 目录：

```bash
# 进入Windows构建目录
cd buildWin

# 查看详细说明
cat README.md

# 环境设置
setup_windows_uv_simple.bat

# 构建应用
build_windows_uv_simple_final_fixed.bat
```

构建结果：
- `dist\ChatMonitor.exe` - 单文件可执行程序
- `ChatMonitor_Windows_Portable.zip` - 便携式ZIP包

### macOS
```bash
# 安装 Tesseract
brew install tesseract tesseract-lang

# 启动程序
./start_monitor.sh
```

### Ubuntu/Debian
```bash
# 安装 Tesseract
sudo apt install tesseract-ocr tesseract-ocr-chi-sim

# 启动程序
./start_monitor.sh
```

### Windows
```cmd
# 下载安装 Tesseract
# https://github.com/UB-Mannheim/tesseract/wiki

# 启动程序
start_monitor.bat

# 构建Windows应用
cd buildWin
setup_windows_uv_simple.bat
build_windows_uv_simple_final_fixed.bat
```

## 🔍 故障排除

### 1. Tesseract未找到
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
```

### 2. 权限问题
```bash
# macOS - 授予屏幕录制权限
系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制
```

### 3. 依赖安装失败
```bash
# 使用国内镜像
pip install -r requirements_clean.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 📊 文件大小对比

| 版本 | 大小 | 说明 |
|------|------|------|
| 精简版 | ~50MB | 核心功能，无大型模型 |
| 完整版 | ~3GB | 包含所有AI模型 |

## 🔄 升级到完整版

如果需要完整功能，可以：

1. 安装额外依赖
2. 下载AI模型
3. 修改配置文件启用高级功能

## 📞 技术支持

- 查看配置文件语法
- 检查程序运行日志
- 提交 GitHub Issue

---

**构建时间**: 2025-07-18 15:41:32
**版本**: 精简版 v1.0.0
**主程序**: main_monitor_dynamic.py
