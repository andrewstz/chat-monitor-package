# 项目资源目录结构

## 📁 Assets 目录结构

```
doPackage/
├── assets/
│   ├── icons/           # 图标资源目录
│   │   ├── icon.png     # 默认应用图标
│   │   ├── icon.icns    # macOS 图标格式
│   │   ├── icon_16x16.png
│   │   ├── icon_32x32.png
│   │   ├── icon_64x64.png
│   │   ├── icon_128x128.png
│   │   └── icon_256x256.png
│   └── sounds/          # 音频资源目录
│       ├── contact_alert_pitch_speed_volume.wav
│       ├── default.wav
│       ├── error_alert_pitch_speed_volume.wav
│       └── normal_tip_pitch_speed_volume.wav
```

## 🎨 图标资源

### 图标文件说明
- **icon.png**: 默认应用图标（256x256）
- **icon.icns**: macOS 图标格式，用于打包
- **icon_*.png**: 不同尺寸的 PNG 图标

### 图标设置优先级
1. `assets/icons/icon.png` - 主要图标
2. `assets/icons/icon_256x256.png` - 高分辨率图标
3. `assets/icons/icon.icns` - macOS 图标格式
4. 其他兼容路径（向后兼容）

## 🔊 音频资源

### 音频文件说明
- **contact_alert_pitch_speed_volume.wav**: 联系人提醒音
- **default.wav**: 默认提示音
- **error_alert_pitch_speed_volume.wav**: 错误提醒音
- **normal_tip_pitch_speed_volume.wav**: 普通提示音

## 🛠️ 管理脚本

### 图标管理
- `create_png_icon.py`: 创建 PNG 格式图标
- `refresh_icon.py`: 刷新图标缓存

### 使用方法
```bash
# 创建新图标
python3 create_png_icon.py

# 刷新图标缓存
python3 refresh_icon.py
```

## 📋 注意事项

1. **图标路径**: 程序会自动查找 `assets/icons/` 目录
2. **兼容性**: 保留了对旧路径的支持
3. **缓存问题**: 修改图标后可能需要运行 `refresh_icon.py`
4. **打包支持**: 图标会自动包含在打包的应用中 