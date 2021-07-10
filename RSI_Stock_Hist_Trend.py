#!/usr/bin/env python

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
from secrets import randbelow
import random
from datetime import datetime
import pyperclip as clp


class Hist_Stock_Trnd_RSI:
   
    def __init__(self):
        self.RSI_cal_Method = 'SMA'
        self.Period = 14 #days
        self.from_dt = '2010-01-01'
        self.to_dt = '2015-01-01'
        self.stock_list=[]
        self.rnd_list = list(range(0,10))
        self.stockNames = ["FB", "AAPL", "AMZN", "IBM", "GOOGL", "MSFT", "NAV", "O", "QCOM", "TSLA"]
        
    #setter properties..
    def set_RSI_Method(self, val):
        self.RSI_cal_Method = val
    
    def set_Period(self, val):
        self.Period = val
    
    def set_FromDT(self, val):
        self.from_dt = val

    def set_ToDT(self, val):
        self.to_dt = val
        
    def set_stock_list(self, val):
        self.stock_list.append(val)
    
    def del_stock_list(self):
        del self.stock_list[:]
    
    #getter properties..
    def get_RSI_Method(self):
        return self.RSI_cal_Method

    def get_Period(self):
        return self.Period
    
    def get_FromDT(self):
        return self.from_dt 
    
    def get_ToDT(self):
        return self.to_dt    

    def get_stock_list(self):
        return self.stock_list  
    
    def ask_user_list_conf(self):
        #global RSI_cal_Method
        check = str(input("Would like to continue (Y) or re-enter / shuffle the list (N)? Enter (Y/N): ")).lower().strip()
        try:
            if check[0] == 'y':           
                return True
            elif check[0] == 'n':
                return False
            else:
                print('Invalid Input')
                return self.ask_user_list_conf()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.ask_user_list_conf()

    def ask_user_RSI_calc(self):
        try:
            check = int(input("Pls select method for Relative Strength Index (RSI) Calculation : Either EWMA(1) or SMA(2) method ? enter (1/2): ")) #.lower().strip()
        #print(check)

            #print(check)
            if check == 1:
                return 'EWMA'
            elif check == 2:
                return 'SMA'
            else:
                print('Invalid Input')
                return self.ask_user_RSI_calc()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.ask_user_RSI_calc()

    def ask_user_MeanWindow(self):
        try:
            check = int(input("Please enter the Moving Window range between 1-50: "))
            if check > 0 and check < 51:
                return check
            else:
                print('Invalid Input')
                return self.ask_user_MeanWindow()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.ask_user_MeanWindow()  

    def ask_user_DateRange(self):

        clpstack=clp.paste()
        clp.copy("2010-01-10;2020-01-10")        
        check =input("Pls enter date Range[eg. 2010-01-10;2020-01-10]. Use semi-colon(;) to seperate FromDate;ToDate or enter ctrl+v to get the default dates :")
        clp.copy(clpstack)
        try:
            date_strt = datetime.fromisoformat(check.split(";")[0])
            date_end = datetime.fromisoformat(check.split(";")[1])
            #print('Date :' + str(check) + ':' + str(date_strt) + ';' + str(date_end))
            if(date_strt > datetime(2009, 12, 31) and date_end < datetime(2020, 2, 1)):
                print('Valid date inputs!')
                self.set_FromDT(date_strt)
                self.set_ToDT(date_end)
                return True
            else:
                print('Invalid Input')
                return self.ask_user_DateRange()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.ask_user_DateRange() 



    def LoadData(self):
    #for i in self.get_stock_list():
        try:
            df = yf.download(self.get_stock_list(), start=self.get_FromDT, end=self.get_ToDT, progress=False)
            df = df[['Close']]
            df.dropna()
        except Exception as error:
            pass
        return df

    
    def getInterested_Stock(self):

        del self.stock_list[:]
        #self.set_stock_list([])
        Stock_intersted = input("Pls key in number of stocks between 1 to 10 or stock name eg. FB : Available Stocks for this excercise : [FB, AAPL, AMZN, IBM, GOOGL, MSFT, NAV, O, QCOM,TSLA]")
        random.shuffle(self.rnd_list)

        if Stock_intersted.isnumeric():
            print('NUMERIC FLOW')
            Stock_intersted = int(Stock_intersted)
            if Stock_intersted > 0 and Stock_intersted < 11:
                print('The following stocks will be plotted :')
                i = 0

                while i < Stock_intersted:
                    self.set_stock_list(self.stockNames[self.rnd_list[i]])
                    i+=1
                print(self.get_stock_list())
                check = self.ask_user_list_conf()

                if (check):
                    #print("plot grapah")
                    self.set_RSI_Method(self.ask_user_RSI_calc())
                    self.set_Period(self.ask_user_MeanWindow())
                    dt = self.ask_user_DateRange()
                    df=[]#df = self.LoadData() 
                    return df
                else:
                    self.getInterested_Stock()
            else:
                print('Pls enter number between 1 - 10')
                self.getInterested_Stock()
                print('^^^^^^^')
        else:
            print('NON NUMERIC FLOW')
            #print('text ;' + str(Stock_intersted))
            for i in self.stockNames:
               # print( str(Stock_intersted.lower().strip()) +' =='+ str(i))
                if (i.lower().strip() == Stock_intersted.lower().strip()):
                    self.set_stock_list(i.upper().strip())
                    #print('matching '+ str(i))

            if(len(self.get_stock_list())>0):
                check = self.ask_user_list_conf()
            else:
                print('Stock that you keyed in  ''[' + str(Stock_intersted) +']'' is not matching from list given above:')
                check = False

            if (check):
                #print("plot grapah")
                self.set_RSI_Method(self.ask_user_RSI_calc())
                self.set_Period(self.ask_user_MeanWindow())
                dt = self.ask_user_DateRange()
                df=[]#df = self.LoadData() 
                return df
            else:
                self.getInterested_Stock()


    #try:
    #except Exception as error:
       # print("Please enter valid inputs")
       # print(error)
       # return self.getInterested_Stock()
        
