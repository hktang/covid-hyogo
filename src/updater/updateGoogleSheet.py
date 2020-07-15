from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import gspread
import json
import os
import requests

hasseiUrl = "https://web.pref.hyogo.lg.jp/kk03/corona_hasseijyokyo.html"
kensaUrl = "https://web.pref.hyogo.lg.jp/kk03/200129.html"


def getSoup(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.content, 'html.parser')


def getHasseiTrs(soup):
    trs = soup.find("table", "datatable").findAll("tr")
    return trs


def getKensaTr(soup):
    tr = soup.find("table", {"class", "ex_table"}).findAll("tr")[3::4]
    return tr[0]


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
    with open(os.path.dirname(__file__) + '/hassei.json', 'r', encoding="utf-8" ) as f:
        data = json.load(f)
    return data


def writeCaseJson(data):
    with open(os.path.dirname(__file__) + '/hassei.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Json saved.")


def getNewCases(data, oldData):
    diff = int(data[0][0]) - int(oldData[0][0])
    return data[0:diff]


def getSheet():
    gc = gspread.service_account()
    return gc.open_by_key('1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw')


def updateSheet(sheet, newCases, yearUpdated):
    worksheet = sheet.worksheet("Hyogo (JA)")
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
            data = [case[0], dateUpdated, case[1], case[2],
                    "", case[3], case[4]]
            worksheet.insert_row(data, 2, "USER_ENTERED")
            print("inserted " + case[0])


def updateDailySheet(sheet):

    # Get 2.A2
    worksheet = sheet.worksheet("2.Daily")
    lastDateString = worksheet.get("A2").first()
    lastDateTime = datetime.strptime(lastDateString, "%Y-%m-%d")

    # If 2.A2 < Today, Add days after 2.A2 until today
    today = datetime.now()
    diff = today - lastDateTime
    if diff.days > 0:
        worksheet.insert_row(
            [today.strftime("%Y-%m-%d"), 0, 0, 0, '=average(D2:D8)'],
            2, "USER_ENTERED")
        lastDateString = worksheet.get("A2").first()

    # If 2.A2 equals D.A3 then copy D.A3 over
    refWorksheet = sheet.worksheet("D")
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
        print("Summary sheet updated.")


def updateAgeSheet(sheet):
    worksheet = sheet.worksheet("4.Age")

    refData = worksheet.col_values(4)
    del refData[0]

    oldDeathCol = worksheet.col_values(3)
    del oldDeathCol[0]

    oldDeathCount = 0

    for val in oldDeathCol:
        oldDeathCount += int(val)

    for i, val in enumerate(refData):
        try:
            refValue = int(worksheet.acell("D" + str(i + 1)).value)
            worksheet.update("B" + str(i + 1), refValue, raw=False)
        except:
            continue

    statusSheet = sheet.worksheet("5.Status")
    deathCount = int(statusSheet.acell("G2").value)

    # Update "Undisclosed" group in death count
    undisclosed = int(worksheet.acell("C13").value)
    diff = deathCount - oldDeathCount

    if(diff != 0):
        worksheet.update("C13", undisclosed + diff, raw=False)

    print("Age sheet updated.")


def updateCitySheet(sheet):
    worksheet = sheet.worksheet("3.City")
    refData = worksheet.col_values(5)

    for i, val in enumerate(refData):
        if(i == 0):
            continue
        try:
            refValue = int(worksheet.acell("E" + str(i + 1)).value)
            worksheet.update("D" + str(i + 1), refValue, raw=False)
        except:
            continue

    print("City sheet updated.")


def updateHassei():
    soup = getSoup(hasseiUrl)
    trs = getHasseiTrs(soup)
    data = getDataFromTrs(trs)
    oldData = readCaseJson()
    newCases = getNewCases(data, oldData)
    yearUpdated = getDateUpdated(soup)[4:8]
    gSheet = getSheet()

    # Update document for future reference
    if len(newCases) > 0:
        print(newCases)
        writeCaseJson(data)

    # Add New Cases to the Google Spreadsheet
    updateSheet(gSheet, newCases, yearUpdated)

    # Update the "2.Daily" sheet
    updateDailySheet(gSheet)

    # Update the "3.City" sheet
    updateCitySheet(gSheet)

    # Update the "4.Age" sheet
    updateAgeSheet(gSheet)


def updateKensa():
    soup = getSoup(kensaUrl)
    tr = getKensaTr(soup)
    tds = tr.findAll("td")
    gSheet = getSheet()
    worksheet = gSheet.worksheet("5.Status")
    lastDateString = worksheet.acell("A2").value
    lastDateTime = datetime.strptime(lastDateString, "%Y-%m-%d")
    oldValue = worksheet.acell("B2").value
    newValue = tds[0].text.strip()

    if(oldValue == newValue):
        print("Status sheet already up-to-date")
        return
    else:
        # Add new row
        data = ['']
        for td in tds:
            data.append(td.text.strip())

        worksheet.insert_row(data, 2, "USER_ENTERED")

        # Add date
        newDateTime = lastDateTime + timedelta(days=1)
        newDateString = newDateTime.strftime("%Y-%m-%d")
        worksheet.update("A2", newDateString, raw=False)

        print("Status sheet updated")


def main():
    updateHassei()
    updateKensa()


if __name__ == "__main__":
    main()
