# 激活环境到指定python版本
✅ DOS环境下的操作：
1. 检查Python版本（DOS命令）
REM 在buildWin目录中
check_python_versions.bat
2. 使用py launcher指定Python版本
REM 在项目根目录（不是buildWin）
cd ..
uv venv --python "py -3.9" --index-url https://pypi.tuna.tsinghua.edu.cn/simple/
cd buildWin
3. 或者使用 pyproject.toml（推荐）（最简单）
REM 在项目根目录
cd ..
uv sync
cd buildWin
4. 激活环境（DOS方式）
REM 激活虚拟环境
..\.venv\Scripts\activate.bat
REM 检查Python版本
python --version


## uv sync包错。。。是不是要清理重做环境
是的！看到playsound又出现了，说明pyproject.toml中还有playsound依赖。让我清理环境并修复这个问题：
✅ 步骤1: 清理现有环境
clean_environment.bat
✅ 步骤2: 修复pyproject.toml，移除playsound
好的，pyproject.toml看起来没有playsound依赖。问题可能是UV缓存中有旧的playsound信息。让我创建一个完全绕过playsound的pyproject.toml：
✅ 步骤3: 创建使用新配置的脚本
setup_uv_no_playsound_fresh.bat
✅ 现在按这个顺序操作：
步骤1: 清理环境
REM 在buildWin目录中
clean_environment.bat
步骤2: 使用新的无playsound脚本
setup_uv_no_playsound_fresh.bat
步骤3: 验证环境
    REM 激活环境
    ..\.venv\Scripts\activate.bat

    REM 检查Python版本
    python --version

    REM 检查依赖
    python -c "import cv2, numpy, psutil, pyautogui, requests, yaml, PIL, pytesseract, watchdog; print('All dependencies OK')"
步骤4: 运行构建
build_windows_uv_simple_english.bat
✅ 关键改进：
✅ 完全清理: 删除旧的 .venv 目录和UV缓存
✅ 无playsound: 新脚本完全不安装playsound
✅ 使用镜像: 加快下载速度
✅ 智能Python检测: 自动选择可用的Python版本

✅ Python 3.13.5 完全可以！
为什么Python 3.13.5没问题：
✅ 性能更好: 比Python 3.9更快pyproject
✅ 兼容性好: 支持所有需要的包
✅ 稳定性好: 已经发布一段时间了
✅ 功能更全: 有更多新特性
pyproject.toml中的版本要求：requires-python = ">=3.9,<3.14"
这意味着支持Python 3.9到3.13，所以3.13.5完全符合要求！

