#!/bin/bash
# macOS 应用程序构建脚本（完整版本）
# 使用 PyInstaller 创建带图标的 .app 可执行程序，并创建 DMG 安装包

set -e  # 遇到错误立即退出

echo "🍎 macOS 应用程序构建脚本启动（完整版本）"
echo "📁 当前目录: $(pwd)"

# 检查系统
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本仅适用于 macOS"
    exit 1
fi

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"

# 检查必要文件
REQUIRED_FILES=(
    "main_monitor_gui_app.py"
    "config_with_yolo.yaml"
    "fuzzy_matcher.py"
    "config_manager.py"
    "network_monitor.py"
)

echo "🔍 检查必要文件..."
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件: $file"
        exit 1
    fi
    echo "  ✅ $file"
done

# 检查图标文件
echo "🎨 检查图标文件..."
ICON_FILE=""
ICON_CANDIDATES=(
    "assets/icons/icon.png"
    "assets/icons/icon_256x256.png"
    "assets/icon.png"
    "icons/icon.png"
    "icon.png"
)

for candidate in "${ICON_CANDIDATES[@]}"; do
    if [ -f "$candidate" ]; then
        ICON_FILE="$candidate"
        echo "  ✅ 找到图标文件: $ICON_FILE"
        break
    fi
done

if [ -z "$ICON_FILE" ]; then
    echo "  ⚠️  未找到图标文件，将使用默认图标"
    echo "  💡 建议运行: python3 create_png_icon.py"
fi

# 构建目录
BUILD_DIR="build_macos_app_simple"
RELEASE_DIR="release"

echo "🧹 清理构建目录..."
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
fi

echo "📁 创建构建目录: $BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 安装PyInstaller
echo "📦 检查PyInstaller..."
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "📦 安装 PyInstaller..."
    python3 -m pip install pyinstaller
fi

echo "🔨 构建macOS应用程序..."

# 创建PyInstaller命令
PYINSTALLER_CMD=(
    "python3" "-m" "PyInstaller"
    "--onedir"                     # 打包成目录（启动更快）
    "--windowed"                   # 无控制台窗口
    "--name=ChatMonitor"           # 应用程序名称
    "--noconfirm"                  # 自动确认覆盖
    "--add-data=config_with_yolo.yaml:."  # 添加配置文件
    "--add-data=fuzzy_matcher.py:."       # 添加模块
    "--add-data=config_manager.py:."      # 添加模块
    "--add-data=network_monitor.py:."     # 添加模块
    "--hidden-import=cv2"                 # 隐藏导入
    "--hidden-import=numpy"
    "--hidden-import=psutil"
    "--hidden-import=pyautogui"
    "--hidden-import=requests"
    "--hidden-import=urllib3"
    "--hidden-import=charset_normalizer"
    "--hidden-import=idna"
    "--hidden-import=certifi"
    "--hidden-import=yaml"
    "--hidden-import=PIL"
    "--hidden-import=pytesseract"
    "--hidden-import=playsound"
    "--hidden-import=watchdog"
    "--hidden-import=ultralytics"         # 预加载YOLO库
    "--hidden-import=cv2"
    "--hidden-import=numpy"
    "--hidden-import=tkinter"
    "--exclude-module=PyQt5"
    "--exclude-module=PyQt6"
    "--exclude-module=IPython"
    "--exclude-module=jupyter"
    "--exclude-module=scikit-learn"
    "--exclude-module=tensorflow"
    "--exclude-module=transformers"
    "--debug=all"
)

# 添加图标（如果找到）
if [ -n "$ICON_FILE" ]; then
    PYINSTALLER_CMD+=("--icon" "$ICON_FILE")
    echo "  🎨 使用图标: $ICON_FILE"
fi

# 添加主程序
PYINSTALLER_CMD+=("main_monitor_gui_app.py")

echo "🚀 执行: ${PYINSTALLER_CMD[*]}"
"${PYINSTALLER_CMD[@]}"

# 检查构建结果
if [ -f "dist/ChatMonitor/ChatMonitor" ]; then
    echo "✅ 可执行文件创建成功: dist/ChatMonitor/ChatMonitor"
    
    # 创建.app包
    echo "📦 创建.app包..."
    
    # 创建应用程序包结构
    APP_NAME="ChatMonitor.app"
    APP_DIR="dist/$APP_NAME"
    CONTENTS_DIR="$APP_DIR/Contents"
    MACOS_DIR="$CONTENTS_DIR/MacOS"
    RESOURCES_DIR="$CONTENTS_DIR/Resources"
    
    mkdir -p "$MACOS_DIR"
    mkdir -p "$RESOURCES_DIR"
    
    # 复制可执行文件
    cp "dist/ChatMonitor/ChatMonitor" "$MACOS_DIR/"
    chmod +x "$MACOS_DIR/ChatMonitor"
    
    # 复制资源文件（如果存在）
    if [ -d "sounds" ]; then
        cp -r sounds "$RESOURCES_DIR/"
        echo "  ✅ 复制 sounds/"
    fi
    
    if [ -d "test_img" ]; then
        cp -r test_img "$RESOURCES_DIR/"
        echo "  ✅ 复制 test_img/"
    fi
    
    if [ -d "models" ]; then
        cp -r models "$RESOURCES_DIR/"
        echo "  ✅ 复制 models/"
    fi
    
    # 复制 assets 目录（如果存在）
    if [ -d "assets" ]; then
        cp -r assets "$RESOURCES_DIR/"
        echo "  ✅ 复制 assets/"
    fi
    
    # 复制配置文件到外部可访问位置
    cp config_with_yolo.yaml "$RESOURCES_DIR/"
    echo "  ✅ 复制 config_with_yolo.yaml"
    
    # 复制图标文件到 Resources 目录
    if [ -n "$ICON_FILE" ]; then
        cp "$ICON_FILE" "$RESOURCES_DIR/icon.png"
        echo "  ✅ 复制图标到 Resources: $ICON_FILE"
    fi
    
    # 创建Info.plist
    cat > "$CONTENTS_DIR/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ChatMonitor</string>
    <key>CFBundleIdentifier</key>
    <string>com.chatmonitor.app</string>
    <key>CFBundleName</key>
    <string>ChatMonitor</string>
    <key>CFBundleDisplayName</key>
    <string>ChatMonitor</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
    <key>NSAppleEventsUsageDescription</key>
    <string>ChatMonitor需要控制其他应用程序来监控聊天弹窗。这是监控功能的核心需求。</string>
    <key>NSSystemAdministrationUsageDescription</key>
    <string>ChatMonitor需要系统管理权限来监控网络连接状态和系统进程。</string>
    <key>NSScreenCaptureUsageDescription</key>
    <string>ChatMonitor需要屏幕录制权限来检测聊天应用的弹窗。这是弹窗检测功能的核心需求。</string>
    <key>NSMicrophoneUsageDescription</key>
    <string>ChatMonitor需要麦克风权限来播放音频警报。</string>
    <key>NSAccessibilityUsageDescription</key>
    <string>ChatMonitor需要辅助功能权限来监控其他应用程序的窗口状态。</string>
    <key>LSUIElement</key>
    <false/>
    <key>LSBackgroundOnly</key>
    <false/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>LSMultipleInstancesProhibited</key>
    <true/>
    <key>CFBundleIconFile</key>
    <string>icon.png</string>
</dict>
</plist>
EOF
    
    echo "✅ 应用程序包创建成功: $APP_DIR"
    
    # 计算大小
    APP_SIZE=$(du -sh "$APP_DIR" | cut -f1)
    echo "📦 应用程序大小: $APP_SIZE"
    
    # 创建发布目录
    mkdir -p "$RELEASE_DIR"
    
    # 复制应用程序到发布目录
    cp -r "$APP_DIR" "$RELEASE_DIR/"
    
    # 移除隔离属性
    echo "🔓 移除应用隔离属性..."
    xattr -rd com.apple.quarantine "$RELEASE_DIR/$APP_NAME" 2>/dev/null || true
    
    # 创建DMG安装包
    echo "📦 创建DMG安装包..."
    DMG_NAME="ChatMonitor-macOS-v1.0.0.dmg"
    DMG_PATH="$RELEASE_DIR/$DMG_NAME"
    
    # 使用更安全的 DMG 创建方法
    echo "🔧 使用安全的 DMG 创建方法..."
    
    # 先创建一个临时目录
    TEMP_DMG_DIR="/tmp/ChatMonitor_dmg_temp"
    rm -rf "$TEMP_DMG_DIR"
    mkdir -p "$TEMP_DMG_DIR"
    
    # 复制应用程序到临时目录（使用 cp -R 保持所有属性）
    echo "📋 复制应用程序到临时目录..."
    cp -R "$RELEASE_DIR/$APP_NAME" "$TEMP_DMG_DIR/"
    
    # 确保所有文件都有正确的权限
    echo "🔧 修复文件权限..."
    find "$TEMP_DMG_DIR" -name "*.dylib" -exec chmod 755 {} \;
    find "$TEMP_DMG_DIR" -name "*.so" -exec chmod 755 {} \;
    find "$TEMP_DMG_DIR" -name "*.app" -exec chmod 755 {} \;
    
    # 移除应用隔离属性
    echo "🔓 移除应用隔离属性..."
    xattr -cr "$TEMP_DMG_DIR/$APP_NAME" 2>/dev/null || true
    
    # 创建 DMG
    echo "📦 创建 DMG..."
    hdiutil create -volname "ChatMonitor" -srcfolder "$TEMP_DMG_DIR" -ov -format UDZO "$DMG_PATH"
    
    # 清理临时目录
    rm -rf "$TEMP_DMG_DIR"
    
    if [ $? -eq 0 ]; then
        DMG_SIZE=$(du -sh "$DMG_PATH" | cut -f1)
        echo "✅ DMG创建成功: $DMG_PATH"
        echo "📦 DMG大小: $DMG_SIZE"
    else
        echo "❌ DMG创建失败"
        exit 1
    fi
    
    echo ""
    echo "🎉 构建完成！"
    echo "📁 应用程序: $RELEASE_DIR/$APP_NAME"
    echo "📦 安装包: $DMG_PATH"
    echo ""
    echo "🚀 使用方法:"
    echo "  1. 双击 $DMG_NAME 挂载DMG"
    echo "  2. 将 ChatMonitor.app 拖拽到应用程序文件夹"
    echo "  3. 从启动台或应用程序文件夹启动"
    echo ""
    echo "⚠️  注意: 首次运行可能需要在系统偏好设置中允许运行"
    echo "🔧 构建特性:"
    echo "  - 使用 PyInstaller 创建独立的 .app 包"
    echo "  - 自动处理图标和资源文件"
    echo "  - 使用安全的 DMG 创建方法"
    echo "  - 修复文件权限和符号链接问题"
    echo "  - 移除应用隔离属性"
    
else
    echo "❌ 构建失败，未找到可执行文件"
    exit 1
fi 