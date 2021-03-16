# https://www.youtube.com/watch?v=XQgXKtPSzUI

from urllib.request import urlopen as uReqOpen
from bs4 import BeautifulSoup as soup
import sys
from datetime import datetime

stockSymbol = sys.argv[1]

filename = stockSymbol + ' data.csv'
f = open(filename, "w")

currentYear = datetime.now().year

headers = "criteria"
for i in range(0, 10):
    headers += ", " + str(currentYear - i)
headers += "\n"

my_url = 'https://www.reuters.com/companies/' + stockSymbol + '/key-metrics'

uClient = uReqOpen(my_url)
page_html = uClient.read()
uClient.close()
page_soup_parsed = soup(page_html, "html.parser")

company_name = page_soup_parsed.findAll("div", {"class": "QuoteRibbon-name-ric-epp2J"})
f.write(company_name[0].h1.text + "," + "," + company_name[0].p.text + "\n\n")

containers = page_soup_parsed.findAll("div", {"class": "KeyMetrics-table-container-3wVZN"})
tr_s = containers[5].div.table.tbody.findAll("tr", {"class": "data"})  # get all the table's lines

KeyMetrics_ROI = [4, 5, 8]


#titles = ""
#values = ""
#for i in KeyMetrics_ROI:
#    titles += tr_s[i].th.text.replace(",", "") + ", "
 #   values += tr_s[i].td.text.replace(",", "") + ", "

#f.write(titles[:len(titles) - 1] + "\n")
#f.write(values[:len(titles) - 1] + "\n")
#f.write("\n")
#f.write(headers)


titles = ""
values = ""
for tr in tr_s:
    if tr.th.text == "Return on Investment (Annual)" or tr.th.text == "Return on Investment (TTM)" or tr.th.text == "Return on Investment (5Y)":
        titles += tr.th.text.replace(",", "") + ", "
        td_s = tr.findAll("td")
        for td in td_s:
            values += td.text.replace(",", "") + ", "

f.write(titles[:len(titles) - 1] + "\n")
f.write(values[:len(titles) - 1] + "\n")

f.write("\n")
f.write(headers)


income_statement_annual = 'https://www.reuters.com/companies/' + stockSymbol + '/financials/income-statement-annual'


uClient = uReqOpen(income_statement_annual)
page_html = uClient.read()
uClient.close()
page_soup_parsed = soup(page_html, "html.parser")

income_statement_table = page_soup_parsed.findAll("div", {"class": "tables-container"})
tr_s = income_statement_table[0].table.tbody.findAll("tr")
# income_statement_lines = [0, 19]


#dates = ""
#for th_dates in income_statement_table[0].table.thead.tr.findAll("th")[1:-1]:
#    print(th_dates.time)
#    dates += ", " + th_dates.time.text.replace(",", "")
#f.write(dates + "\n")

row_map1={}

for tr in tr_s:
    if tr.th.span.text == "Revenue" or tr.th.span.text == "Diluted EPS Excluding ExtraOrd Items" or tr.th.span.text == "Interest Income, Bank":
        line = tr.th.span.text.replace(",", "")
        td_s = tr.findAll("td")
        for td in td_s:
            line += ", " + td.text.replace(",", "")
        row_map1[tr.th.span.text] = line + "\n"

printing_list1 = ["Interest Income, Bank", "Revenue", "Diluted EPS Excluding ExtraOrd Items"]

for nextline1 in printing_list1:
    if row_map1.get(nextline1) is not None:
        f.write(row_map1.get(nextline1))
    elif nextline1 != "Interest Income, Bank":
        f.write(nextline1 + "\n")


# for i in income_statement_lines:
#     line = tr_s[i].th.span.text
#     td_s = tr_s[i].findAll("td")
#     for td in td_s:
#         line += ", " + td.text
#     f.write(line + "\n")

balance_sheet_annual = 'https://www.reuters.com/companies/' + stockSymbol + '/financials/balance-sheet-annual'

uClient = uReqOpen(balance_sheet_annual)
page_html = uClient.read()
uClient.close()
page_soup_parsed = soup(page_html, "html.parser")

balance_sheet_table = page_soup_parsed.findAll("div", {"class": "tables-container"})
tr_s = balance_sheet_table[0].table.tbody.findAll("tr")
# balance_sheet_lines = [31,0,33,20]

row_map2={}

for tr in tr_s:
    if tr.th.span.text == "Total Equity" or tr.th.span.text == "Cash & Equivalents" or tr.th.span.text == "Total Common Shares Outstanding" or tr.th.span.text == "Total Long Term Debt" \
            or tr.th.span.text == "Total Current Assets" or tr.th.span.text == "Total Current Liabilities":
        line = tr.th.span.text.replace(",", "")
        td_s = tr.findAll("td")
        for td in td_s:
            line += ", " + td.text.replace(",", "")
        row_map2[tr.th.span.text] = line + "\n"

printing_list = ["Total Equity", "Cash & Equivalents", "Total Common Shares Outstanding", "Total Long Term Debt", "Total Current Assets", "Total Current Liabilities"]

for nextline2 in printing_list:
    if row_map2.get(nextline2) is not None:
        f.write(row_map2.get(nextline2))
    else:
        f.write(nextline2+ "\n")

# for i in balance_sheet_lines:
#     line = tr_s[i].th.span.text
#     td_s = tr_s[i].findAll("td")
#     for td in td_s:
#         line += ", " + td.text
#     f.write(line + "\n")


f.close()
