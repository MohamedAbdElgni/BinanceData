"""This module extracts information from your `.env` file so that
you can use your Binance API key in other parts of the application.
"""


import os
import datetime


# pydantic used for data validation

from pydantic import BaseSettings


def return_full_path(filename: str = ".env") -> str:
    """Uses os to return the correct path of the `.env` file."""
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    full_path = os.path.join(directory_name, filename)
    return full_path


class Settings(BaseSettings):
    """Uses pydantic to define settings."""

    api_key: str
    api_sec: str
    model_directory: str
    data_directory: str

    class Config:
        env_file = return_full_path(".env")

    def get_filename_csv(self, df, symbol, invertal) -> str:
        """generate unique filename for the csv file

        Args:
            df (pandas.dataframe): data frame to get the date from
            symbol (str): the ticker symbol

        Returns:
            str: file name with the directory data_directory
        """
        now = datetime.datetime.now()
        timestamp_str = str(int(now.timestamp()*1000)).replace('.', '_')[:-3]
        return f"{settings.data_directory}/{symbol}_{invertal}_{df.index[0].year}_{df.index[0].month}_{timestamp_str}.csv"


# Create instance of `Settings` class that will be imported

settings = Settings()
