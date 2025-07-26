# GitHub Actions 自动打包指南

## 概述

这个配置允许你将 `doPackage` 目录单独作为一个独立的 GitHub 仓库，使用 GitHub Actions 进行自动打包。

## 仓库结构

```
chat-monitor-package/
├── .github/
│   └── workflows/
│       ├── build.yml          # 完整构建工作流
│       └── quick-build.yml    # 快速构建工作流
├── main_monitor_dynamic.py    # 主程序
├── network_monitor.py         # 网络监控
├── config_with_yolo.yaml      # 配置文件
├── requirements_clean.txt     # 依赖文件
├── start_monitor.bat          # Windows启动脚本
├── start_monitor.sh           # Linux/macOS启动脚本
├── sounds/                    # 音频文件
├── test_img/                  # 测试图片
├── fuzzy_matcher.py           # 模糊匹配
├── config_manager.py          # 配置管理
└── README.md                  # 说明文档
```

## 使用方法

### 1. 创建独立仓库

```bash
# 1. 创建新目录
mkdir chat-monitor-package
cd chat-monitor-package

# 2. 复制 doPackage 内容
cp -r ../yolov5-popup-detector/doPackage/* .

# 3. 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 4. 在 GitHub 上创建新仓库
# 5. 推送代码
git remote add origin https://github.com/yourusername/chat-monitor-package.git
git branch -M main
git push -u origin main
```

### 2. 触发构建

#### 自动触发
- 推送到 `main` 或 `master` 分支
- 创建 Pull Request
- 发布 Release

#### 手动触发
1. 在 GitHub 仓库页面
2. 点击 "Actions" 标签
3. 选择 "Quick Build" 工作流
4. 点击 "Run workflow"

### 3. 下载构建产物

构建完成后，可以在 Actions 页面下载：
- Windows: `chat_monitor_Windows.zip`
- Linux: `chat_monitor_Linux.tar.gz`
- macOS: `chat_monitor_macOS.tar.gz`

## 工作流说明

### Quick Build (推荐)

**触发条件**: Push 到主分支或手动触发
**构建平台**: Windows, Linux, macOS
**Python 版本**: 3.10
**构建时间**: ~10-15 分钟

**特点**:
- 快速构建
- 单文件可执行程序
- 包含所有必要文件
- 适合日常使用

### Full Build

**触发条件**: Push 到主分支、PR 或发布 Release
**构建平台**: Windows, Linux, macOS
**Python 版本**: 3.9, 3.10, 3.11
**构建时间**: ~30-45 分钟

**特点**:
- 多版本支持
- 自动发布到 Release
- 完整测试
- 适合正式发布

## 配置说明

### 依赖文件

`requirements_clean.txt` 包含最小依赖：
```
opencv-python>=4.5.0
numpy>=1.21.0
Pillow>=8.0.0
PyYAML>=5.4.0
watchdog>=2.1.0
```

### 构建参数

PyInstaller 参数：
- `--onefile`: 打包成单个可执行文件
- `--windowed`: Windows 下隐藏控制台窗口
- `--name`: 指定可执行文件名称

### 系统依赖

Linux 系统需要安装：
```bash
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
```

## 自定义配置

### 修改构建参数

编辑 `.github/workflows/quick-build.yml`:

```yaml
- name: Build executable
  run: |
    pyinstaller --onefile --hidden-import=cv2 --name chat_monitor main_monitor_dynamic.py
```

### 添加新的 Python 版本

```yaml
strategy:
  matrix:
    os: [windows-latest, ubuntu-latest, macos-latest]
    python-version: [3.9, 3.10, 3.11]  # 添加版本
```

### 修改触发条件

```yaml
on:
  push:
    branches: [ main, develop ]  # 添加分支
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # 每周日构建
```

## 故障排除

### 常见问题

1. **构建失败**
   - 检查依赖文件是否正确
   - 确认 Python 版本兼容性
   - 查看构建日志

2. **文件缺失**
   - 确保所有必要文件都在仓库中
   - 检查文件路径是否正确

3. **权限问题**
   - Linux/macOS 需要设置执行权限
   - 确保脚本文件可执行

### 调试方法

1. **本地测试**
   ```bash
   pip install -r requirements_clean.txt
   pyinstaller --onefile main_monitor_dynamic.py
   ```

2. **查看构建日志**
   - 在 Actions 页面查看详细日志
   - 检查错误信息

3. **测试可执行文件**
   - 下载构建产物
   - 在目标系统上测试

## 优化建议

### 构建优化

1. **缓存依赖**
   ```yaml
   - name: Cache pip dependencies
     uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements_clean.txt') }}
   ```

2. **并行构建**
   - 使用矩阵策略并行构建
   - 减少总体构建时间

3. **增量构建**
   - 只构建变更的文件
   - 使用缓存加速构建

### 发布优化

1. **自动版本号**
   ```yaml
   - name: Generate version
     run: echo "VERSION=$(date +'%Y%m%d.%H%M')" >> $GITHUB_ENV
   ```

2. **发布说明**
   - 自动生成 changelog
   - 包含构建信息

3. **签名验证**
   - 对可执行文件进行签名
   - 提供校验和

## 安全考虑

1. **依赖安全**
   - 定期更新依赖版本
   - 检查安全漏洞

2. **代码审查**
   - 启用 PR 审查
   - 使用 Dependabot

3. **访问控制**
   - 限制 Actions 权限
   - 使用最小权限原则

## 扩展功能

### 添加测试

```yaml
- name: Run tests
  run: |
    pip install pytest
    pytest tests/
```

### 代码质量检查

```yaml
- name: Lint code
  run: |
    pip install flake8 black
    flake8 .
    black --check .
```

### 自动部署

```yaml
- name: Deploy to server
  if: github.ref == 'refs/heads/main'
  run: |
    # 部署脚本
```

## 联系支持

如果遇到问题，可以：
1. 查看 GitHub Issues
2. 提交 Bug 报告
3. 参与讨论 