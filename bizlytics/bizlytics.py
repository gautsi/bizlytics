import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
pd.options.display.mpl_style = 'default'
import matplotlib.dates as mdates
import matplotlib.ticker as tic

daydict = {0: 'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}

quarteryeardates = [dt.date(2011,1,1) + dt.timedelta(weeks=n*13.06) for n in xrange(16)]

halfyeardates = [dt.date(2011,1,1) + dt.timedelta(weeks=n*26.11) for n in xrange(8)]

class itemsframe(object):

    def __init__(self, df, pricename="Price", qtyname="Qty"):
        
        self.df = df
        
        #Add money column
        self.df["Money"] = self.df[qtyname]*self.df[pricename]
        
    def group(self, by='y'):
        
        groupfunc = None
        
        if by == 'y':
            groupfunc = lambda x: self.df.CreatedOn[x].year
        
        elif by == 'm':
            groupfunc = lambda x: pd.to_datetime("{}-1-{}".format(self.df.CreatedOn[x].month, self.df.CreatedOn[x].year))
            
        elif by == 'w':
            groupfunc = lambda x: pd.to_datetime("1-1-{}".format(self.df.CreatedOn[x].year)).to_datetime() + dt.timedelta(days=7*self.df.CreatedOn[x].week)
        
        elif by == 'd':
            groupfunc = lambda x : self.df.CreatedOn[x].date()
            
        elif by == 'prod':
            groupfunc = lambda x : self.df.Description[x]
            
        return self.df.groupby(groupfunc)
        
        
def dateplot(plotseries=[[[dt.date(2011, 1, 1), dt.date(2012, 2, 4)],[3,-1]]], 
             monthlocator=range(1,13), dateformatter='%b\n%Y', 
             title='', showlegend=False, loc='best', legfontsize=20, save=True, filename='test'):
    plt.clf()
    plt.gca().xaxis.set_major_locator(
    mdates.MonthLocator(bymonth=monthlocator)
    )
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter(dateformatter)
    )
    for ser in plotseries:
        xvals = ser[0]
        yvals = ser[1]
        label = ser[2] if len(ser) == 3 else ''
        plt.plot_date(x=xvals, y=yvals, fmt="-", lw=4, label=label)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.title(title, fontsize=30)
    if showlegend:
        plt.legend(loc=loc, fancybox=True, framealpha=0.5, fontsize=legfontsize)
    plt.gcf().set_size_inches(16,9)
    plt.savefig(filename, dpi=300, bbox_inches='tight')


def dfbyperiod(start_period, stop_period, dfp):
    return dfp[(dfp.CreatedOn >= start_period) & (dfp.CreatedOn < stop_period)]

def gbpsbyperiod(start_period, stop_period, df2):
    dfp = dfbyperiod(start_period, stop_period, df2)
    itfp = itemsframe(dfp[dfp.Description != "Account Payment"])
    return itfp.group(by='prod').sum()

def dfbyyear(yr, dfp):
    return dfbyperiod(dt.date(yr, 1, 1), dt.date(yr+1, 1, 1), dfp)

def gbpsbyyear(yr, dfp):
    dfy = dfbyyear(yr, dfp)
    itfy = itemsframe(dfy[dfy.Description != "Account Payment"])
    return itfy.group(by='prod').sum()
    

def best_selling_products(dates, top=3):
    
    prods = []
    
    for date_ind in xrange(len(dates)-1):
        prods += biz.gbpsbyperiod(dates[date_ind], dates[date_ind+1], df2=df).sort(columns='Money', ascending=0)[:top].index
    prods = set(prods)
    return prods
    
def get_moneylist(prod, dates):
    moneylist = []
    for date_ind in xrange(len(dates)-1):
        money = biz.gbpsbyperiod(dates[date_ind], dates[date_ind+1], df2=df[df.Description == prod]).Money
        if len(money) == 0:
            money = 0
        else:
            money = money[0]
        moneylist += [money]
    return moneylist         
        
