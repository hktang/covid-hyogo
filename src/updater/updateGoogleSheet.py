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

placeholder_lat_ln = [36.204823, 138.25293]

current_cities = {
    'たつの市': [34.831408, 134.549424],
    '三木市': [34.796896, 134.990194],
    '三田市': [34.89, 135.225507],
    '中播磨健康福祉事務所管内': [34.822511, 134.693029],
    '丹波健康福祉事務所管内': [35.177132, 135.035842],
    '丹波市': [35.177132, 135.035842],
    '京都市': [35.011564, 135.768149],
    '伊丹健康福祉事務所管内': [34.784348, 135.40091],
    '伊丹健康福祉事務所管外': placeholder_lat_ln,
    '伊丹市': [34.784348, 135.40091],
    '加古川健康事務所管内': [34.756919, 134.84136],
    '加古川健康福祉事務所管内': [34.756919, 134.84136],
    '加古川市': [34.756919, 134.84136],
    '加東健康福祉事務所管内': [34.9185915, 134.9734436],
    '加東市': [34.9185915, 134.9734436],
    '加西市': [34.9280226, 134.841609],
    '千葉県': [35.335416, 140.183252],
    '千葉県船橋市': [35.694549, 139.982728],
    '南あわじ市': [34.29449, 134.779782],
    '吹田市': [34.759359, 135.516477],
    '堺市': [34.573326, 135.483118],
    '多可町': [35.050216, 134.923425],
    '大阪市': [34.6413315, 135.5629394],
    '大阪府': [34.6413315, 135.5629394],
    '姫路市': [34.815418, 134.685551],
    '宍粟市': [35.004241, 134.549379],
    '宝塚健康福祉事務所管内': [34.799984, 135.360259],
    '宝塚市': [34.799984, 135.360259],
    '寝屋川市': [34.76625, 135.628018],
    '小野市': [34.853198, 134.93151],
    '尼崎市': [34.732711, 135.405791],
    '川西市': [34.830199, 135.417395],
    '播磨町': [34.7152468, 134.8680023],
    '新温泉町': [35.623691, 134.44893],
    '明石': [34.643208, 134.997586],
    '明石市': [34.643208, 134.997586],
    '明石市外': placeholder_lat_ln,
    '朝来健康福祉事務所管内': [35.339783, 134.852348],
    '朝来市': [35.339783, 134.852348],
    '東京都': [35.689487, 139.691711],
    '池田市': [34.821557, 135.42838],
    '洲本健康福祉事務所管内': [34.340382, 134.889557],
    '淡路市': [34.4396558, 134.9149109],
    '猪名川町': [34.8950618, 135.3761626],
    '県内': [34.683336, 135.163486],
    '県外': placeholder_lat_ln,
    "県外\n（大阪府内）": placeholder_lat_ln,
    '神戸市': [34.690081, 135.195631],
    '神戸市外': placeholder_lat_ln,
    '福崎町': [34.950238, 134.760182],
    '稲美町': [34.75, 134.916667],
    '管外': placeholder_lat_ln,
    '芦屋健康福祉事務所管内': [34.726954, 135.304127],
    '芦屋市': [34.726954, 135.304127],
    '西宮市': [34.737603, 135.341511],
    '西宮市外': placeholder_lat_ln,
    '西脇市': [34.993388, 134.969355],
    '調査中': placeholder_lat_ln,
    '豊中市': [34.781108, 135.469953],
    '豊岡健康福祉事務所管内': [35.544556, 134.820241],
    '赤穂健康福祉事務所管内': [34.755069, 134.390227],
    '赤穂市': [34.755069, 134.390227],
    '長崎県': [33.248853, 129.693091],
    '青森県': [40.765708, 140.917588],
    '非公表': placeholder_lat_ln,
    '香川県': [34.222592, 134.019915],
    '高砂市': [34.7661005, 134.7906014],
    '龍野健康福祉事務所管内': [34.831408, 134.549424],
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


def update_cities_data_on_gsheet():
    city_data = []
    cities = get_unique_by_col(x_case_data, 6)

    for city in cities:
        count = len(x_df.loc[x_df[6] == city])

        if city == '':
            continue

        if city not in current_cities:
            lat_ln = placeholder_lat_ln
            print('Notice:', city, 'is not in the list.')
        else:
            lat_ln = current_cities[city]

        city_data.append([lat_ln[0], lat_ln[1], city, count])

    merged_data = merge_city_data(city_data)

    g_ws = g_wb.worksheet(gsheet_tabs[3])

    g_ws.clear()

    g_ws.update("A1:D1", [['Lat', 'Lng', 'City', 'Total confirmed cases']])
    g_ws.update("A2:D", merged_data)

    print("City sheet updated.")


def get_unique_by_col(data, col):
    values = []
    for row in data:
        if row[col] not in values:
            values.append(row[col])
    return values


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield end_date - timedelta(n)


def merge_city_data(city_data):
    city_data.sort(key=lambda x: x[0])

    lats = []
    merged_data = []

    for row in city_data:
        lat = row[0]
        id = next((i for i, x in enumerate(
            merged_data) if lat in x), None)

        if id == None:
            lats.append(lat)
            merged_data.append(row)
        else:
            existing_row = merged_data[id]
            existing_row[2] = existing_row[2].replace("\n", '') + ', ' + row[2]
            existing_row[3] = existing_row[3] + row[3]

    return merged_data


def main():
    update_main_data_on_gsheet()
    update_metadata_on_gsheet()
    update_daily_data_on_gsheet()
    update_age_data_on_gsheet()
    update_cities_data_on_gsheet()


if __name__ == "__main__":
    main()
