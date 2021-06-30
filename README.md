# VigilRx

## Setup Commands
Create and activate a Python environment (Linux):
```
VigilRx> python3 -m venv env
VigilRx> source env/bin/activate
```

Create and activate Python environment (Windows):
```
VigilRx> python3 -m venv env
VigilRx> source env\Scripts\activate.bat
```

Install Python dependences:
```
VigilRx> pip install -r requirements.txt
```

Install and run Ganache (Linux):
```
VigilRx> npm install ganache-cli web3
VigilRx> node_modules/.bin/ganache-cli
```

Compile Solidity smart contracts:
```
VigilRx/VigilRx> python build.py --action=compile
```

Run Django web server:
```
VigilRx/VigilRx> python build.py --action=app
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
