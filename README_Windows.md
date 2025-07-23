# ChatMonitor - Windows 绿色版

## 🪟 Windows 11 虚拟机打包指南

### 📋 系统要求

- Windows 11 (虚拟机环境)
- Python 3.8+
- 足够的磁盘空间 (建议 2GB+)

### 🚀 快速开始

#### 1. 环境准备

```bash
# 安装Python依赖
pip install -r requirements_windows.txt

# 图标文件已包含在目录中（macOS创建）
```

#### 2. 构建应用程序

```bash
# 运行Windows构建脚本
build_windows_app.bat
```

#### 3. 使用绿色版

构建完成后，在 `release` 目录下会生成：

- `ChatMonitor-Windows-v1.0.0.zip` - 绿色版压缩包
- `ChatMonitor/` - 解压后的应用程序目录

### 📦 绿色版特性

#### ✅ 免安装
- 解压即可使用，无需安装
- 不修改系统注册表
- 不写入系统目录

#### ✅ 便携性
- 可复制到U盘使用
- 支持任意目录运行
- 包含所有依赖文件

#### ✅ 完整性
- 包含所有资源文件 (sounds, models, assets)
- 包含配置文件 (config_with_yolo.yaml)
- 包含启动脚本和说明文件

### 🎯 使用方法

#### 方法1: 使用启动脚本
```bash
# 双击运行
start_chatmonitor.bat
```

#### 方法2: 直接运行
```bash
# 双击运行
ChatMonitor.exe
```

### 🔧 功能特性

#### 🎯 核心功能
- **YOLO弹出框检测**: 使用深度学习模型检测聊天弹窗
- **Tesseract OCR**: 文字识别和内容提取
- **网络监控**: 实时监控网络连接状态
- **进程监控**: 监控目标应用程序运行状态

#### 🎨 界面功能
- **自适应布局**: 窗口大小自动调整
- **发信人设置**: 可配置监控的目标联系人
- **网络监控频率**: 可调整网络检测参数
- **实时日志**: 显示检测结果和系统状态

#### 🔊 声音提醒
- **联系提醒音**: 检测到目标联系人时播放
- **网络警报音**: 网络异常时播放
- **进程退出音**: 目标应用退出时播放

### 🎨 图标共用

Windows版本完全支持使用PNG图标，并且可以与macOS版本共用图标文件：

#### ✅ PNG图标支持
- **直接使用macOS图标**: Windows版本直接使用macOS创建的PNG图标
- **跨平台兼容**: PNG图标可以在macOS和Windows之间共用
- **自动查找**: 支持多种路径的图标文件

#### 📁 图标文件位置
```
assets/icons/icon.png          # 主要PNG图标（与macOS共用）
assets/icons/icon_256x256.png  # 256x256 PNG图标（与macOS共用）
assets/icons/icon_128x128.png  # 128x128 PNG图标（与macOS共用）
assets/icons/icon_64x64.png    # 64x64 PNG图标（与macOS共用）
assets/icons/icon_32x32.png    # 32x32 PNG图标（与macOS共用）
assets/icons/icon_16x16.png    # 16x16 PNG图标（与macOS共用）
```

#### 🔄 图标创建流程
```bash
# 在macOS上创建图标
python create_png_icon.py

# 将整个目录复制到Windows环境
# 然后直接运行构建脚本
```

### 📁 文件结构

```
ChatMonitor/
├── ChatMonitor.exe          # 主程序
├── start_chatmonitor.bat    # 启动脚本
├── README.txt              # 使用说明
├── config_with_yolo.yaml   # 配置文件
├── icon.png               # 程序图标（PNG格式）
├── sounds/                # 声音文件
│   ├── contact_alert_pitch_speed_volume.wav
│   ├── error_alert_pitch_speed_volume.wav
│   └── normal_tip_pitch_speed_volume.wav
├── models/                # YOLO模型文件
│   └── best.pt
├── assets/                # 资源文件
│   └── icons/
└── [其他依赖文件]
```

### ⚙️ 配置说明

#### 发信人设置
1. 启动程序后点击"发信人设置"
2. 输入要监控的联系人姓名，用逗号分隔
3. 点击"保存设置"生效

#### 网络监控频率
1. 点击"网络监控频率"按钮
2. 调整以下参数：
   - **检测间隔**: 网络检测频率 (10-60秒)
   - **超时时间**: 单次检测超时 (5-10秒)
   - **连续失败阈值**: 触发警报的失败次数 (2-5次)
   - **容错时间**: 等待时间 (0.1-1分钟)

### 🔍 故障排除

#### 常见问题

**Q: 程序无法启动**
- 检查是否被杀毒软件拦截
- 确保Windows防火墙允许访问
- 尝试以管理员身份运行

**Q: 检测不到弹窗**
- 检查目标应用是否正在运行
- 确认屏幕录制权限已开启
- 检查配置文件中的目标应用名称

**Q: 声音不播放**
- 检查系统音量设置
- 确认声音文件是否存在
- 检查音频驱动是否正常

**Q: 网络监控不工作**
- 检查网络连接状态
- 确认防火墙设置
- 调整网络监控参数

### 🛠️ 开发说明

#### 构建脚本特性
- **自动依赖检查**: 检查Python环境和必要文件
- **图标处理**: 自动查找macOS创建的PNG图标
- **资源打包**: 自动复制所有资源文件
- **绿色版生成**: 创建免安装的压缩包

#### 跨平台优化
- **图标共享**: 直接使用macOS创建的PNG图标
- **路径处理**: 适配Windows路径分隔符
- **编码支持**: 支持中文文件名和路径
- **权限处理**: 处理Windows权限问题

### 📝 更新日志

#### v1.0.0
- ✅ 初始版本发布
- ✅ 支持Windows 11虚拟机环境
- ✅ 绿色版免安装
- ✅ 完整的GUI界面
- ✅ 网络和进程监控功能

### 📞 技术支持

如遇到问题，请检查：
1. 系统日志文件
2. 程序运行日志
3. 配置文件设置
4. 网络连接状态

---

**注意**: 此版本专为Windows 11虚拟机环境优化，确保最佳的兼容性和性能。 