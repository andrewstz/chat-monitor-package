# 快速开始 - GitHub Actions 自动打包

## 🚀 一键部署

### 方法一：使用部署脚本（推荐）

```bash
# 进入 doPackage 目录
cd yolov5-popup-detector/doPackage

# 运行部署脚本
./deploy_to_github.sh
```

脚本会自动：
1. 检查依赖
2. 获取 GitHub 用户名
3. 创建临时目录
4. 复制所有必要文件
5. 初始化 Git 仓库
6. 创建 GitHub 仓库
7. 推送代码

### 方法二：手动部署

```bash
# 1. 创建新目录
mkdir chat-monitor-package
cd chat-monitor-package

# 2. 复制 doPackage 内容
cp -r ../yolov5-popup-detector/doPackage/* .

# 3. 初始化 Git
git init
git add .
git commit -m "Initial commit"

# 4. 在 GitHub 上创建新仓库
# 访问: https://github.com/new

# 5. 推送代码
git remote add origin https://github.com/yourusername/chat-monitor-package.git
git branch -M main
git push -u origin main
```

## 📦 构建产物

构建完成后，在 GitHub Actions 页面可以下载：

- **Windows**: `chat_monitor_Windows.zip`
- **Linux**: `chat_monitor_Linux.tar.gz`  
- **macOS**: `chat_monitor_macOS.tar.gz`

## ⚡ 快速构建

1. 访问你的 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Quick Build" 工作流
4. 点击 "Run workflow"
5. 等待 10-15 分钟完成构建

## 🔧 自定义配置

### 修改构建参数

编辑 `.github/workflows/quick-build.yml`:

```yaml
- name: Build executable
  run: |
    pyinstaller --onefile --hidden-import=cv2 --name chat_monitor main_monitor_dynamic.py
```

### 添加 Python 版本

```yaml
strategy:
  matrix:
    os: [windows-latest, ubuntu-latest, macos-latest]
    python-version: [3.9, 3.10, 3.11]  # 添加版本
```

## 📋 文件说明

| 文件 | 说明 |
|------|------|
| `main_monitor_dynamic.py` | 主程序（动态配置） |
| `network_monitor.py` | 网络监控模块 |
| `config_with_yolo.yaml` | 配置文件 |
| `requirements_clean.txt` | 最小依赖 |
| `start_monitor.bat` | Windows 启动脚本 |
| `start_monitor.sh` | Linux/macOS 启动脚本 |
| `fuzzy_matcher.py` | 模糊匹配模块 |
| `config_manager.py` | 配置管理模块 |

## 🛠️ 故障排除

### 构建失败

1. 检查依赖文件 `requirements_clean.txt`
2. 确认 Python 版本兼容性
3. 查看 Actions 构建日志

### 文件缺失

1. 确保所有必要文件都在仓库中
2. 检查文件路径是否正确
3. 验证 `.github/workflows/` 目录存在

### 权限问题

1. Linux/macOS 需要设置执行权限
2. 确保脚本文件可执行
3. 检查 GitHub Actions 权限设置

## 📞 获取帮助

- 查看详细文档：`README_GitHub_Actions.md`
- 检查构建日志：GitHub Actions 页面
- 提交 Issue：GitHub 仓库 Issues

## 🎯 下一步

1. 测试构建产物
2. 配置自动发布
3. 添加代码签名
4. 设置自动测试 