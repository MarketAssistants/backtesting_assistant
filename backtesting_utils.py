def payloadize(ticker,first_day,data_open,data_close,data_high,data_low,data_volume):

    payload = {
    "ticker":ticker, 
    "first_day": first_day,
    "data_open": data_open,
    "data_close": data_close, 
    "data_high": data_high, 
    "data_low": data_low, 
    "data_volume": data_volume
    }
    return payload 