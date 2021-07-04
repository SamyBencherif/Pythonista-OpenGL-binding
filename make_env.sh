
echo Creating virtual environment.
python3 -m venv pythonista-venv

echo Installing local modules.
cp -r contents/* pythonista-venv/lib/python3.9/site-packages

echo Starting virtual environment.
source pythonista-venv/bin/activate

echo Installing network modules.
pip install numpy
pip install pyglet
