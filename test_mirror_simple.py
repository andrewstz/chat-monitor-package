#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版PyPI镜像源测试
使用urllib，无需额外依赖
"""

import urllib.request
import urllib.error
import time
import ssl

def test_mirror_simple(mirror_name, mirror_url, timeout=10):
    """
    测试单个镜像源的可用性（简化版）
    """
    start_time = time.time()
    success = False
    error_msg = ""
    
    try:
        # 创建请求
        test_url = f"{mirror_url}/simple/"
        req = urllib.request.Request(test_url)
        
        # 设置超时
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.getcode() == 200:
                success = True
                response_time = time.time() - start_time
                print(f"✅ {mirror_name}: {response_time:.2f}s")
                return (mirror_name, mirror_url, success, response_time, "")
            else:
                error_msg = f"HTTP {response.getcode()}"
                
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            error_msg = f"连接失败: {e.reason}"
        elif hasattr(e, 'code'):
            error_msg = f"HTTP错误: {e.code}"
        else:
            error_msg = "未知URLError"
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP错误: {e.code}"
    except Exception as e:
        error_msg = f"未知错误: {str(e)}"
    
    response_time = time.time() - start_time
    print(f"❌ {mirror_name}: {error_msg}")
    return (mirror_name, mirror_url, success, response_time, error_msg)

def main():
    print("🔍 开始测试PyPI镜像源可用性（简化版）...")
    print("=" * 60)
    
    # 镜像源列表
    mirrors = [
        # 国内镜像源
        ("清华大学", "https://pypi.tuna.tsinghua.edu.cn/simple"),
        ("阿里云", "https://mirrors.aliyun.com/pypi/simple"),
        ("中国科技大学", "https://pypi.mirrors.ustc.edu.cn/simple"),
        ("豆瓣", "https://pypi.douban.com/simple"),
        ("华为云", "https://mirrors.huaweicloud.com/repository/pypi/simple"),
        ("腾讯云", "https://mirrors.cloud.tencent.com/pypi/simple"),
        ("网易", "https://mirrors.163.com/pypi/simple"),
        ("搜狐", "https://mirrors.sohu.com/pypi/simple"),
        
        # 国外镜像源（备用）
        ("PyPI官方", "https://pypi.org/simple"),
        ("PyPI官方备用", "https://files.pythonhosted.org/simple"),
        
        # 其他备用源
        ("中科院", "https://pypi.mirrors.ustc.edu.cn/simple"),
        ("北京外国语大学", "https://mirrors.bfsu.edu.cn/pypi/simple"),
        ("上海交通大学", "https://mirrors.sjtug.sjtu.edu.cn/pypi/simple"),
    ]
    
    print("📋 测试镜像源基本连接...")
    print("-" * 60)
    
    # 逐个测试镜像源
    results = []
    for name, url in mirrors:
        result = test_mirror_simple(name, url)
        results.append(result)
        time.sleep(0.5)  # 避免请求过快
    
    # 按响应时间排序
    successful_results = [r for r in results if r[2]]  # 成功的
    failed_results = [r for r in results if not r[2]]  # 失败的
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    if successful_results:
        print("\n✅ 可用的镜像源（按速度排序）:")
        print("-" * 60)
        successful_results.sort(key=lambda x: x[3])  # 按响应时间排序
        
        for i, (name, url, success, response_time, error) in enumerate(successful_results, 1):
            print(f"{i:2d}. {name:15s} | {response_time:6.2f}s | {url}")
    
    if failed_results:
        print(f"\n❌ 不可用的镜像源 ({len(failed_results)}个):")
        print("-" * 60)
        for name, url, success, response_time, error in failed_results:
            print(f"    {name:15s} | {error}")
    
    # 生成推荐配置
    print("\n" + "=" * 60)
    print("💡 推荐配置")
    print("=" * 60)
    
    if successful_results:
        best_mirror = successful_results[0]
        print(f"推荐使用: {best_mirror[0]} ({best_mirror[1]})")
        print(f"响应时间: {best_mirror[3]:.2f}秒")
        
        print("\n在构建脚本中使用:")
        print(f"uv pip install package_name -i {best_mirror[1]}")
        
        # 生成备用方案
        if len(successful_results) > 1:
            print(f"\n备用方案（如果主源失败）:")
            for i, (name, url, success, response_time, error) in enumerate(successful_results[1:4], 2):
                print(f"{i}. {name}: {url}")
    else:
        print("❌ 没有找到可用的镜像源")
        print("建议:")
        print("1. 检查网络连接")
        print("2. 尝试使用代理")
        print("3. 联系网络管理员")
    
    print("\n" + "=" * 60)
    print("📝 使用说明")
    print("=" * 60)
    print("1. 将推荐的镜像源URL复制到构建脚本中")
    print("2. 替换原有的 -i 参数后的URL")
    print("3. 如果主源失败，可以尝试备用源")
    print("4. 建议在构建脚本中添加多个备用源")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试过程中出现错误: {e}")
    
    input("\n按回车键退出...") 