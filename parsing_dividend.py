import urllib.request
from bs4 import BeautifulSoup
from global_define import RESULT_PATH

yahooDividendUrl = 'https://tw.stock.yahoo.com/d/s/dividend_{number}.html'
def parseDividend(stockId) :
    parseURL = yahooDividendUrl.format(number = stockId)
    try :
        htmlDoc = urllib.request.urlopen(parseURL)
    except :
        print('Url error')
        print(parseURL)
        return None
    parser = BeautifulSoup(htmlDoc.read())
    # hard coed find dividend table
    dividendTable = parser.find('table', width='100%', border='0', cellspacing='1', cellpadding='3')
    
    if not RESULT_PATH.exists() :
        RESULT_PATH.mkdir()
    try :
        out = open(str(RESULT_PATH) + '/dividend_{number}.csv'.format(number = stockId), 'w')
        for row in dividendTable.find_all('tr') :
            excludeIndex = 0
            for column in row.find_all('td') :
                # remove redundent white space
                if not excludeIndex in range(1, 5) :
                    out.write(column.string.replace(' ', '').replace('　', '') + ',')
                excludeIndex += 1
            out.write('\n')
    except Exception as e :
        print('Open file error\n' + e)
    finally :
        out.close()

if __name__ == '__main__' :
    parseDividend('1732')