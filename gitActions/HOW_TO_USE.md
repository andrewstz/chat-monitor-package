# 如何使用Git Actions构建工具

## 📁 当前状态

`gitActions/` 目录现在包含构建相关的工具脚本和配置文件：

```
gitActions/
├── audio_windows_fixed.py     # Windows音频播放修复模块
├── config_windows.yaml        # Windows专用配置文件
├── debug_yolo_windows.py      # Windows YOLO调试脚本
├── README_GitHub_Actions.md   # GitHub Actions详细指南
├── HOW_TO_USE.md             # 本文件
└── README.md                  # 构建工具说明
```

## 🔧 工具脚本使用

### 1. Windows YOLO调试
```bash
# 在Windows虚拟机上运行诊断
python gitActions/debug_yolo_windows.py
```

### 2. Windows音频播放测试
```bash
# 测试Windows音频播放功能
python gitActions/audio_windows_fixed.py
```

### 3. 使用Windows专用配置
```bash
# 复制Windows优化配置
cp gitActions/config_windows.yaml config_with_yolo.yaml
```

## 🚀 GitHub Actions状态

GitHub Actions配置文件保持在根目录：
```
.github/
└── workflows/
    ├── build.yml          # 完整构建配置
    └── quick-build.yml    # 快速构建配置
```

这样可以确保GitHub Actions正常工作。

## 📦 构建流程

### 自动触发
- 推送代码到 `main` 分支
- 创建 Pull Request
- 发布 Release

### 手动触发
1. 在GitHub仓库页面
2. 点击 "Actions" 标签
3. 选择工作流
4. 点击 "Run workflow"

## 🔍 故障排除

### Windows构建问题
1. 运行 `debug_yolo_windows.py` 诊断YOLO问题
2. 运行 `audio_windows_fixed.py` 测试音频
3. 使用 `config_windows.yaml` 优化配置

### 构建失败
1. 检查 `.github/workflows/` 目录
2. 验证YAML语法
3. 查看构建日志

### 依赖问题
1. 检查 `requirements_clean.txt`
2. 验证Python版本
3. 确认所有依赖库

## 📝 更新配置

### 修改构建配置
1. 编辑 `.github/workflows/build.yml`
2. 提交并推送更改
3. 触发新的构建

### 修改工具脚本
1. 编辑 `gitActions/` 目录中的脚本
2. 测试功能
3. 提交更改

## 🔗 相关文档

- [构建工具说明](README.md)
- [GitHub Actions 详细指南](README_GitHub_Actions.md)
- [快速开始指南](../QUICK_START.md)

## ⚠️ 注意事项

1. **GitHub Actions**: `.github/` 目录必须在根目录
2. **工具脚本**: 可以安全地放在 `gitActions/` 目录
3. **配置文件**: 根据需要选择使用默认或Windows专用配置 