#!/bin/bash

echo "🍎 macOS 应用程序精确优化构建脚本启动"
echo "📁 当前目录: $(pwd)"

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $python_version"

# 检查必要文件
echo "🔍 检查必要文件..."
required_files=(
    "main_monitor_gui_app.py"
    "config_with_yolo.yaml"
    "fuzzy_matcher.py"
    "config_manager.py"
    "network_monitor.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file 不存在"
        exit 1
    fi
done

# 清理构建目录
echo "🧹 清理构建目录..."
rm -rf build_macos_app_optimized_v2
rm -rf dist/ChatMonitor_optimized_v2
rm -rf dist/ChatMonitor_optimized_v2.app

# 创建构建目录
echo "📁 创建构建目录: build_macos_app_optimized_v2"
mkdir -p build_macos_app_optimized_v2

# 检查 PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller 未安装，请先安装: pip install pyinstaller"
    exit 1
fi
echo "📦 检查PyInstaller..."

# 构建 macOS 应用程序（精确优化版本）
echo "🔨 构建macOS应用程序（精确优化版本）..."

# 精确优化的 PyInstaller 命令，只排除真正不需要的依赖
pyinstaller_cmd="python3 -m PyInstaller \
    --onedir \
    --windowed \
    --name=ChatMonitor_optimized_v2 \
    --noconfirm \
    --add-data=config_with_yolo.yaml:. \
    --add-data=fuzzy_matcher.py:. \
    --add-data=config_manager.py:. \
    --add-data=network_monitor.py:. \
    --hidden-import=cv2 \
    --hidden-import=numpy \
    --hidden-import=psutil \
    --hidden-import=pyautogui \
    --hidden-import=requests \
    --hidden-import=urllib3 \
    --hidden-import=charset_normalizer \
    --hidden-import=idna \
    --hidden-import=certifi \
    --hidden-import=yaml \
    --hidden-import=PIL \
    --hidden-import=pytesseract \
    --hidden-import=ultralytics \
    --hidden-import=torch \
    --hidden-import=torchvision \
    --hidden-import=tkinter \
    --exclude-module=paddle \
    --exclude-module=scipy \
    --exclude-module=matplotlib \
    --exclude-module=pandas \
    --exclude-module=llvmlite \
    --exclude-module=numba \
    --exclude-module=sympy \
    --exclude-module=networkx \
    --exclude-module=sqlalchemy \
    --exclude-module=lxml \
    --exclude-module=shapely \
    --exclude-module=openpyxl \
    --exclude-module=PyQt5 \
    --exclude-module=PyQt6 \
    --exclude-module=IPython \
    --exclude-module=jupyter \
    --exclude-module=scikit-learn \
    --exclude-module=tensorflow \
    --exclude-module=transformers \
    --exclude-module=torchaudio \
    --exclude-module=torchtext \
    --exclude-module=torchdata \
    --exclude-module=torchserve \
    --exclude-module=torchx \
    --exclude-module=torchrec \
    --exclude-module=torchrl \
    --exclude-module=torchmetrics \
    --debug=all \
    main_monitor_gui_app.py"

echo "🚀 执行: $pyinstaller_cmd"
eval $pyinstaller_cmd

if [ $? -eq 0 ]; then
    echo "✅ 可执行文件创建成功: dist/ChatMonitor_optimized_v2/ChatMonitor_optimized_v2"
else
    echo "❌ 构建失败"
    exit 1
fi

# 创建.app包
echo "📦 创建.app包..."
app_dir="dist/ChatMonitor_optimized_v2.app"
mkdir -p "$app_dir/Contents/MacOS"
mkdir -p "$app_dir/Contents/Resources"

# 复制可执行文件
cp "dist/ChatMonitor_optimized_v2/ChatMonitor_optimized_v2" "$app_dir/Contents/MacOS/ChatMonitor_optimized_v2"

# 复制必要的资源文件
echo "  ✅ 复制 sounds/"
cp -r "sounds" "$app_dir/Contents/Resources/"

echo "  ✅ 复制 test_img/"
cp -r "test_img" "$app_dir/Contents/Resources/"

echo "  ✅ 复制 models/"
cp -r "models" "$app_dir/Contents/Resources/"

echo "  ✅ 复制 config_with_yolo.yaml"
cp "config_with_yolo.yaml" "$app_dir/Contents/Resources/"

# 创建 Info.plist
cat > "$app_dir/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ChatMonitor_optimized_v2</string>
    <key>CFBundleIdentifier</key>
    <string>com.chatmonitor.app</string>
    <key>CFBundleName</key>
    <string>ChatMonitor</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
EOF

# 检查应用程序大小
app_size=$(du -sh "$app_dir" | cut -f1)
echo "✅ 应用程序包创建成功: $app_dir"
echo "📦 应用程序大小: $app_size"

# 移除应用隔离属性
echo "🔓 移除应用隔离属性..."
xattr -cr "$app_dir" 2>/dev/null || true

# 创建 DMG 安装包
echo "📦 创建DMG安装包..."
dmg_name="ChatMonitor-macOS-optimized-v2-v1.0.0.dmg"
dmg_path="release/$dmg_name"

# 确保 release 目录存在
mkdir -p release

# 创建 DMG
hdiutil create -volname "ChatMonitor" -srcfolder "$app_dir" -ov -format UDZO "$dmg_path"

if [ $? -eq 0 ]; then
    dmg_size=$(du -sh "$dmg_path" | cut -f1)
    echo "✅ DMG创建成功: $dmg_path"
    echo "📦 DMG大小: $dmg_size"
else
    echo "❌ DMG创建失败"
    exit 1
fi

echo ""
echo "🎉 精确优化构建完成！"
echo "📁 应用程序: $app_dir"
echo "📦 安装包: $dmg_path"
echo ""
echo "🚀 使用方法:"
echo "  1. 双击 $dmg_name 挂载DMG"
echo "  2. 将 ChatMonitor_optimized_v2.app 拖拽到应用程序文件夹"
echo "  3. 从启动台或应用程序文件夹启动"
echo ""
echo "⚠️  注意: 首次运行可能需要在系统偏好设置中允许运行"
echo ""
echo "📊 优化策略:"
echo "  - 保留: torch, ultralytics (YOLO必需)"
echo "  - 排除: paddle, scipy, matplotlib, pandas 等"
echo "  - 预期大小: 约 300-500MB" 