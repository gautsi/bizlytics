import pandas as pd
import datetime as dt

class itemsframe(object):

    def __init__(self, df, pricename="Price", qtyname="Qty"):
        
        self.df = df
        
        #Add money column
        self.df["Money"] = self.df[qtyname]*self.df[pricename]
        
    def group(self, by='y'):
        
        groupfunc = None
        
        if by == 'y':
            groupfunc = lambda x: df.CreatedOn[x].year
        
        elif by == 'm':
            groupfunc = lambda x: pd.to_datetime("{}-1-{}".format(df.CreatedOn[x].month, df.CreatedOn[x].year))
            
        elif by == 'w':
            groupfunc = lambda x: pd.to_datetime("1-1-{}".format(df.CreatedOn[x].year)).to_datetime() + dt.timedelta(days=7*df.CreatedOn[x].week)
        
        elif by == 'd':
            groupfunc = lambda x : df.CreatedOn[x].date()
            
        elif by == 'prod':
            groupfunc = lambda x : df.Description[x]
            
        return self.df.groupby(groupfunc)

            
        
