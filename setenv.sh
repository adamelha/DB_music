# Set the python3 virtual env
echo "Installing Python virutal enviornment"
virtualenv -p python3 venv

# Getting the pip dependencies
echo "Installing pip requirements"
venv/bin/pip install -r requirements.txt