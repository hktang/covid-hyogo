from classes.excel import Excel
from classes.gsheet import Gsheet
from datetime import timedelta, date
import numpy
import pandas

excel_params = {
    'url': 'https://web.pref.hyogo.lg.jp/kk03/documents/corona-kanjajokyou.xlsx',
}

# gsheet_key = '1MJbDJzx8JHVbe9aH--FqkW34eDUczF9WnQvFq9szrzs'  # dev
gsheet_key = '1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw'  # prod

gsheet_tabs = {
    1: '1. Hyogo',
    2: '2.Daily',
    3: '3.City',
    4: '4.Age',
    5: '5.Status',
    6: '6. Cluster',
    7: '7.Totals',
    8: 'Hyogo (JA)',
}

age_groups = {
    '10歳未満': '<10',
    '10': '10-19',
    '20': '20-29',
    '30': '30-39',
    '40': '40-49',
    '50': '50-59',
    '60': '60-69',
    '70': '70-79',
    '80': '80-89',
    '90歳以上': '>90',
    '非公表': 'Undisclosed'
}

x_wb = Excel(params=excel_params)
x_ws = x_wb.load_worksheet()
x_case_data = x_wb.get_main_data(x_ws)
x_df = pandas.DataFrame(x_case_data)

g_wb = Gsheet(gsheet_key).get_wb()


def update_main_data_on_gsheet():
    max_col = x_wb.get_column_letter(x_ws.max_column)
    datarange = 'A' + str(x_wb.params['start_row']) + \
        ":" + max_col + str(x_ws.max_row)
    g_ws = g_wb.worksheet(gsheet_tabs[8])
    g_ws.update(datarange, x_case_data)
    print('Case data updated.')


def update_metadata_on_gsheet():
    g_ws = g_wb.worksheet(gsheet_tabs[8])
    g_ws.update(x_wb.params['last_updated_cell'], str(
        x_ws[x_wb.params['last_updated_cell']].value)[0:10])
    g_ws.update(x_wb.params['annotation_cell'],
                x_ws[x_wb.params['annotation_cell']].value)
    print('Timestamp and summary updated.')


def update_daily_data_on_gsheet():

    case_dates = get_unique_by_col(x_case_data, 2)

    start_date = date(2020, 3, 1)
    end_date = x_wb.get_newest_date(x_ws).date()

    daily_data = []

    for single_date in daterange(start_date, end_date):

        date_string = single_date.strftime(x_wb.params['time_format'])

        if date_string in case_dates:
            # total rows on that date
            total = x_df.loc[x_df[2] == date_string]

            # Check Gender column (4)
            female_count = len(total.loc[total[4].str.strip() == '女性'])
            male_count = len(total.loc[total[4].str.strip() == '男性'])
            undisclosed_count = len(total.loc[total[4].str.strip() == '非公表'])

            daily_data.append([date_string, female_count, male_count,
                               undisclosed_count, len(total)])
        else:
            daily_data.append([date_string, 0, 0, 0, 0])

    df = pandas.DataFrame(daily_data)
    df['rolling'] = df.rolling(7).mean()[4].shift(-6)
    data_list = (df.replace(numpy.nan, 0, regex=True).values.tolist())

    g_ws = g_wb.worksheet(gsheet_tabs[2])
    g_ws.update("A2:F", data_list)

    print('Daily sheet updated.')


def update_age_data_on_gsheet():
    age_data = []
    for group, label in age_groups.items():
        count = len(x_df.loc[x_df[3].astype(str) == group])
        age_data.append([label, count])
    g_ws = g_wb.worksheet(gsheet_tabs[4])
    g_ws.update("A2:B", age_data)
    print('Age sheet updated.')


def get_unique_by_col(data, col):
    values = []
    for row in data:
        if row[col] not in values:
            values.append(row[col])
    return values


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield end_date - timedelta(n)


def main():
    update_main_data_on_gsheet()
    update_metadata_on_gsheet()
    update_daily_data_on_gsheet()
    update_age_data_on_gsheet()


if __name__ == "__main__":
    main()
