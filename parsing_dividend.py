import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path

yahooDividendUrl = 'https://tw.stock.yahoo.com/d/s/dividend_{number}.html'
resultDir = Path('./result_CSV')
def parseDividend(stockNumber) :
    parseURL = yahooDividendUrl.format(number = stockNumber)
    try :
        htmlDoc = urllib.request.urlopen(parseURL)
    except :
        print('Url error')
        print(parseURL)
        return None
    parser = BeautifulSoup(htmlDoc.read())
    # hard coed find dividend table
    dividendTable = parser.find('table', width='100%', border='0', cellspacing='1', cellpadding='3')
    
    if not resultDir.exists() :
        resultDir.mkdir()
    try :
        out = open(str(resultDir) + '/dividend_{number}.csv'.format(number = stockNumber), 'w')
        for row in dividendTable.find_all('tr') :
            for column in row.find_all('td') :
                # remove redundent white space
                out.write(column.string.replace(' ', '').replace('　', '') + ',')
            out.write('\n')
    except Exception as e :
        print('File error\n' + e)
    finally :
        out.close()