from typing import Any, Dict, List

import pandas as pd


def normalize_col(column_name):
    return column_name.strip().lower().replace(" ", "_")


class Environment:
    def __init__(self):
        self.source_df: pd.DataFrame = None
        self.training_df: pd.DataFrame = None

        self.target_col: str = None
        self.feature_cols: List[str] = []

        self.category_col: str = None

    def execute(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return getattr(self, action)(**parameters)

    def load_dataset_async(self, dataset_name: str):
        dataset_normed = normalize_col(dataset_name)
        self.source_df = pd.read_csv(f"data/{dataset_normed}.csv")
        self.source_df.columns = map(normalize_col, self.source_df.columns)
        return f"Dataset {dataset_normed} loaded."

    def list_columns(self):
        return f"Column list: {self.source_df.columns.tolist()}"

    def show_column(self, column_name):
        normed_column = normalize_col(column_name)
        return (
            f"Details for {normed_column}:\n"
            f"  min: {self.source_df[normed_column].min()},\n"
            f"  max: {self.source_df[normed_column].max()},\n"
            f"  count: {self.source_df[normed_column].count()}\n"
            f"First 5 values: \n"
            f"{self.source_df[normed_column].head(5)}"
        )

    def add_feature(self, column_name):
        normed_col = normalize_col(column_name)
        if normed_col in self.source_df.columns:
            self.feature_cols.append(normalize_col(column_name))
            return f"Column {normed_col} has been added as feature."
        else:
            self.exists__ = f"Column {normed_col} doesn't exists."
            return self.exists__

    def list_features(self):
        return f"Feature list: {self.feature_cols}"

    def drop_feature(self, column_name):
        normed_col = normalize_col(column_name)
        if normed_col in self.source_df.columns:
            self.feature_cols.remove(normalize_col(column_name))
            return f"Column {normed_col} has been dropped from features."
        else:
            return f"Column {normed_col} doesn't exist."

    def choose_category_column(self, column_name):
        normed_col = normalize_col(column_name)
        if normed_col in self.source_df.columns:
            self.category_col = normed_col
            if normed_col in self.feature_cols:
                self.feature_cols.remove(normed_col)
            return f"Column {normed_col} has been chosen as category column."
        return f"Column {normed_col} doesn't exists."

    def show_category_column(self):
        return f"Column {self.category_col} is used as category column."

    def normalize_column(self, column_name):
        normed_col = normalize_col(column_name)
        if normed_col in self.source_df.columns:
            # self.training_df[normed_col] = self.source_df[normed_col].normalize()
            return f"Column {normed_col} has been normalized."
        return f"Column {normed_col} doesn't exist."

    def fill_missing_values(self, column_name, mode):
        normed_col = normalize_col(column_name)
        if normed_col in self.source_df.columns:
            # self.training_df[normed_col] = self.source_df[normed_col].normalize()
            return f"Missing values in column {normed_col} has been filled with {mode}."
        return f"Column {normed_col} doesn't exist."

    def encode_categorical_column(self, column_name, encoder):
        normed_col = normalize_col(column_name)
        if normed_col in self.source_df.columns:
            # self.training_df[normed_col] = self.source_df[normed_col].normalize()
            return f"Column {normed_col} has been encoded with {encoder}."
        return f"Column {normed_col} doesn't exist."

    def get_column_correlation(self, column_name):
        if not column_name:
            return f'Correlation for the dataset:\n{self.source_df.corr()}'
        normed_col = normalize_col(column_name)
        if normed_col in self.source_df.columns:
            corr = self.source_df.corr()[normed_col].sort_values(axis=0, ascending=False).tail(-1)
            # self.training_df[normed_col] = self.source_df[normed_col].normalize()
            return f"Correlation for column {normed_col}:\n{corr}."
        return f"Column {normed_col} doesn't exist."
