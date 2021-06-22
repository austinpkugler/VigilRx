from web3 import Web3


def create_prescription(prescription):
    # ABI and address used to create contract https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.contract
    print(f'{prescription}')


def get_prescriptions():
    return [
        {
            'name': 'Aspirin',
            'ndc': '89342875',
            'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
            'date': 'June 18, 2021'
        },
        {
            'name': 'Hydrocodone',
            'ndc': '532634634453',
            'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
            'date': 'June 12, 2021'
        },
        {
            'name': 'Fentanyl',
            'ndc': '3253434553',
            'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
            'date': 'November 18, 2020'
        }
    ]
