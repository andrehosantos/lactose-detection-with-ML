from utils import FileHandler as file_handler
from libraries.pd.pdtools import Dataframe as dfs
import pandas as pd


def main():
    dir = './raw_data'
    files_list = file_handler.get_files(dir)
    dataframes = dfs(files_list)
    dataframes.create_dataframes(drop_columns=[0, 5])
    dataframes.concatenate_dataframes(concat_all=True)
    # sorted_df = 
    biggest = dataframes.get_biggest_dataframe(concatenated=True)
    for units, df in biggest.items():
        print(df.shape)
        print(df.groupby("Frequency (Hz)").agg(['mean', 'std', 'skew']).head())
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