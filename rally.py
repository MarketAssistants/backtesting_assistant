import numpy as np
from backtesting_utils import payloadize



def averaging_over (list, over_nbr_days): 

    list_avg = []

    for i in range(0,over_nbr_days-1): 
        list_avg.append(0)

    for i in range(over_nbr_days-1,len(list)): 
        count =0 
        counter = 0 
        j = i
        while(counter <3 and j>=0): 
            if list[j] != -10:
                count += list[j]
                counter +=1

            j -=1

        list_avg.append(round(count/over_nbr_days,2))


    return list_avg

def rally_backtest(self): 
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

    for day in range(self.first_day,self.nbr_days): 
        #define daily data
        open_price = self.open_data[day]
        high_price = self.high_data[day]
        close_price = self.close_data[day]
        low_price = self.low_data[day]

        #check for backup

        #stock participation: get iceberg_buy * volume, get iceberg_sell * volume and look at trends

        #stock morning rush: check close to next day open to see trends 

        #check general market morning rush: as above but for SPY
 
        rsi = self.rsi_data[day]


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
            year_after = round((day+self.first_day)/252,2) # Approximation for business days in a year
            # print("year_after: ",year_after)
            holding_timeout = 5
            buying_time= round(year_after * 4) / 4
            nbr_buys+=1
            if show_trades:
                print(f"====BUY {self.ticker}: buying on {self.date_secretary.get_date(day)} at the price of:",buying_price,"\n")
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
                    print(f"====WIN {self.ticker}: selling on {date} for planned profit target of {profit_target}%.")
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
    return self.nbr_days-1,nbr_buys,nbr_successes,total_win_prc,total_loss_prc,profit_tracker,np.array(success_buys_times),np.array(failed_buys_times)



def rally_graph(self):


    #get days stored
    dates = []
    for day in range(self.first_day+1,self.nbr_days):
        dates.append(self.date_secretary.get_date(day))

    # get/graph high prices with 50,200 MA averages    
    fifty_mas = []
    twohundred_mas = []
    for day in range(self.first_day+1,self.nbr_days):

        if (day-self.first_day +1) < 50: 
            fifty_mas.append(0)
        else: 
            fifty_mas.append(self.strategies_guy.MA_instant(self.data_close[day-50:day]))

        if (day-self.first_day +1) < 200: 
            twohundred_mas.append(0)
        else: 
            twohundred_mas.append(self.strategies_guy.MA_instant(self.data_close[day-200:day]))

    # get/graph broken depth, broken rank, relative strength
    # get/graph backup support, its rank, relative strength
            
    # broken_depth = [] 
    # broken_rank = []
    # relative_stength_broken = [] 
    # backup_support = []
    # backup_rank = []
    # relative_strength_backup = []
    # self.strategies_guy.change_reports(["NothingJustToGetDataStored"])
    # payload = payloadize(self.ticker,self.first_day,self.data_open,self.data_close,self.data_high,self.data_low,self.data_volume)
    # self.strategies_guy.run_reports(payload)

    # self.strategies_guy.change_reports(["support_levels"])
    
    # for day in range(self.first_day+1,self.nbr_days):
    #     if (day - self.first_day+ 1) < 300: 
    #         continue

    #     max_wdw, max_wdw_meta = self.support_guy.get_levels("support")

    #     self.get_relative_strength
    # # get/graph buy sell participation: iceberg buy * volume, iceberg sell*volume
    # stock and spy
    buy_participation_stock = []
    sell_participation_stock = []
    buy_iceberg_stock = []
    sell_iceberg_stock = []
    buy_participation_spy = []
    sell_participation_spy = []
    buy_iceberg_spy  = []
    sell_iceberg_spy  = []
    for date in dates:
        day = self.date_secretary.get_date_index(date)
        if day == -1:
            print("************ no way index was not found for date for stock") 
            exit(0)
        prices_stock = [self.data_close[day-1],self.data_open[day],self.data_low[day],self.data_close[day],self.data_high[day]]
        if any(np.isnan(price) for price in prices_stock): 
            buy_participation_stock.append(-10)
            sell_participation_stock.append(-10)

            buy_iceberg_stock.append(-10)
            sell_iceberg_stock.append(-10)
        else:    
            power_buy,power_sell = self.strategies_guy.get_daily_power(prices_stock,"same")
            buy_participation_stock.append(power_buy/100*self.data_vol[day])
            sell_participation_stock.append(power_sell/100*self.data_vol[day])
            buy_iceberg_stock.append(power_buy)
            sell_iceberg_stock.append(power_sell)

        day = self.date_secretary.get_date_index_ind(date)
        if day == -1:
            print(f"************ date {date} was not found in indices") 
            buy_participation_spy.append(-10)
            sell_participation_spy.append(-10)
            continue

        prices_spy = [self.spy_close[day-1],self.spy_open[day],self.spy_low[day],self.spy_close[day],self.spy_high[day]]
        if any(np.isnan(price) for price in prices_spy): 
            buy_participation_spy.append(-10)
            sell_participation_spy.append(-10)

            buy_iceberg_spy.append(-10)
            sell_iceberg_spy.append(-10)
        else:    
            power_buy_spy,power_sell_spy = self.strategies_guy.get_daily_power(prices_spy,"same")
            buy_participation_spy.append(power_buy_spy/100*self.spy_vol[day])
            sell_participation_spy.append(power_sell_spy/100*self.spy_vol[day])


            buy_iceberg_spy.append(power_buy_spy)
            sell_iceberg_spy.append(power_sell_spy)
            # if date == '2023-10-27': 
                # print(prices_spy)
                # print("power_buy is: ", power_buy_spy)
                # print("sell power is: ", power_sell_spy)
                # exit(0)

    # get/graph morning buy rush ie overnight prc change \

    morning_rush_stock = []
    morning_rush_spy = []

    #this one is to store daily percent changes
    daily_prcchg_stock = []
    daily_prcchg_spy = []

    for idx,date in enumerate(dates):

        day = self.date_secretary.get_date_index(date)
        if day == -1:
            print("************ no way index was not found for date for stock") 
            exit(0)
        #STOCK
        morning_rush_stock.append(round(100*(self.data_open[day]-self.data_close[day-1])/self.data_close[day-1],2))
        daily_prcchg_stock.append(round(100*(self.data_close[day]-self.data_open[day])/self.data_open[day],2))

        #SPY
        day = self.date_secretary.get_date_index_ind(date)
        prev_date = self.date_secretary.get_date_ind(day-1)
        if day == -1:
            print(f"************ date {date} was not found in indices") 
            buy_participation_spy.append(-10)
            sell_participation_spy.append(-10)
            morning_rush_spy.append(0)
            daily_prcchg_spy.append(-20)
            continue

        if any(np.isnan(price) for price in [self.spy_open[day],self.spy_close[day]]): 
            daily_prcchg_spy.append(-20)
        else: 
            daily_prcchg_spy.append(round(100*(self.spy_close[day]-self.spy_open[day])/self.spy_open[day],2))

        #this is for percent change
        if idx > 0 and prev_date != dates[idx-1] :
            print(f"************ previous spy date {prev_date} does not match previous stock date { dates[idx-1]}") 
            buy_participation_spy.append(-10)
            sell_participation_spy.append(-10)
            morning_rush_spy.append(0)
            continue

        if any(np.isnan(price) for price in [self.spy_open[day],self.spy_close[day-1]]): 
            morning_rush_spy.append(0)
        else: 
            morning_rush_spy.append(round(100*(self.spy_open[day]-self.spy_close[day-1])/self.spy_close[day-1],2))

    ## defying or with spy in terms of percent changes:  -2 is spy + and stock -, -1 is spy nagative and stock negative, 1 is spy positive and stock positive, +2 is spy neg and stock pos
    stocks_defying_spy = []
    for date in dates:
        day = self.date_secretary.get_date_index(date)
        if day == -1:
            print("************ no way index was not found for date for stock") 
            exit(0)
        stock_day_prcchg = 100*(self.data_close[day]-self.data_open[day])/self.data_open[day]

        day = self.date_secretary.get_date_index_ind(date)
        if day == -1:
            print(f"************ date {date} was not found in indices") 
            stocks_defying_spy.append(0)
            continue

        spy_day_prcchg   = 100*(self.spy_close[day]-self.spy_open[day])/self.spy_open[day]

        if spy_day_prcchg > 0 and stock_day_prcchg < 0: 
            stocks_defying_spy.append(-2)
        elif spy_day_prcchg < 0 and stock_day_prcchg < 0: 
            stocks_defying_spy.append(-1)
        elif spy_day_prcchg > 0 and stock_day_prcchg > 0: 
            stocks_defying_spy.append(1)
        elif spy_day_prcchg < 0 and stock_day_prcchg > 0: 
            stocks_defying_spy.append(2)
        else: 
            stocks_defying_spy.append(0)


    #averaging

    buy_iceberg_stock_avg = averaging_over(buy_iceberg_stock, 3)
    sell_iceberg_stock_avg = averaging_over(sell_iceberg_stock, 3)
    buy_iceberg_spy_avg  = averaging_over(buy_iceberg_spy, 3)
    sell_iceberg_spy_avg  = averaging_over(sell_iceberg_spy, 3)


    #iceberg_formula = (1+morning_rushpercenetchage/10)*buy_iceberg*(1+daily_percentchange/10)

    iceberg_formula_stock = [] 
    iceberg_formula_spy = []
    for i in range(len(morning_rush_stock)):
         formula = (1+morning_rush_stock[i]/10)*buy_iceberg_stock[i]*(1+daily_prcchg_stock[i]/10)
         iceberg_formula_stock.append(formula)

         formula = (1+morning_rush_spy[i]/10)*buy_iceberg_spy[i]*(1+daily_prcchg_spy[i]/10)
         iceberg_formula_spy.append(formula)


    avg_diff_iceberg_stock = [x - y for x, y in zip(buy_iceberg_stock_avg, sell_iceberg_stock_avg)]
    avg_diff_iceberg_spy = [x - y for x, y in zip(buy_iceberg_spy_avg, sell_iceberg_spy_avg)]

    st = dates.index('2022-04-11')
    en = dates.index('2022-11-15')
    
    # self.graphing_guy.plot_xy_same([dates[st:en],dates[st:en],dates[st:en],dates[st:en]],
    #                                          [buy_iceberg_stock_avg[st:en],buy_iceberg_spy_avg[st:en],avg_diff_iceberg_stock[st:en],avg_diff_iceberg_spy[st:en]],
    #                                          [" "," "," "," "],
    #                                          [" "," "," "," "],
    #                                          ["3day AVG stock buy iceberg","3day AVG stock buy iceberg","3day avg buy iceberg diff stock","3day avg buy iceberg diff spy"]
    #                                          )


    # self.graphing_guy.plot_xy_seperate([dates[st:en],dates[st:en],dates[st:en],dates[st:en]],
    #                                          [buy_participation_stock[st:en],sell_participation_stock[st:en], buy_participation_spy[st:en], 
    #                                           sell_participation_spy[st:en]],
    #                                          ["stock buy participation","stock sell participation", "spy buy participation", "spy sell participation"],
    #                                          [" "," "," "," "],
     
    #                                         [" "," "," "," "])


    # print(len(dates[st:en]))
    # print(len(stocks_defying_spy[st:en]))
    # print(len(morning_rush_spy[st:en]))
    # print(len(morning_rush_stock[st:en]))

    self.graphing_guy.plot_xy_seperate([dates[st:en],dates[st:en],dates[st:en]],
                                             [iceberg_formula_stock[st:en],iceberg_formula_spy[st:en],stocks_defying_spy[st:en] ],
                                             [ "icebergformulastock","icebergformulaspy","stocks_defying_spy"],
                                             [" "," "," "],
                                             [" "," "," "])
            
