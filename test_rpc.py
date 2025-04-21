from web3 import Web3
import os
from dotenv import load_dotenv


def test_block_number():
    url = 'https://rpc.ankr.com/eth/595f40ef102171f483bac0b16b78a39669987f446f24ad94955062bb06be39c7'  # URL string

    web3 = Web3(Web3.HTTPProvider(url))
    if web3.is_connected():
        print(f"Connected to Ethereum network. Current block number: {web3.eth.block_number}")
    else:
        print("Failed to connect to the Ethereum network.")

# Вызов функции
test_block_number()

# Загрузка переменных окружения из файла .env
load_dotenv()

# Ваш API-ключ от Alchemy
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')

# Данные о сетях с использованием Alchemy
DATA = {
    'ethereum':     {'rpc': f'https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}',         'scan': 'https://etherscan.io/tx',              'token': 'ETH', 'chain_id': 1},
    'optimism':     {'rpc': f'https://opt-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}',         'scan': 'https://optimistic.etherscan.io/tx',   'token': 'ETH', 'chain_id': 10},
    'bsc':          {'rpc': f'https://bsc-dataseed.binance.org',                                'scan': 'https://bscscan.com/tx',               'token': 'BNB', 'chain_id': 56},
    'polygon':      {'rpc': f'https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}',      'scan': 'https://polygonscan.com/tx',           'token': 'MATIC','chain_id': 137},
    'polygon_zkevm':{'rpc': 'https://zkevm-rpc.com',                                           'scan': 'https://zkevm.polygonscan.com/tx',     'token': 'ETH', 'chain_id': 1101},
    'arbitrum':     {'rpc': f'https://arb-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}',         'scan': 'https://arbiscan.io/tx',               'token': 'ETH', 'chain_id': 42161},
    'avalanche':    {'rpc': 'https://api.avax.network/ext/bc/C/rpc',                          'scan': 'https://snowtrace.io/tx',              'token': 'AVAX','chain_id': 43114},
    'fantom':       {'rpc': f'https://fantom-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}',          'scan': 'https://ftmscan.com/tx',               'token': 'FTM', 'chain_id': 250},
    'nova':         {'rpc': 'https://nova.arbitrum.io/rpc',                                   'scan': 'https://nova.arbiscan.io/tx',          'token': 'ETH', 'chain_id': 42170},
    'zksync':       {'rpc': 'https://mainnet.era.zksync.io',                                  'scan': 'https://explorer.zksync.io/tx',        'token': 'ETH', 'chain_id': 324},
    'celo':         {'rpc': 'https://1rpc.io/celo',                                           'scan': 'https://celoscan.io/tx',               'token': 'CELO','chain_id': 42220},
    'gnosis':       {'rpc': 'https://1rpc.io/gnosis',                                         'scan': 'https://gnosisscan.io/tx',             'token': 'xDAI','chain_id': 100},
    'core':         {'rpc': 'https://rpc.coredao.org',                                        'scan': 'https://scan.coredao.org/tx',          'token': 'CORE','chain_id': 1116},
    'harmony':      {'rpc': 'https://api.harmony.one',                                        'scan': 'https://explorer.harmony.one/tx',      'token': 'ONE', 'chain_id': 1666600000},
    'klaytn':       {'rpc': 'https://public-node-api.klaytnapi.com/v1/cypress',               'scan': 'https://klaytnscope.com/tx/',          'token': 'KLAY', 'chain_id': 8217},
    'moonbeam':     {'rpc': f'https://moonbeam.api.onfinality.io/public',                    'scan': 'https://moonscan.io/tx',               'token': 'GLMR','chain_id': 1284},
    'moonriver':    {'rpc': 'https://moonriver.public.blastapi.io',                             'scan': 'https://moonriver.moonscan.io/tx',     'token': 'MOVR','chain_id': 1285},
    'linea':        {'rpc': 'https://rpc.linea.build',                                        'scan': 'https://lineascan.build/tx',           'token': 'ETH', 'chain_id': 59144},
    'base':         {'rpc': 'https://mainnet.base.org',                                       'scan': 'https://basescan.org/tx',              'token': 'ETH', 'chain_id': 8453},
}

def check_rpc_connections(data):
    failed_connections = []

    for network, info in data.items():
        rpc_url = info['rpc']
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if w3.is_connected():
                print(f"Successfully connected to {network} ({rpc_url})")
            else:
                print(f"Failed to connect to {network} ({rpc_url})")
                failed_connections.append(network)
        except Exception as e:
            print(f"Error connecting to {network} ({rpc_url}): {e}")
            failed_connections.append(network)

    return failed_connections

# Вызов функции
if __name__ == "__main__":
    failed_connections = check_rpc_connections(DATA)
    if failed_connections:
        print("\nFailed to connect to the following networks:")
        for network in failed_connections:
            print(f"- {network}")
    else:
        print("\nAll RPC connections are successful.")



# Данные о сетях с использованием Alchemy
DATA = {
    'optimism': {
        'w3': Web3(Web3.HTTPProvider(f'https://opt-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}')),
        'scan': 'https://optimistic.etherscan.io/tx'
    },
    'bsc': {
        'w3': Web3(Web3.HTTPProvider(f'https://bsc-dataseed.binance.org')),
        'scan': 'https://bscscan.com/tx'
    },
    'polygon': {
        'w3': Web3(Web3.HTTPProvider(f'https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}')),
        'scan': 'https://polygonscan.com/tx'
    },
    'arbitrum': {
        'w3': Web3(Web3.HTTPProvider(f'https://arb-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}')),
        'scan': 'https://arbiscan.io/tx'
    },
    'avalanche': {
        'w3': Web3(Web3.HTTPProvider(f'https://api.avax.network/ext/bc/C/rpc')),
        'scan': 'https://snowtrace.io/tx'
    },
    'fantom': {
        'w3': Web3(Web3.HTTPProvider(f'https://fantom-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}')),
        'scan': 'https://ftmscan.com/tx'
    },
    'gnosis': {
        'w3': Web3(Web3.HTTPProvider('https://1rpc.io/gnosis')),
        'scan': 'https://gnosisscan.io/tx'
    },
    'celo': {
        'w3': Web3(Web3.HTTPProvider('https://1rpc.io/celo')),
        'scan': 'https://celoscan.io/tx'
    }
}

def check_rpc_connections(data):
    failed_connections = []

    for network, info in data.items():
        rpc_url = info['rpc']
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if w3.is_connected():
                print(f"Successfully connected to {network} ({rpc_url})")
            else:
                print(f"Failed to connect to {network} ({rpc_url})")
                failed_connections.append(network)
        except Exception as e:
            print(f"Error connecting to {network} ({rpc_url}): {e}")
            failed_connections.append(network)

    return failed_connections

# Вызов функции
if __name__ == "__main__":
    failed_connections = check_rpc_connections(DATA)
    if failed_connections:
        print("\nFailed to connect to the following networks:")
        for network in failed_connections:
            print(f"- {network}")
    else:
        print("\nAll RPC connections are successful.")