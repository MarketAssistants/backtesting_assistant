from decimal import Decimal
import numpy as np
decimal_dtype = np.dtype(Decimal)

SPY_IDX = 1

class Backtesting_Assistant:     
    
    def __init__(self,reports,nbr_days, tickers_info,
                 date_secretary, strategies_guy,support_resistance_guy,graphing_guy,
                 ind_data_open, ind_data_close, ind_data_high, ind_data_low, ind_data_volume):
        # constant attributes
        self.enontiation = "=Backtesting=Assistant=: "
        self.nbr_days = nbr_days
        self.reports = reports
        self.tickers_info = tickers_info

        self.spy_open = np.array([tup[SPY_IDX] for tup in ind_data_open], dtype=decimal_dtype)
        self.spy_close = np.array([tup[SPY_IDX] for tup in ind_data_close], dtype=decimal_dtype)
        self.spy_high = np.array([tup[SPY_IDX] for tup in ind_data_high], dtype=decimal_dtype)
        self.spy_low = np.array([tup[SPY_IDX] for tup in ind_data_low], dtype=decimal_dtype)
        self.spy_vol = np.array([tup[SPY_IDX] for tup in ind_data_volume], dtype=decimal_dtype)

        self.date_secretary = date_secretary
        self.strategies_guy = strategies_guy
        self.support_resistance_guy = support_resistance_guy
        self.graphing_guy = graphing_guy

        self.nbr_days_ind = date_secretary.nbr_days_ind
        

    from rally import rally_backtest,rally_graph
    from getting_data import get_daily_prc_chg,get_daily_10dayMA_volume_prcchg,get_daily_iceberg_powers,get_spx_major_mas_relative_location

    def change_reports(self,new_reports): 
        self.reports = new_reports
         
    def run_reports(self,payload):

        list_reports = self.reports
        if not list_reports:
            print(self.enontiation + "No reports have been assigned to me ..Yaaay!")
            return {payload["ticker"]:{}}
        
        self.ticker = payload["ticker"]
        try:
            self.first_day = payload["first_day"]
            self.data_open = payload["data_open"]
            self.data_close = payload["data_close"]
            self.data_high = payload["data_high"]
            self.data_low = payload["data_low"]
            self.data_vol= payload["data_volume"]
        except: 
            print(self.enontiation +"some data is not given - Pass since maybe intentional.")
            pass 

        # print(f"strategies assistant: attaching {self.ticker} with last price{self.data_high[-1]}")
        # exit(0)
        reports = {}
        if self.first_day == -1: 
            return {self.ticker:reports}
        results = None
        for report in list_reports: 
            print(f"running {report} for ticker {self.ticker}")

            #this section for new way of passing report list: name,paramet1,parameter2...as necessary
            if isinstance(report, list):
                if report[0] == "dailyprcchghighhigh": 
                    results = self.get_daily_prc_chg(report[1],report[2],"highhigh")

                if report[0] == "dailyprcchglowlow": 
                    results = self.get_daily_prc_chg(report[1],report[2],"lowlow")

                if report[0] == "icebergposarea": 
                    results = self.get_daily_iceberg_powers(report[1],report[2],"posarea")

                if report[0] == "icebergnegarea": 
                    results = self.get_daily_iceberg_powers(report[1],report[2],"negarea")

                if report[0] == "icebergprcposarea": 
                    results = self.get_daily_iceberg_powers(report[1],report[2],"prcposarea")

                if report[0] == "volmaprcchg": 
                    results = self.get_daily_10dayMA_volume_prcchg(report[1],report[2])

                if report[0] == "dailyprcchgcloseopen": 
                    results = self.get_daily_prc_chg(report[1],report[2],"closeopen")

                # if report[0] == "spxmaslocation":
                #     results = self.get_spx_major_mas_relative_location(report[1],report[2])

                reports[report[0]] = results
                        #this section for new way of passing report list: name,paramet1,parameter2...as necessary
            # if isinstance(report, list):
            #     if report[0] == "RSI14":
            #         results = self.get_rsi_data(start_date=report[1], end_date=report[2])

            #     reports[report[0]] = results

            #this section is for legacy way of doing things - passing report as string
            if isinstance(report, str):
                if report == "rally_backtest":
                    results = self.rally_backtest()   

                if report == "rally_graph":
                    results = self.rally_graph()   

                
                reports[report] = results

        return {self.ticker:reports}
         
