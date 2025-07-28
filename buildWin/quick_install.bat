@echo off
echo Installing dependencies...

conda install -y -c conda-forge opencv pillow requests pyyaml psutil pygame pyinstaller
pip install ultralytics

echo Done!
pause 