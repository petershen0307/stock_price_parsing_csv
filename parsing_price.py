import re
import urllib.request

# combine with stock number and to witch year
twsePriceUrl = 'http://www.twse.com.tw/ch/trading/exchange/FMNPTK/FMNPTK2.php?STK_NO={stockNumber}&myear={untilYear}&mmon=07&type=csv'
def getStockPriceFromWeb(stockId, years):
    urlWithStockAndYear = twsePriceUrl.format(stockNumber = stockId, untilYear = years)
    try :
        webMessage = urllib.request.urlopen(urlWithStockAndYear)
    except :
        print('URL error')
        print(urlWithStockAndYear)
        return False
    #rawdata type is bytes, it need to decode
    rawdata = webMessage.read()
    return rawdata.decode('big5')

from global_define import RESULT_PATH
def getStockYearAndPrice(stockId, years, duringYears = 5):
    parsingYears = '年度'
    parsingAvgPrice = '收盤平均價'
    csvData = getStockPriceFromWeb(stockId, years)
    if False == csvData :
        return False
    lineList = csvData.replace(' ', '').split('\n')
    #remove garbage messages
    removeIndex = [0, len(lineList)-1, len(lineList)-2, len(lineList)-3, len(lineList)-4]
    lineList = [i for j, i in enumerate(lineList) if j not in removeIndex]

    #parse title line
    yearIndex = 0
    avgIndex = 0
    titleLine = lineList.pop(0).split(',')
    try:
        yearIndex = titleLine.index(parsingYears)
        avgIndex = titleLine.index(parsingAvgPrice)
    except ValueError:
        print('pass')
        return False

    #get the stock price
    resultList = [[parsingYears, parsingAvgPrice]]
    avgPrices = []
    for each in lineList :
        tmp = re.sub(r'"[\d,]+"', 'xx', each).split(',')
        resultList.append([int(tmp[yearIndex]), float(tmp[avgIndex])])
        avgPrices.append(float(tmp[avgIndex]))
    print(resultList)

    totalYears = len(avgPrices)
    if totalYears < duringYears or 0 == duringYears:
        totalAvgPrice = float(sum(avgPrices) / totalYears)
    else :
        #[first : second]  list
        # last duringYears
        totalAvgPrice = float(sum(avgPrices[(totalYears - duringYears) : totalYears]) / duringYears)
    resultList.append([str(duringYears) + ' years', totalAvgPrice])

    if not RESULT_PATH.exists() :
        RESULT_PATH.mkdir()
    with open(str(RESULT_PATH) + '/avgPrice_{Id}.csv'.format(Id = stockId), 'w', encoding = 'big5') as writeData :
        for eleList in resultList :
            for eleStr in eleList :
                #detect the type which is Number -> isinstance(eleStr, Number)
                writeData.write(str(eleStr) + ',')
            writeData.write('\n')

if __name__ == '__main__' :
    getStockYearAndPrice('1732', 2014, 0)