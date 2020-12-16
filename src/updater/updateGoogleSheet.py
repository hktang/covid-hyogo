from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import gspread
import json
import os
import re
import requests

kensaUrl = "https://web.pref.hyogo.lg.jp/kf16/coronavirus_data.html"

def getSoup(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.content, 'html.parser')


def getKensaTr(soup):
    tr = soup.findAll("table", {"class", "ex_table"})[1].findAll("tr")[3::4]
    return tr[0]


def getTotalConfirmed(soup):
    tr = soup.find("table", {"class", "ex_table"}).findAll("tr")[2::3]
    totalConfirmed = tr[0].findAll("td")[0::1][0].text.replace(',', '')
    return totalConfirmed


def getSheet():
    gc = gspread.service_account()

    # production
    return gc.open_by_key('1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw')

    # Development
    # return gc.open_by_key('1MJbDJzx8JHVbe9aH--FqkW34eDUczF9WnQvFq9szrzs')


def updateKensa():
    soup = getSoup(kensaUrl)
    tr = getKensaTr(soup)
    tds = tr.findAll("td")
    gSheet = getSheet()
    worksheet = gSheet.worksheet("5.Status")
    lastDateString = worksheet.acell("A2").value
    lastDateTime = datetime.strptime(lastDateString, "%Y-%m-%d")
    oldValue = worksheet.acell("B2").value
    newValue = tds[0].text.strip().replace(',', '')

    if(oldValue == newValue):
        print("Status sheet already up-to-date")
        return
    else:
        # Add new row
        data = ['']
        for td in tds:
            data.append(td.text.strip().replace(',', ''))

        worksheet.insert_row(data, 2, "USER_ENTERED")

        # Add date
        newDateTime = lastDateTime + timedelta(days=1)
        newDateString = newDateTime.strftime("%Y-%m-%d")
        worksheet.update("A2", newDateString, raw=False)

        print("Status sheet updated")


def updateTotalConfirmed():
    soup = getSoup(kensaUrl)
    totalConfirmed = getTotalConfirmed(soup)
    gSheet = getSheet()
    worksheet = gSheet.worksheet("7.Totals")

    oldValue = worksheet.acell("B2").value.replace(',', '')

    if(oldValue == totalConfirmed):
        print("Total confirmed unchanged.")
    else:
        worksheet.update("B2", totalConfirmed, raw=False)
        print("Total confirmed updated.")


def main():
    updateKensa()
    updateTotalConfirmed()


if __name__ == "__main__":
    main()
