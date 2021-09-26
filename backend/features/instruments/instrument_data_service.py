from datetime import datetime, timedelta
from sqlmodel import Session, select,  or_, func
from backend.features.instruments.instrument_data_models import Instrument_Data_Daily

import yfinance as yf

class InstrumentDataService:
    def __init__(self, db_session):                   
        self.db =  db_session
    
    def add_instrument_data(self, ticker:str):    
        end_date = datetime.now()            
        statement = select(func.max(Instrument_Data_Daily.trade_date)).where(Instrument_Data_Daily.ticker == ticker)
        start_date = self.db.exec(statement).first()       
        if start_date is None:
            start_date = datetime(datetime.now().year - 20, 1, 1)
        
        data = yf.download(ticker, start=start_date, end=end_date)
        data = data.reset_index()
        print(data.head())
        # creating list       
        list_data = []
        for row in data.itertuples():
            #print(row)
            list_data.append( Instrument_Data_Daily(ticker=ticker,
                                    trade_date= row.Date,
                                    open_price = row.Open,
                                    close_price = row.Close,
                                    low_price = row.Low,
                                    high_price = row.High,
                                    avg_price = (row.Low + row.High)/2,
                                    vol= row.Volume))
     
        self.db.bulk_save_objects(list_data)
        self.db.commit()


        return True

