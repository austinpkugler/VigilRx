# VigilRx

## Setup Commands (Linux)
Create and activate a Python environment:
```
VigilRx> python3 -m venv env
VigilRx> source env/bin/activate
```

Install Python dependences:
```
(env) VigilRx> pip install -r requirements.txt
```

Install Ganache:
```
(env) VigilRx> npm install ganache-cli web3
```

Build and run VigilRx:
```
(env) VigilRx/VigilRx> python cli.py --action=build
```

## Troubleshooting
If compiling fails, install solc using snap:
```
(env) VigilRx/VigilRx> sudo snap install solc --edge
```
Or using apt:
```
(env) VigilRx/VigilRx> sudo add-apt-repository ppa:ethereum/ethereum
(env) VigilRx/VigilRx> sudo apt-get update
(env) VigilRx/VigilRx> sudo apt-get install solc 
```