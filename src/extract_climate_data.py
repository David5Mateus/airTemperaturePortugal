import cdsapi
from time import sleep

client = cdsapi.Client()

DATA_FOLDER_PATH = '../data/'
yi = 1992
yf = 2022

for year in range(yi, yf+1):
    outcdf = f"{DATA_FOLDER_PATH}/ERA5_t2m_WIb_{year}.nc"

    print('\n\n=================================')
    print(f"Saving {year} data to {outcdf}...\n")

    client.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': '2m_temperature',
            'year': str(year),
            'month': [
              '01', '02', '03',
              '04', '05', '06',
              '07', '08', '09',
              '10', '11', '12',
            ],
            'day': [
              '01', '02', '03',
              '04', '05', '06',
              '07', '08', '09',
              '10', '11', '12',
              '13', '14', '15',
              '16', '17', '18',
              '19', '20', '21',
              '22', '23', '24',
              '25', '26', '27',
              '28', '29', '30',
              '31',
            ],
            'time': [
              '00:00', '01:00', '02:00',
              '03:00', '04:00', '05:00',
              '06:00', '07:00', '08:00',
              '09:00', '10:00', '11:00',
              '12:00', '13:00', '14:00',
              '15:00', '16:00', '17:00',
              '18:00', '19:00', '20:00',
              '21:00', '22:00', '23:00',
            ],
            'area': [
              43, -10, 36,
              -6,
            ],
            'format': 'netcdf',
          },
        outcdf)
    sleep(3)
