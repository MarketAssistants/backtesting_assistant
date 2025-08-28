import numpy as np

def get_daily_prc_chg(self,st,en,mode):
    
    lenn =en-st +1
    daily_prcchg_stock = np.full(lenn,-999,dtype=float)

    first_idx = max(self.first_day,st) - st
    for day in range(max(self.first_day,st),en+1):
        if mode == "highhigh":
            if any(np.isnan(price) for price in [self.data_high[day],self.data_high[day-1]]):
                first_idx +=1
                continue
            daily_prcchg_stock[first_idx] = (round(100*(self.data_high[day]-self.data_high[day-1])/self.data_high[day-1],2))
        
        if mode == "lowlow":
            if any(np.isnan(price) for price in [self.data_low[day],self.data_low[day-1]]):
                first_idx +=1
                continue
            daily_prcchg_stock[first_idx] = (round(100*(self.data_low[day]-self.data_low[day-1])/self.data_low[day-1],2))

        if mode == "closeopen":
            if any(np.isnan(price) for price in [self.data_high[day],self.data_high[day-1]]):
                first_idx +=1
                continue
            daily_prcchg_stock[first_idx] = (round(100*(self.data_open[day]-self.data_close[day-1])/self.data_close[day-1],2))
        
        first_idx +=1
    # print(daily_prcchg_stock)
    return daily_prcchg_stock




def get_daily_10dayMA_volume_prcchg(self,st,en):
    st = st -1 # delay by one day since this is prc chg
    lenn =en-st
    arr = np.full(lenn,-999,dtype=float)

    first_idx = max(self.first_day,st) - st
    for day in range(max(self.first_day,st)+1,en+1):
        ten_prev_vols = [self.data_vol[day-i] for i in range(10)]
        if any(np.isnan(vol) for vol in ten_prev_vols):
            first_idx +=1
            continue
        arr[first_idx] = np.mean(ten_prev_vols)
        first_idx +=1
    # print(arr)
    #get percent changes now: 
    arr_prcchg = np.full(lenn-1,-999,dtype=float)
    for idx in range(1,len(arr)):
        if arr[idx] == -999 or arr[idx-1] == -999 or arr[idx-1] == 0 or arr[idx] ==0: 
            continue
        
        arr_prcchg[idx-1] = round(100*(arr[idx]-arr[idx-1])/arr[idx-1],2)

    # print(arr_prcchg)
    # print(daily_prcchg_stock)
    return arr_prcchg


def get_daily_iceberg_powers(self,st,en,mode): 
    lenn =en-st+1
    daily_prcchg_stock = np.full(lenn,-999,dtype=float)

    first_idx = max(self.first_day,st) - st
    for day in range(max(self.first_day,st),en+1):
        prices_stock = [self.data_open[day],self.data_low[day],self.data_close[day],self.data_high[day]]
        if any(np.isnan(price) for price in prices_stock): 
            continue
        
        power_posarea,power_negarea,power_prc = self.strategies_guy.get_daily_powers_prcchg(prices_stock)

        if mode == "posarea":
            daily_prcchg_stock[first_idx] = power_posarea

        if mode == "negarea":
            daily_prcchg_stock[first_idx] = power_negarea
        
        if mode == "prcposarea":
            daily_prcchg_stock[first_idx] = power_prc
        
        first_idx +=1
    # print(daily_prcchg_stock)
    return daily_prcchg_stock


def get_spx_major_mas_relative_location(self,st,en): 

    results = {}


    for day in range(st,en+1):
        goback = self.nbr_days_ind -1 - day
        res = self.strategies_guy.get_major_mas_relative_loc("spy-close","spy-close",goback=goback)
        date = self.date_secretary.get_date_ind(day)

        results[date] = res
    return results