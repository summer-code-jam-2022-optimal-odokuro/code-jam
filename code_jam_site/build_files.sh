# build_files.sh
python3 -m venv virtual-env
source virtual-env/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic
