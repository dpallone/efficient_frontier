import pandas as pd
import numpy as np
import yahoo_finance as yf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import datetime as dt

def efficient_frontier(tickA,tickB):
    print "connecting to ", tickA, "....."
    assetA = yf.Share(tickA)
    print "connecting to ", tickB, "....."
    assetB = yf.Share(tickB)
    
    print "getting info for ", tickA, "....."
    infoA = assetA.get_info()
    print "getting info for ", tickB, "....."
    infoB = assetB.get_info()
    
    start =  max(make_date(infoA['start']),make_date(infoB['start']))
    end = min(make_date(infoA['end']), make_date(infoB['end']))
   
    print "getting data for " + tickA + "....."
    historicalA = assetA.get_historical(str(start),str(end))
    print "getting data for " + tickB + "....."
    historicalB = assetB.get_historical(str(start),str(end))
    print "data gathered"
    dataA = pd.DataFrame(historicalA)
    dataB = pd.DataFrame(historicalB)
    
    dataA['Close'] = map(float, dataA['Close'])
    dataB['Close'] = map(float, dataB['Close'])

    expectedA = ((dataA['Close'][0] /dataA['Close'][len(dataA)-1]) ** 
                 (1 / ((end - start).days / 365.25)) - 1)
    expectedB = ((dataB['Close'][0] / dataB['Close'][len(dataB)-1]) ** 
                 (1 / ((end - start).days / 365.25)) - 1)
    
    dataA['Returns'] = np.log(dataA['Close'] / dataA['Close'].shift(1))
    dataB['Returns'] = np.log(dataB['Close'] / dataB['Close'].shift(1))
    
    varianceA = np.var(dataA['Returns'])
    varianceB = np.var(dataB['Returns'])
    
    std_devA = np.std(dataA['Returns'])
    std_devB = np.std(dataB['Returns'])

    weights = pd.DataFrame({
            tickA : [.05 * i for i in range(21)],
            tickB : [.05 * i for i in range(21)][::-1]
            })

    correlation = np.correlate(dataA['Returns'][1:],dataB['Returns'][1:])
   
    expectedP = (weights[tickA] * expectedA) +\
            (weights[tickB] * expectedB)

    varianceP = ((weights[tickA] ** 2) * varianceA) +\
                ((weights[tickB] ** 2) * varianceB) +\
                (2 * weights[tickA] * weights[tickB] *\
                 std_devA * std_devB * correlation[0])
    
    portfolio_stats = pd.DataFrame()
    portfolio_stats['Expected Return'] = expectedP
    portfolio_stats['Variance'] = varianceP
    portfolio_stats['w-'+tickA] = weights[tickA]
    portfolio_stats['w-'+tickB] = weights[tickB]
    portfolio_stats['risk tolerance'] = np.diff(portfolio_stats['Expected Return'] / np.diff(portfolio_stats['Variance'])
    x = portfolio_stats['Variance']
    y = portfolio_stats['Expected Return']
    z = portfolio_stats['risk tolerance']
    
                                                

    print portfolio_stats
    
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot(xs=x, ys=y, zs = z, zdir='z')
	
    plt.plot(x, y)
    plt.show()
    print "done"

def make_date(datestring):
    year = int(datestring[:4])
    month = int(datestring[5:7])
    day = int(datestring[8:])
    return dt.date(year, month, day)

if __name__ == "__main__":
    efficient_frontier('GOOGL', 'FB')
    
    
    
    
    
    
    
