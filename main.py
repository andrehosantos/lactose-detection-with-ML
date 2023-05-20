from utils import FileHandler as file_handler
from libraries.pd.pdtools import Dataframe as df_handler
import pandas as pd


def main():
    dir = './raw_data'
    concat_dir = './concat'
    files_list = file_handler.get_files(dir)
    dataframes_list = df_handler(file_path=dir)
    dataframes = dataframes_list.create_dataframes(files_list, drop_indices=[0])
    concat_df = df_handler.concatenate_dataframes(dataframes)
    for units, concentrations in dataframes.items():
        print(units)
        for concentration, df in concentrations.items():
            print(concentration)
            print(df[0].shape)
    # for i in range(40,50):
    #     file_path = files[i][2]
    #     dataframe = df(file_path=file_path)
    #     result = dataframe.create_dataframe()
    #     dataframes.append(result)
    # concat = df.concatenate_dataframes(pd_dataframes=dataframes)
    # concat.to_csv('concat.csv', index=True)
    # concat["Frequency (Hz)"] = concat["Frequency (Hz)"].astype("category")
    # grouped = concat.groupby("Frequency (Hz)")
    # stats = grouped.describe()
    # print(stats)



    # print(concat.groupby("Frequency (Hz)")["-Phase (°)"].describe())
    # print(concat.tail())
    # print(concat["-Phase (°)"].groupby("Index"))


if __name__ == "__main__":
    main()