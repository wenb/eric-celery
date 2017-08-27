#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: wenbin
@filename: test
@created date: 2017/8/9
@last modified: 2017/8/9
"""
import numpy as np
import talib as ta
import DataAPI
ta.EMA
EQUITY_DAILY_FIELDS = ['preClosePrice', 'openPrice', 'closePrice', 'highestPrice', 'lowestPrice',
                       'turnoverVol', 'turnoverValue', 'accumAdjFactor']
endDate = "2017-08-01"


def get_tradeday(endDate,N,startDate="20150101"):
    try:
        df_all_day = DataAPI.TradeCalGet(exchangeCD="XSHE", beginDate=startDate,)
        if df_all_day.empty:
            raise Exception("DataAPI.TradeCalGet returns error!")
        df_open_day = df_all_day[df_all_day.isOpen == 1].reset_index()
        index_endDate = df_open_day[df_open_day.calendarDate == endDate].index[0]
        index_startDate = index_endDate - N
        return df_open_day.loc[index_startDate,"calendarDate"]
    except Exception, e:
        print e


def get_equ_data(secID,startDate,endDate,field=EQUITY_DAILY_FIELDS):
    df = DataAPI.MktEqudAdjGet(secID=secID,beginDate=startDate,
                               endDate=endDate,field=["secID","tradeDate"]+field,pandas="1")
    return df


class SignalGenerator(object):

    def __init__(self,df_price):
        self.df_price = df_price
        self.closePrice_array = self.df_price["closePrice"].as_matrix()

    def acd(self, N):
        self.df_price = self.df_price[-N:]
        self.df_price["buy"] = self.df_price["closePrice"] -\
                               self.df_price[["lowestPrice", "preClosePrice"]].min(axis=1)
        self.df_price["sell"] = self.df_price["closePrice"] -\
                                self.df_price[["highestPrice", "preClosePrice"]].max(axis=1)
        return np.sum(self.df_price["buy"]) + np.sum(self.df_price["sell"])

    def EMA(self, N):
        self.EMA_value = ta.EMA(self.closePrice_array,timeperiod=N)
        return self.EMA_value

    def MA(self, N):
        self.MA_value = ta.MA(self.closePrice_array,timeperiod=N)
        return self.MA_value

    def MA10Close(self):
        self.MA_value = ta.MA(self.closePrice_array,timeperiod=10)
        return np.divide(self.MA_value,self.closePrice_array)

    def APBMA(self, N=5):
        self.MA_value = ta.MA(self.closePrice_array, timeperiod=N)
        self.APBMA_value = ta.MA(np.abs(self.closePrice_array - self.MA_value), timeperiod=N)
        return self.APBMA_value

    def BBI(self):
        MA_values = [ta.MA(self.closePrice_array,timeperiod=3*i) for i in range(1,5,1)]
        self.BBI = np.nanmean(np.array([i for i in MA_values]),axis=0)
        return self.BBI

    def BBIC(self):
        MA_values = [ta.MA(self.closePrice_array,timeperiod=3*i) for i in range(1,5,1)]
        self.BBI = np.nanmean(np.array([i for i in MA_values]),axis=0)
        return np.divide(self.BBI, self.closePrice_array)

    def TEMA(self,N):
        self.TEMA_value = ta.TEMA(self.closePrice_array,timeperiod=N)
        return self.TEMA_value


n = 100
tradeDays = n*2
startDate = get_tradeday(endDate,tradeDays)
df = get_equ_data("000001.XSHE",startDate.replace("-",""),endDate.replace("-",""))

signal = SignalGenerator(df)
print signal.MA10Close()
