
# import numpy as np

# def get_rsi_data(self,start_date,end_date): 
#     st = self.date_secretary.get_date_index(start_date)
#     en = self.date_secretary.get_date_index(end_date)


#     lenn =en-st
#     daily_prcchg_stock = np.full(lenn,-999,dtype=float)


#         try:
#             rsi_data = strategies_results[idx][ticker]["RSI14"]
#         except: 
#             print(f"{ticker}*error getting data**continuing")
#             continue
#     first_idx = max(self.first_day,st) - st
#     for day in range(max(self.first_day,st)+1,en+1):

#         if any(np.isnan(price) for price in [self.data_high[day],self.data_high[day-1]]):
#             continue
#         daily_prcchg_stock[first_idx] = (round(100*(self.data_high[day]-self.data_high[day-1])/self.data_high[day-1],2))
#         first_idx +=1
#     # print(daily_prcchg_stock)
#     return daily_prcchg_stock

#     return 






def backtest_rsi(self,ticker,show_trades,rsi_data,open_data,low_data,close_data,rsi_threshehold,high_data,nbr_days, first_day): 
    #could be passed or not
    conditions_confirm = []
    conditions_sell    = []
    conditions_buy     = []

    total_win_prc = 0
    total_loss_prc = 0
    bought = False
    buying = False
    confirming = False

    confirm_bool = False
    confirm_timeout = 0

    nbr_buys = 0
    nbr_successes = 0
    success_buys_times = []
    failed_buys_times = []

    profit_tracker = [[0,'2000']]

    for day in range(first_day,nbr_days): 
        #define daily data
        open_price = open_data[day]
        high_price = high_data[day]
        close_price = close_data[day]
        low_price = low_data[day]
        rsi = rsi_data[day]


        if confirming:  
            if confirm_timeout ==0: 
                confirming = False
                continue
            conditions_confirm = []

            if all(conditions_confirm): 
                buying = True
                confirming = False
                continue
            else: 
                confirm_timeout -=1

        if buying: 
            bought = True
            buying = False
            buying_price = open_price
            year_after = round((day+first_day)/252,2) # Approximation for business days in a year
            # print("year_after: ",year_after)
            holding_timeout = 5
            buying_time= round(year_after * 4) / 4
            nbr_buys+=1
            if show_trades:
                print(f"====BUY {ticker}: buying on {self.date_secretary.get_date(day)} at the price of:",buying_price,"\n")
        if bought: #check for profit
            
            if holding_timeout ==0 or round((low_price-buying_price)*100/buying_price,2) <= -5: 
                bought = False
                failed_buys_times.append(buying_time)
                loss_prc = -5
                date = self.date_secretary.get_date(day)
                if show_trades:
                    print(f"====LOSS {ticker}: selling on {date} for loss of {loss_prc}%.")
                total_loss_prc += loss_prc
                profit_tracker.append([profit_tracker[-1][0] + loss_prc,date])
                continue
            profit_target   = 1
            day_chg_high    = 100*(high_price - buying_price)/buying_price
            conditions_sell = [day_chg_high >=profit_target]

            if all(conditions_sell): 
                bought = False
                nbr_successes +=1
                success_buys_times.append(buying_time)
                date = self.date_secretary.get_date(day)
                if show_trades:
                    print(f"====WIN {ticker}: selling on {date} for planned profit target of {profit_target}%.")
                total_win_prc += profit_target
                profit_tracker.append([profit_tracker[-1][0] + profit_target,date])
                continue
            else: 
               holding_timeout -=1

        else: #chasing a buy

            conditions_buy = [ rsi <= rsi_threshehold*1.03]
            if all(conditions_buy): #trigger a buy
                # buying = True
                if confirm_bool:
                    confirming = True
                else:
                    buying = True
                
    # print("getting here")
    # print(np.array(success_buys_times))
    return nbr_days-1,nbr_buys,nbr_successes,total_win_prc,total_loss_prc,profit_tracker,np.array(success_buys_times),np.array(failed_buys_times)