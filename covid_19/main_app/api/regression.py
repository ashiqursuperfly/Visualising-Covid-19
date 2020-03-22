import numpy
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

graph_image_store_path="graphs"

def regressionNumpy(x ,y ,degree :int, filename: str, pointColor="blue", lineColor="black", bgColor="white",xlabel="DATE",ylabel="Y"):

    # plt.rcParams['axes.facecolor'] = bgColor
    fig = plt.figure()
    ax = fig.add_subplot(111, label="1")
    ax2 = fig.add_subplot(111, label="2", frame_on=False)

    mymodel = numpy.poly1d(numpy.polyfit(x, y, degree))
    myline = numpy.linspace(min(x),max(x),len(x)*500)
    ax.plot(myline, mymodel(myline), color=lineColor)
    ax.xaxis.set_visible(False)
    ax.set_ylabel(ylabel, fontsize=10)

    dates=list()
    for val in x:
        date_obj=datetime.fromtimestamp(val).date()
        dates.append(date_obj)

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=int(len(dates)/4)))
    # ax2.set_xlabel(xlabel, fontsize=10)

    ax2.scatter(dates, y, color=pointColor)
    ax2.yaxis.set_visible(False)
    # plt.gcf().autofmt_xdate()


    fig.tight_layout()
    file_name = os.path.join(os.path.abspath(graph_image_store_path),filename+"_numpy"+".png")
    print(file_name)
    plt.savefig(file_name)
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
