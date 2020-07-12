from bs4 import BeautifulSoup
from datetime import datetime
import gspread, json, os, requests

url = "https://web.pref.hyogo.lg.jp/kk03/corona_hasseijyokyo.html"

def getSoup(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.content, 'html.parser')

def getTrs(soup):
    trs = soup.find("table", "datatable").findAll("tr")
    dateUpdatedJa = soup.find("p", {"id": "tmp_update"})
    return trs

def getDateUpdated(soup):
    p = soup.find("p", {"id": "tmp_update"})
    return p.text.strip()

def getDataFromTrs(trs):
    data = [] 
    for tr in trs:
        case = []
        tds = tr.findAll("td")
        for td in tds:
            case.append(td.text.strip())
        data.append(case)
    data.pop(0)
    return data

def readCaseJson():
    with open(os.path.dirname(__file__) + '/hassei.json', 'r') as f:
        data = json.load(f)
    return data

def writeCaseJson(data):
    with open(os.path.dirname(__file__) + '/hassei.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Json saved.")

def getNewCases(data, oldData):
    diff = int(data[0][0]) - int(oldData[0][0])
    return data[0:diff]

def getSheet():
    gc = gspread.service_account()
    return gc.open_by_key('1MJbDJzx8JHVbe9aH--FqkW34eDUczF9WnQvFq9szrzs')

def updateSheet(newCases, yearUpdated):
    sh = getSheet()
    worksheet = sh.worksheet("Hyogo (JA)")
    newCases.reverse()
    if len(newCases) > 0:
        for case in newCases: 
            monthUpdated = len(case[5].split("月")[0]) > 1 \
                           and case[5].split("月")[0] \
                           or "0" + case[5].split("月")[0]
            dayUpdated = len(case[5].split("月")[1].rstrip("日")) > 1 \
                           and case[5].split("月")[1].rstrip("日") \
                           or "0" + case[5].split("月")[1].rstrip("日")
            dateUpdated = yearUpdated + "-" + monthUpdated + "-" + dayUpdated
            data = [case[0], dateUpdated, case[1], case[2], "", case[3], case[4]]
            worksheet.insert_row(data, 2, "USER_ENTERED") 
            print("inserted " + case[0])

def updateDailySummary():
    sh = getSheet()
    
    # Get 2.A2  
    worksheet = sh.worksheet("2.Daily")
    lastDateString = worksheet.get("A2").first()
    lastDateTime = datetime.strptime(lastDateString, "%Y-%m-%d")

    # If 2.A2 < Today, Add days after 2.A2 until today
    today = datetime.now()
    diff = today - lastDateTime
    if diff.days > 0:
        worksheet.insert_row( \
            [today.strftime("%Y-%m-%d"), 0, 0, 0, '=average(D2:D8)'], \
            2, "USER_ENTERED")
        lastDateString = worksheet.get("A2").first()

    # If 2.A2 equals D.A3 then copy D.A3 over
    refWorksheet = sh.worksheet("D")
    pivotLastDateString = refWorksheet.get("A3").first()
    if lastDateString == pivotLastDateString:
        if refWorksheet.acell("B3").value == '':
            female = 0
        else:
            female = refWorksheet.acell("B3").value

        if refWorksheet.acell("C3").value == '': 
            male = 0
        else:
            male = refWorksheet.acell("C3").value

        if refWorksheet.acell("D3").value == '': 
            total = 0
        else:
            total = refWorksheet.acell("D3").value

        worksheet.update("B2", female, raw=False)
        worksheet.update("C2", male, raw=False)
        worksheet.update("D2", total, raw=False)

def main():
    soup = getSoup(url)
    trs = getTrs(soup)
    data = getDataFromTrs(trs)
    oldData = readCaseJson()
    newCases = getNewCases(data, oldData)
    yearUpdated = getDateUpdated(soup)[4:8]

    # Update document for future reference
    if len(newCases) > 0:
        print(newCases)
        writeCaseJson(data)

    # Add New Cases to the Google Spreadsheet
    updateSheet(newCases, yearUpdated)

    # Update the "2.Daily" sheet
    updateDailySummary()

if __name__ == "__main__":
    main()
