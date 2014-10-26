from pathlib import Path

RESULT_PATH = Path('./result_CSV')

def getDividendFilePath(stockId) :
    assert RESULT_PATH.exists(), str(RESULT_PATH) + 'path not exists'
    return str(RESULT_PATH) + '/dividend_{number}.csv'.format(number = stockId)

def getPriceFilePath(stockId) :
    assert RESULT_PATH.exists(), str(RESULT_PATH) + 'path not exists'
    return str(RESULT_PATH) + '/avgPrice_{number}.csv'.format(number = stockId)