# buildWin 目录文件索引

## 📁 文件列表

### 🔧 环境设置脚本 (3个)
- `setup_windows.bat` - 基础Windows环境设置
- `setup_windows_uv.bat` - UV包管理器环境设置
- `setup_windows_uv_simple.bat` - 简化版UV环境设置 ⭐ **推荐**

### 🏗️ 构建脚本 (6个)
- `build_windows_app.bat` - 基础Windows应用构建
- `build_windows_uv_simple_fixed.bat` - 修复版UV构建脚本
- `build_windows_no_playsound.bat` - 绕过playsound的构建脚本
- `build_windows_uv_simple_final.bat` - 最终版UV构建脚本
- `build_windows_uv_simple_final_fixed.bat` - 修复版最终构建脚本 ⭐ **推荐**
- `build_windows_uv_complete.bat` - 完整版UV构建脚本

### 🔧 问题修复脚本 (1个)
- `fix_playsound_issue.bat` - 修复playsound安装问题

### 📚 说明文档 (4个)
- `README.md` - 主要说明文档 ⭐ **必读**
- `README_Windows.md` - Windows详细说明
- `README-14windows上打绿色包.md` - Windows绿色包制作指南
- `WINDOWS_SIMPLE_GUIDE.md` - Windows简单指南

### 📋 配置文件 (1个)
- `requirements_windows.txt` - Windows依赖列表

## 🚀 快速使用

### 1. 查看说明
```bash
cat README.md
```

### 2. 环境设置
```bash
setup_windows_uv_simple.bat
```

### 3. 构建应用
```bash
build_windows_uv_simple_final_fixed.bat
```

## 📊 文件统计

- **总文件数**: 15个
- **脚本文件**: 10个 (.bat)
- **文档文件**: 4个 (.md)
- **配置文件**: 1个 (.txt)

## 🎯 推荐使用流程

1. **首次使用**: 阅读 `README.md`
2. **环境设置**: 运行 `setup_windows_uv_simple.bat`
3. **构建应用**: 运行 `build_windows_uv_simple_final_fixed.bat`
4. **问题修复**: 如有音频问题，运行 `fix_playsound_issue.bat`

## 📝 版本说明

- **v1.0**: 基础构建脚本
- **v2.0**: 添加UV支持
- **v3.0**: 修复playsound问题
- **v4.0**: 最终稳定版本

---

**创建时间**: 2025-07-23 14:28
**文件总数**: 15个
**推荐脚本**: `build_windows_uv_simple_final_fixed.bat` 