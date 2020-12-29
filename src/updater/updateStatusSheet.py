from classes.excel import Excel
from classes.gsheet import Gsheet
import numpy

excel_params = {
    'url': 'https://web.pref.hyogo.lg.jp/kf16/documents/yousei.xlsx',
    'sheet_name': 'yousei ',
    'start_row': 2,
    'date_cols': ['A', 'B'],
    'time_format': "%Y-%m-%d",
}

gsheet_key = '1MJbDJzx8JHVbe9aH--FqkW34eDUczF9WnQvFq9szrzs'

x_wb = Excel(params=excel_params)
x_ws = x_wb.load_worksheet()
x_main_data = x_wb.get_main_data(x_ws)
x_main_data.reverse()

g_wb = Gsheet(gsheet_key).get_wb()


def update_main_data_on_gsheet():
    datarange = 'A2:L'
    gws = g_wb.worksheet('5.Status')
    diff_rows = x_ws.max_row - gws.row_count

    if diff_rows > 0:
        gws.insert_rows(numpy.zeros((diff_rows, 1)).tolist(), row=2)

    gws.update(datarange, x_main_data)
    print('Status data updated.')


def main():
    update_main_data_on_gsheet()


if __name__ == "__main__":
    main()
