import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from cycler import cycler


coordinates_file_path = '../data/sites_coordinates.csv'
retrieved_dataset = '../data/ERA5_t2m_WIb_1992_2022.nc'

output_folder = "../outputs"
output_filename = "t_air_regions_1992_2022_mean_plot.pdf"
output_excel_filename = "t_air_mean_values.xlsx"
output_csv_filename = "t_air_merged_values.csv"
output_excel_filepath = f"{output_folder}/{output_excel_filename}"
output_pdf_filepath = f"{output_folder}/{output_filename}"


regions = ['North', 'Center', 'Southwest', 'South']
line_colors = ['blue', 'orange', 'green', 'red']

custom_cycler = cycler(color=line_colors)


def build_t_air_mean_plot():
    ds = xr.open_dataset(retrieved_dataset)
    # convert to celsius
    t_air = ds.t2m - 272.15
    # calculate yearly mean values
    t_air_yearly = t_air.resample(time='Y').mean()
    mean_t_air_data = []

    # load coordinates file dataset
    stns = pd.read_csv(coordinates_file_path, sep=';')

    # Matriz bidimensional para guardar os valores
    t_air2d = np.empty((len(stns), len(t_air_yearly))) * np.nan

    # Preenchimento da matriz
    for idx in range(0, len(stns)):
        stn_lo = stns.Longitude[idx]
        stn_la = stns.Latitude[idx]

        t_air2d[idx, :] = t_air_yearly.sel(longitude=stn_lo, latitude=stn_la, method='nearest')

    t_air_loc = xr.Dataset(
        data_vars=dict(
            t_air=(["loc", "time"], t_air2d),
            region=(["loc"], stns.Regiao.values),
            local=(["loc"], stns.Local.values),
            lat=(["loc"], stns.Latitude.values),
            lon=(["loc"], stns.Longitude.values),
        ),
        coords=dict(
            loc=(["loc"], stns.index.array),
            time=t_air_yearly.time,
        ),
        attrs=dict(description=""),
    )

    fig, ax = plt.subplots(figsize=(14, 8))

    # PLOT SETTINGS
    # Line colors
    ax.set_prop_cycle(custom_cycler)
    # Set X and Y labels
    ax.set_xlabel('')
    ax.set_ylabel('°C (mean ± S.E.)')
    # Format time on x-axis
    date_format = mdates.DateFormatter('%b %Y')  # Month and Year
    ax.xaxis.set_major_formatter(date_format)
    # Set the interval of time on the x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=36))

    for region, color in zip(regions, line_colors):
        t_air_data = t_air_loc.where(t_air_loc.region == region).t_air

        # Plot mean line with specified color
        t_air_mean = t_air_data.mean('loc')
        mean_t_air_data.append(t_air_mean.values)
        ax.plot(t_air_mean.time.values, t_air_mean.values, label=f'{region} (mean)', color=color)

        # Calculate standard error using numpy's std function and divide by sqrt(number of samples)
        t_air_se = t_air_data.std('loc', ddof=1) / np.sqrt(len(stns))

        # Plot standard error bars without points
        ax.errorbar(
            t_air_mean.time.values, t_air_mean.values, yerr=t_air_se, fmt='-', label='', capsize=5, elinewidth=1, ecolor='black')

    # Create a legend with only region names
    ax.legend(regions, title='Regions')

    return ds, fig, mean_t_air_data, t_air_yearly


def export_nc_to_csv(ds):
    df = ds.to_dataframe()
    df.to_csv(f"{output_folder}/{output_csv_filename}")


def export_t_air_mean_plot(fig):
    # Exports the plot to a PDF file
    # Save the figure to the specified PDF file
    fig.savefig(output_pdf_filepath, bbox_inches="tight", format="pdf")


def export_t_air_mean_csv(mean_t_air_data, t_air_yearly):
    # Convert to a DataFrame

    # Create a DataFrame for mean T air values
    df_t_air_mean = pd.DataFrame(mean_t_air_data, index=regions, columns=t_air_yearly.time.values)

    # Save the DataFrame to an Excel file
    df_t_air_mean.to_excel(output_excel_filepath, sheet_name='Mean_T_AIR')


if __name__ == '__main__':
    ds, fig, mean_t_air_data, t_air_yearly = build_t_air_mean_plot()
    # plt.show()
    export_nc_to_csv(ds)
    export_t_air_mean_plot(fig)
    export_t_air_mean_csv(mean_t_air_data, t_air_yearly)
