import numpy
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

def regressionNumpy(x ,y ,degree :int, filename: str, pointColor="midnightblue", lineColor="black", bgColor="honeydew",xlabel="DATE",ylabel="Y"):

    plt.rcParams['axes.facecolor'] = bgColor
    plt.rcParams['savefig.facecolor'] = bgColor
    plt.rcParams['xtick.color']=pointColor
    plt.rcParams['ytick.color']=pointColor
    plt.rcParams['xtick.labelsize']=10
    plt.rcParams['ytick.labelsize']=10

    # print(plt.rcParams)

    fig = plt.figure()
    ax = fig.add_subplot(111, label="1")

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    ax.spines['right'].set_color(bgColor)
    ax.spines['top'].set_color(bgColor)
    ax.spines['left'].set_color("lightgray")
    ax.spines['bottom'].set_color("lightgray")


    ax2 = fig.add_subplot(111, label="2", frame_on=False)

    mymodel = numpy.poly1d(numpy.polyfit(x, y, degree))
    myline = numpy.linspace(min(x),max(x),len(x)*500)
    ax.plot(myline, mymodel(myline), color=lineColor, linewidth=6)
    ax.xaxis.set_visible(False)
    ax.set_ylabel(ylabel, fontsize=10, color=pointColor)

    dates=list()
    for val in x:
        date_obj=datetime.fromtimestamp(val).date()
        dates.append(date_obj)

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=int(math.ceil(len(dates)/4))))
    # ax2.set_xlabel(xlabel, fontsize=10)

    ax2.scatter(dates, y, color=pointColor, linewidth=10)
    ax2.yaxis.set_visible(False)
    # plt.gcf().autofmt_xdate()


    # fig.tight_layout()
    # print(filename)
    plt.savefig(filename)
    plt.close()

    return mymodel

from sklearn.linear_model import LinearRegression

def regressionScikit(x ,y , filename: str):
    x = numpy.array(x).reshape(-1, 1)  # values converts it into a numpy array
    y = numpy.array(y).reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(x, y)  # perform linear regression
    Y_pred = linear_regressor.predict(x)  # make predictions

    plt.scatter(x, y)
    plt.plot(x, Y_pred, color='red')
    plt.savefig(filename+"_scikit"+".png")
