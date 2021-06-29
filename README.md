# VigilRx

## Setup Commands
Create a Python environment (Linux):
```
python3 -m venv env
source env/bin/activate
```

Create a Python environment (Windows):
```
python3 -m venv env
source env\Scripts\activate.bat
```

Activate Python environment (Linux):
```
source env/bin/activate
```

Activate Python environment (Windows):
```
env/Scripts/activate.bat
```

Install Python dependences:
```
pip install -r requirements.txt
```

## Other Helpful Commands
Create a Django superuser:
```
python manage.py createsuperuser
```

Test migrations before making:
```
python manage.py makemigrations --dry-run
```

Make and apply Django migrations:
```
python manage.py makemigrations
python manage.py migrate
```

Install solc:
```
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc
```
