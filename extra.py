    # #get days stored
    # dates = []
    # for day in range(self.first_day+1,self.nbr_days):
    #     dates.append(self.date_secretary.get_date(day))


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
    # buy_participation_stock = []
    # sell_participation_stock = []
    # buy_iceberg_stock = []
    # sell_iceberg_stock = []
    # buy_participation_spy = []
    # sell_participation_spy = []
    # buy_iceberg_spy  = []
    # sell_iceberg_spy  = []
    # for date in dates:
    #     day = self.date_secretary.get_date_index(date)
    #     if day == -1:
    #         print("************ no way index was not found for date for stock") 
    #         exit(0)
    #     prices_stock = [self.data_close[day-1],self.data_open[day],self.data_low[day],self.data_close[day],self.data_high[day]]
    #     if any(np.isnan(price) for price in prices_stock): 
    #         buy_participation_stock.append(-10)
    #         sell_participation_stock.append(-10)

    #         buy_iceberg_stock.append(-10)
    #         sell_iceberg_stock.append(-10)
    #     else:    
    #         power_buy,power_sell = self.strategies_guy.get_daily_power(prices_stock,"same")
    #         buy_participation_stock.append(power_buy/100*self.data_vol[day])
    #         sell_participation_stock.append(power_sell/100*self.data_vol[day])
    #         buy_iceberg_stock.append(power_buy)
    #         sell_iceberg_stock.append(power_sell)

    #     prices_spy = [self.spy_close[day-1],self.spy_open[day],self.spy_low[day],self.spy_close[day],self.spy_high[day]]
    #     if any(np.isnan(price) for price in prices_spy): 
    #         buy_participation_spy.append(-10)
    #         sell_participation_spy.append(-10)

    #         buy_iceberg_spy.append(-10)
    #         sell_iceberg_spy.append(-10)
    #     else:    
    #         power_buy_spy,power_sell_spy = self.strategies_guy.get_daily_power(prices_spy,"same")
    #         buy_participation_spy.append(power_buy_spy/100*self.spy_vol[day])
    #         sell_participation_spy.append(power_sell_spy/100*self.spy_vol[day])


    #         buy_iceberg_spy.append(power_buy_spy)
    #         sell_iceberg_spy.append(power_sell_spy)
    #         # if date == '2023-10-27': 
    #             # print(prices_spy)
    #             # print("power_buy is: ", power_buy_spy)
    #             # print("sell power is: ", power_sell_spy)
    #             # exit(0)