@echo off
echo Fixing debug log path for Windows...

echo Creating Windows-compatible debug log...
(
echo import os
echo import tempfile
echo.
echo def get_debug_log_path():
echo     return os.path.join(tempfile.gettempdir(), "chatmonitor_debug.log")
echo.
echo def debug_log(msg):
echo     try:
echo         with open(get_debug_log_path(), "a", encoding="utf-8") as f:
echo             import datetime
echo             timestamp = datetime.datetime.now().strftime("%%Y-%%m-%%d %%H:%%M:%%S")
echo             f.write(f"[{timestamp}] {msg}\n")
echo     except Exception as e:
echo         pass
echo.
echo def clear_debug_log():
echo     try:
echo         with open(get_debug_log_path(), "w", encoding="utf-8") as f:
echo             pass
echo     except Exception as e:
echo         pass
) > "debug_log_fix.py"

echo Running debug log fix...
python debug_log_fix.py

echo Debug log path fixed!
pause 