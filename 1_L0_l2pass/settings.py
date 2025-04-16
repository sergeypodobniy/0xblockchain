MAX_GWEI = 100          # гвей лимит
RETRY = 1               # попытки отправить транзакцию
SLEEP_FROM = 300          # сон от
SLEEP_TO = 450           # сон до

RANDOM_WALLETS = True # True / False


COUNT_TX = [0, 1] #от 1 до 2 транзакций

#['polygon', 'fantom', 'arbitrum nova', 'base', 'gnosis', 'optimism', 'moonbeam', 'moonriver', 'celo', 'kava evm', 'fuse', 'mantle']
FROM_CHAINS = ['polygon', 'fantom', 'arbitrum nova', 'base', 'gnosis', 'optimism', 'moonbeam', 'moonriver', 'celo', 'kava evm', 'fuse', 'mantle']

COUNT_NATIV = [0.00001, 0.00002] #от 0.00001 до 0.00002 нативного токена приемника

MIN_NATIV = {
    'optimism':         0.00008,
    'bsc':              0.0015,
    'arbitrum':         0.00012,
    'polygon':          0.1,
    'celo':             0.1,
    'gnosis':           0.07,
    'moonbeam':         0.3,
    'fantom':           0.2,
    'arbitrum nova':    0.0001,
    'base':             0.0001,
    'moonriver':        0.1,
    'kava evm':         0.5,
    'fuse':             0.5,
    'mantle':           0.2,
}
