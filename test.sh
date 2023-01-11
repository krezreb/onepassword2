set -eu

python3 -m venv venv

mkdir tmp || true

source .envrc
source venv/bin/activate

pip install twine setuptools wheel

pip install  onepassword2

bash