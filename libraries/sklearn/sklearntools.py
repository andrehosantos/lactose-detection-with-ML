from utils import FileHandler as file_handler
from libraries.pd.pdtools import Dataframe as dfs
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, FunctionTransformer, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA, KernelPCA
import numpy as np
import pandas as pd

class Data:
    def __init__(self,
                 dataframe: pd.DataFrame,
                 train: float = 0.8,
                 test: float = 0.2,
                 val: float = 0,
                 target_name: str = ''):
        self.RANDOM_STATE = 42
        self.df = dataframe
        self.train_ratio = train
        self.test_ratio = test
        self.val_ratio = val
        self.target_name = target_name
        if isinstance(self.df, dict):
            self.features = self.df['features']
        else:
            self.features = self.df.columns[:-1]
        self.test_size = self.test_ratio + self.val_ratio
        self.test_val_df = []
        self.train_df = []
        self.test_df = []
        self.val_df = []
        self.train_transformed = []
        self.test_transformed = []
        self.val_transformed = []
        self.df_list = ('train', 'test', 'val')
        self.train_test_val_transformed = {}
        self.pca_transformed_train = []
        self.pca_transformed_test = []
        self.pca_transformed_val = []

    def split_data(self):
        self.train_df, self.test_val_df = train_test_split(self.df,
                                                           test_size=self.test_size,
                                                           stratify=self.df["Frequency (Hz)"],
                                                           random_state=self.RANDOM_STATE)
        if self.val_ratio:
            self.test_df, self.val_df = train_test_split(self.test_val_df,
                                                         test_size=1-self.val_ratio,
                                                         stratify=self.test_val_df["Frequency (Hz)"], 
                                                         random_state=self.RANDOM_STATE)
    @staticmethod
    def split_np_data(np_arrays,
                      test: float = 0.2,
                      val: float = 0,
                      random_state: int = 42):
        test_size = test + val
        train_df, test_val_df = train_test_split(np_arrays,
                                                 test_size=test_size,
                                                 random_state=random_state)
        if val:
            test_df, val_df = train_test_split(test_val_df,
                                               test_size=1-val,
                                               random_state=random_state)
            return test_df, train_df, val_df
        return train_df, test_val_df

    def transform_data(self):
        power_transformer = preprocessing.PowerTransformer(method='yeo-johnson')
        log_transformer = FunctionTransformer(np.log1p, validate=True)
        target = [self.target_name]
        self.train_transformed = self.train_df.copy()
        column_transformer = ColumnTransformer(
            transformers=[
                ('num', power_transformer, self.features),
                ('target', log_transformer, target)],
            remainder='passthrough'
            )
        self.train_transformed = column_transformer.fit_transform(self.train_df)
        self.train_transformed = pd.DataFrame(self.train_transformed, columns=self.train_df.columns)
        self.test_transformed = column_transformer.fit_transform(self.test_df)
        self.test_transformed = pd.DataFrame(self.test_transformed, columns=self.test_df.columns)
        self.val_transformed = column_transformer.fit_transform(self.val_df)
        self.val_transformed = pd.DataFrame(self.val_transformed, columns=self.val_df.columns)
        
        for df_name in self.df_list:
            attr = f"{df_name}_transformed"
            self.train_test_val_transformed[df_name] = getattr(self, attr)

    def run_pca(self):
        for method, df in self.train_test_val_transformed.items():
            print(method, df.head())
            df = df.drop(self.target_name, axis=1)
            pca = PCA().fit(df)
            labels = ["PC" + str(n + 1) for n in range(len(pca.components_))]
            pca_components = pd.DataFrame(columns=labels)
            for i, component in enumerate(pca.components_):
                pca_df = df.copy()
                pca_df = pca_df * component[i]
                pca_components[labels[i]] = pca_df.sum(axis=1)
            attr = f"pca_transformed_{method}"
            setattr(self, attr, pca_components)
