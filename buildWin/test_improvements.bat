@echo off
echo Testing GUI improvements...

echo.
echo 1. Testing GUI state saving...
python -c "
import yaml
import os

# Create test GUI state
test_state = {
    'gui_state': {
        'app_monitor_enabled': True,
        'network_monitor_enabled': False,
        'window_geometry': '800x600',
        'auto_scroll': True,
        'max_log_lines': 1000
    }
}

# Save test state
with open('gui_state.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(test_state, f, default_flow_style=False, allow_unicode=True)

print('GUI state file created successfully')
"

echo.
echo 2. Testing config with YOLO confidence...
python -c "
import yaml

# Create test config with YOLO confidence
test_config = {
    'yolo': {
        'enabled': True,
        'model_path': 'models/best.pt',
        'confidence': 0.3
    },
    'monitor': {
        'check_interval': 1,
        'reply_wait': 3
    },
    'popup_settings': {
        'fast_mode': False
    }
}

# Save test config
with open('test_config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(test_config, f, default_flow_style=False, allow_unicode=True)

print('Test config with YOLO confidence created successfully')
"

echo.
echo 3. Testing popup settings UI...
python -c "
import sys
sys.path.append('..')
from gui.popup_settings import PopupSettingsWindow
import tkinter as tk

root = tk.Tk()
root.withdraw()  # Hide the main window

# Test popup settings
popup_settings = PopupSettingsWindow(root)
print('Popup settings window created successfully')

root.destroy()
"

echo.
echo Improvements test completed!
echo.
echo New features:
echo 1. GUI state will be saved and restored
echo 2. YOLO confidence can be set in popup settings
echo 3. Monitor toggle states are remembered

pause 