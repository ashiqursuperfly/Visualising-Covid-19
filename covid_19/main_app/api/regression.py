import numpy
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import seaborn as sns
import pandas as pd

LINE_WIDTH = 15
POINT_WIDTH = 400

def regressionNumpy(x ,y ,predictedX,predictedY,filename: str,title="",pointColor="midnightblue", lineColor="#222222", bgColor="black",xlabel="DATE",ylabel="Y"):


    plt.rcParams['figure.figsize'] = 15, 10
    plt.rcParams['axes.facecolor'] = bgColor
    plt.rcParams['savefig.facecolor'] = bgColor
    plt.rcParams['xtick.color']=lineColor
    plt.rcParams['ytick.color']=lineColor
    plt.rcParams['xtick.labelsize']=15
    plt.rcParams['ytick.labelsize']=15
    plt.rcParams["font.family"] = "sans-serif"

    # print(plt.rcParams)

    fig = plt.figure()
    ax = fig.add_subplot(111, label="1")
    ax.set_title(title, color=lineColor, fontsize=24)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    ax.spines['right'].set_color(bgColor)
    ax.spines['top'].set_color(bgColor)
    ax.spines['left'].set_color("lightgray")
    ax.spines['bottom'].set_color("lightgray")

    ax2 = fig.add_subplot(111, label="2", frame_on=False)

    ax.plot(predictedX, predictedY, color=lineColor, linewidth=LINE_WIDTH)
    ax.xaxis.set_visible(False)
    ax.set_ylabel(ylabel, fontsize=22, color=lineColor, labelpad=25)

    dates=list()
    for val in x:
        date_obj=datetime.fromtimestamp(val).date()
        dates.append(date_obj)


    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=int(math.ceil(len(dates)/10))))
    # ax2.set_xlabel(xlabel, fontsize=22, labelpad=5)

    ax2.tick_params(axis='x', rotation=45)

    ax2.scatter(dates, y, color=pointColor, s=POINT_WIDTH)
    ax2.yaxis.set_visible(False)
    # plt.gcf().autofmt_xdate()


    # fig.tight_layout()
    # print(filename)
    plt.savefig(filename)
    plt.close()

def generate_model(x,y,degree):
    mymodel = numpy.poly1d(numpy.polyfit(x, y, degree))
    myline = numpy.linspace(min(x),max(x),len(x)*500)

    yhat = mymodel(myline)
    # ybar = numpy.sum(y)/len(y)
    # ssreg = numpy.sum((yhat-ybar)**2)
    # sstot = numpy.sum((y - ybar)**2)
    # if sstot != 0: ratio = ssreg / sstot
    # else: ratio = 0

    correlation_matrix = numpy.corrcoef(x, y)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2

    return (r_squared,myline,yhat,mymodel)

def create_pie(legends: list, labels : list,sizes :list,colors: list,explode,filename: str):

    print("Sizes",sizes)

    # plt.axis('equal')
    # plt.tight_layout()
    # plt.savefig(filename)
    # plt.close()

    plt.rcParams['figure.figsize'] = 10, 12
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams['savefig.facecolor'] = "black"
    fig1, ax1 = plt.subplots()
    patches, texts = ax1.pie(sizes, colors = colors, labels=labels, startangle=90, explode=explode, textprops={'color':"w"}) # labeldistance=2
    leg = plt.legend(patches, legends, bbox_to_anchor=(1,0), loc="lower right",borderpad=2,labelspacing=1.5, bbox_transform=fig1.transFigure, prop={'size': 16})

    for color,text in zip(colors,leg.get_texts()):
        text.set_color(color)

    #draw circle
    centre_circle = plt.Circle((0,0),0.6,fc='black')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def create_heatmap(filename: str, values: list,title="", xlabel = "Date", ylabel="Country",value_label="New Deaths",textColor="#fff766", bgColor="black"):

    df = pd.DataFrame(values, columns = [ylabel, xlabel, value_label])
    df = df.pivot(ylabel, xlabel, value_label)


    print(df)
    df = df.fillna(0)

    print(df)

    plt.rcParams['figure.figsize'] = 25, 15
    plt.rcParams['axes.facecolor'] = bgColor
    plt.rcParams['savefig.facecolor'] = bgColor
    plt.rcParams['xtick.color']=textColor
    plt.rcParams['ytick.color']=textColor
    plt.rcParams['xtick.labelsize']=15
    plt.rcParams['ytick.labelsize']=15
    plt.rcParams["font.family"] = "sans-serif"
    #sns.set()

    sns_plot = sns.heatmap(data=df,annot=False, cmap="hot")
    sns_plot.tick_params(axis='x', rotation=45)
    sns_plot.set_title(title, color=textColor, fontsize=24)

    fig = sns_plot.get_figure()
    fig.savefig(filename)
    plt.close()

