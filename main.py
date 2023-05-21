from utils import FileHandler as file_handler
from libraries.pd.pdtools import Dataframe as dfs
import pandas as pd


def main():
    dir = './raw_data'
    files_list = file_handler.get_files(dir)
    dataframes = dfs(files_list)
    dataframes.create_dataframes(drop_columns=[0])
    dataframes.concatenate_dataframes()
    # sorted_df = 
    biggest = dfs.get_biggest_dataframe(concat_df)
    for units, concentrations in dataframes.items():
        print(units)
        for concentration, df in concentrations.items():
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