# 这网络监控太复杂了，请改回原来那个简单的一个函数的判断即可（只修改main_monitor_dynamic网络监控部分，其他文件不变），注意，为了避免网路抖动的误判，只要1分钟内连续尝试三次网络检测不过就提示声音，1分钟、3次这两个参数从配置中拿

python3 main_monitor_dynamic.py --help 2>/dev/null || echo "测试网络监控功能"
test_simple_network.py
✅ 网络监控简化完成！
我已经按照你的要求简化了网络监控功能：
主要修改：
移除了复杂的 NetworkMonitor 类
使用简单的函数判断：check_network_with_alert()
从配置文件读取参数：
consecutive_failures: 连续失败阈值（默认3次）
tolerance_minutes: 容错时间（默认1分钟）
新的网络监控逻辑：
check_network_with_alert
python3 test_simple_network.py
