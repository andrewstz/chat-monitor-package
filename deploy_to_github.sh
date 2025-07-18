#!/bin/bash

# 部署脚本 - 将 doPackage 部署到独立的 GitHub 仓库

set -e

# 配置变量
REPO_NAME="chat-monitor-package"
GITHUB_USERNAME=""
BRANCH="main"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查依赖
check_dependencies() {
    print_step "检查依赖..."
    
    if ! command -v git &> /dev/null; then
        print_error "Git 未安装，请先安装 Git"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装，请先安装 Python3"
        exit 1
    fi
    
    print_message "依赖检查完成"
}

# 获取用户输入
get_user_input() {
    print_step "获取配置信息..."
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo -n "请输入 GitHub 用户名: "
        read GITHUB_USERNAME
    fi
    
    if [ -z "$GITHUB_USERNAME" ]; then
        print_error "GitHub 用户名不能为空"
        exit 1
    fi
    
    echo -n "请输入仓库名称 (默认: $REPO_NAME): "
    read input_repo_name
    if [ ! -z "$input_repo_name" ]; then
        REPO_NAME="$input_repo_name"
    fi
    
    print_message "配置信息: 用户名=$GITHUB_USERNAME, 仓库=$REPO_NAME"
}

# 创建临时目录
create_temp_dir() {
    print_step "创建临时目录..."
    
    TEMP_DIR=$(mktemp -d)
    print_message "临时目录: $TEMP_DIR"
}

# 复制文件
copy_files() {
    print_step "复制文件到临时目录..."
    
    # 复制主要文件
    cp main_monitor_dynamic.py "$TEMP_DIR/"
    cp network_monitor.py "$TEMP_DIR/"
    cp config_with_yolo.yaml "$TEMP_DIR/"
    cp requirements_clean.txt "$TEMP_DIR/"
    cp start_monitor.bat "$TEMP_DIR/"
    cp start_monitor.sh "$TEMP_DIR/"
    cp fuzzy_matcher.py "$TEMP_DIR/"
    cp config_manager.py "$TEMP_DIR/"
    cp README.md "$TEMP_DIR/"
    
    # 复制目录
    if [ -d "sounds" ]; then
        cp -r sounds "$TEMP_DIR/"
    fi
    
    if [ -d "test_img" ]; then
        cp -r test_img "$TEMP_DIR/"
    fi
    
    # 复制 GitHub Actions 配置
    mkdir -p "$TEMP_DIR/.github/workflows"
    cp .github/workflows/*.yml "$TEMP_DIR/.github/workflows/"
    
    print_message "文件复制完成"
}

# 创建 .gitignore
create_gitignore() {
    print_step "创建 .gitignore..."
    
    cat > "$TEMP_DIR/.gitignore" << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
EOF

    print_message ".gitignore 创建完成"
}

# 初始化 Git 仓库
init_git_repo() {
    print_step "初始化 Git 仓库..."
    
    cd "$TEMP_DIR"
    
    git init
    git add .
    git commit -m "Initial commit: Chat Monitor Package"
    
    print_message "Git 仓库初始化完成"
}

# 创建 GitHub 仓库
create_github_repo() {
    print_step "创建 GitHub 仓库..."
    
    # 检查是否已安装 GitHub CLI
    if command -v gh &> /dev/null; then
        print_message "使用 GitHub CLI 创建仓库..."
        
        # 检查是否已登录
        if ! gh auth status &> /dev/null; then
            print_warning "GitHub CLI 未登录，请先运行: gh auth login"
            print_message "或者手动在 GitHub 上创建仓库: https://github.com/new"
            return
        fi
        
        # 创建仓库
        gh repo create "$GITHUB_USERNAME/$REPO_NAME" \
            --public \
            --description "Chat Monitor Package - Automated build with GitHub Actions" \
            --source="$TEMP_DIR" \
            --remote="origin" \
            --push
        
        print_message "GitHub 仓库创建完成: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    else
        print_warning "GitHub CLI 未安装，请手动创建仓库"
        print_message "1. 访问: https://github.com/new"
        print_message "2. 仓库名称: $REPO_NAME"
        print_message "3. 选择 Public"
        print_message "4. 不要初始化 README、.gitignore 或 license"
        print_message "5. 创建仓库后，运行以下命令:"
        echo ""
        echo "cd $TEMP_DIR"
        echo "git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        echo "git branch -M $BRANCH"
        echo "git push -u origin $BRANCH"
        echo ""
    fi
}

# 推送代码
push_code() {
    print_step "推送代码到 GitHub..."
    
    cd "$TEMP_DIR"
    
    # 检查远程仓库是否已添加
    if ! git remote get-url origin &> /dev/null; then
        git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    fi
    
    git branch -M "$BRANCH"
    git push -u origin "$BRANCH"
    
    print_message "代码推送完成"
}

# 显示后续步骤
show_next_steps() {
    print_step "部署完成！后续步骤:"
    echo ""
    print_message "1. 访问仓库: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    print_message "2. 检查 Actions 标签页，查看构建状态"
    print_message "3. 等待构建完成后下载可执行文件"
    print_message "4. 测试构建产物是否正常工作"
    echo ""
    print_warning "注意: 首次构建可能需要 10-15 分钟"
    echo ""
    print_message "临时目录: $TEMP_DIR"
    print_message "如需清理，请运行: rm -rf $TEMP_DIR"
}

# 清理临时目录
cleanup() {
    if [ ! -z "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        print_step "清理临时目录..."
        rm -rf "$TEMP_DIR"
        print_message "清理完成"
    fi
}

# 主函数
main() {
    print_message "开始部署 Chat Monitor Package 到 GitHub..."
    echo ""
    
    # 设置错误处理
    trap cleanup EXIT
    
    check_dependencies
    get_user_input
    create_temp_dir
    copy_files
    create_gitignore
    init_git_repo
    create_github_repo
    push_code
    show_next_steps
    
    print_message "部署流程完成！"
}

# 显示帮助信息
show_help() {
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -u, --user     指定 GitHub 用户名"
    echo "  -r, --repo     指定仓库名称"
    echo "  -b, --branch   指定分支名称 (默认: main)"
    echo ""
    echo "示例:"
    echo "  $0"
    echo "  $0 -u myusername -r my-chat-monitor"
    echo "  $0 --user myusername --repo my-chat-monitor --branch develop"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -u|--user)
            GITHUB_USERNAME="$2"
            shift 2
            ;;
        -r|--repo)
            REPO_NAME="$2"
            shift 2
            ;;
        -b|--branch)
            BRANCH="$2"
            shift 2
            ;;
        *)
            print_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 运行主函数
main 