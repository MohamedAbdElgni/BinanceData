from binance.client import Client
import pandas as pd
from config import settings


class Binance_data:
    def __init__(self):
        # init binance client
        self.__client = Client(settings.api_key, settings.api_sec)

    def get_data(self, symbol, start_date, end_date, invertal):
        """ Get data from binance api

        Args:
            symbol (str): Sympol vs USDT or any other supported currency
            start_date (str): y-m-d
            end_date (str): y-m-d
            invertal (str): 1M-1H-1D-1W-1M

        return: pandas dataframe with given start and end date and the given invertal
        """

        symbol = symbol.upper()
        start_date = str(int((pd.Timestamp(start_date).timestamp())*1000))
        end_date = str(int((pd.Timestamp(end_date).timestamp())*1000))
        try:
            k_lines = self.__client.get_historical_klines(
                symbol, invertal, start_date, end_date)

            df = pd.DataFrame(k_lines, columns=['timestamp', 'open', 'high', 'low', 'close',
                                                'volume', 'close_time', 'quote_asset_volume',
                                                'number_of_trades', 'taker_buy_base_asset_volume',
                                                'taker_buy_quote_asset_volume', 'ignore'])
            # convert timestamp to date time
            df['timestamp'] = pd.to_datetime(
                df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df.sort_index(ascending=True, inplace=True)
            # convert to float
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            # 10 Dicemal places for close price
            df['close'] = df['close'].astype(float).round(10)
            df['volume'] = df['volume'].astype(float)
            df['quote_asset_volume'] = df['quote_asset_volume'].astype(float)
            df['taker_buy_base_asset_volume'] = df['taker_buy_base_asset_volume'].astype(
                float)
            df['taker_buy_quote_asset_volume'] = df['taker_buy_quote_asset_volume'].astype(
                float)
            df['ignore'] = df['ignore'].astype(float)

            # adding the freq to df index
            new_index = pd.date_range(start=df.index.min(
            ), end=df.index.max(), freq=invertal[-1].upper())

            df = df.reindex(new_index)
            df.index.name = 'timestamp'
            df.sort_index(ascending=True, inplace=True)

            print(
                f"Data Downloaded successfully !!!!!!\nData frame with {len(df)} observations For {symbol} from date {str(df.index.min().date())} to {str(df.index.max().date())} with {invertal} invertal From Binance...")
            # save data to class
            self.__df = df
            self.__invertal = invertal[-1]
            self.__symbol = symbol

            return df

        except Exception as e:
            print(
                f"An error occurred while fetching data from Binance. Please check the provided symbol, date range, and interval.\n{e}")

    def wrangle_data(self, get_time_series=True, columns=['close']):
        """ Wrangle data for model
        Args:
            get_time_series (bool): if True return time series data False by default
            columns (list,str): list of columns to return if get_time_series is False or one columns if get_time_series is False
        Return:
            pandas dataframe with close column or the given columns    
        """
        if get_time_series:
            # get time series data
            model_data = self.__df['close']

            self.__model_data = model_data
            return model_data
        else:
            model_data = self.__df[columns]

            self.__model_data = model_data
            return model_data

    def save_data(self):
        """
        Save data to csv in the data folder using get_filename_csv method from config.py
        """
        # save data to csv
        self.__model_data.index.freq = self.__invertal
        self.__model_data.to_csv(settings.get_filename_csv(
            df=self.__model_data, symbol=self.__symbol, invertal=self.__invertal), date_format="%Y-%m-%d %H:%M:%S.%f ", header=True)
        print(
            f"Data saved successfully to {settings.get_filename_csv(df=self.__model_data, symbol=self.__symbol,invertal=self.__invertal),}")
        return self.__model_data
#wep developments in this branch
