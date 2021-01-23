from main_app.api.api import *
from main_app.api.regression import *
from main_app.views import GraphFile
from main_app.models import *
import datetime
import time
import shutil
import os

def run():
    update_country_wise_charts()
    update_combined_charts()

class PieSlice:

    def __init__(self, label, size, legend_label,color):
      self.label = label
      self.size = size
      self.legend_label = legend_label
      self.color = color

    def __str__(self):
        return str(self.size)

def recordEstimatedTotalCase(target_country,predictor_model,last_data,confidence):
    print("Latest:", last_data, last_data.record_date)
    today = last_data.record_date
    tomorrow = today + datetime.timedelta(1.25)
    predicted = predictor_model(int(time.mktime(tomorrow.timetuple())))
    #
    predicted_new_cases = int((predicted - last_data.total_cases)*abs(confidence))

    if predicted_new_cases < 0:
        predicted_new_cases = 0

    print(target_country,"Predicted:",predicted,'New',predicted_new_cases,"New Date",tomorrow)


    data = EstimatedTotalCasesData(country=target_country,estimated_date=tomorrow,estimated_total_cases=predicted,estimated_new_cases=predicted_new_cases)
    data.save()

    return predicted_new_cases

def update_country_wise_charts():

    countries = Country.objects.all()

    for c in countries:
        latest_data = list()
        total=TotalCasesData.objects.filter(country=c).order_by("record_date") # TODO: this is very important
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3

        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_cases)


            latest_data.append(total[len(total)-1])
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_CASES)
            (ratio,predictedX,predictedY,predictor) = generate_model(x,y,degree)
            estimated_new_cases_tomorrow = recordEstimatedTotalCase(c,predictor,total[len(total)-1],ratio)

            if estimated_new_cases_tomorrow > 0:
                title = "Estimated New Cases Tomorrow: "+str(estimated_new_cases_tomorrow)
            else: title =  "Estimated New Cases Tomorrow: ---"
            regressionNumpy(x,y,predictedX,predictedY,file_name,
            title=title,
            lineColor="#fff766", pointColor="sienna", ylabel="Total Infected")

            print("Confidence",ratio)
        else:
            print("Not Enough Data to Generate charts TotalCases", c)


        latest_total_cases = total[len(total)-1].total_cases
        total=TotalDeathsData.objects.filter(country=c)
        latest_total_deaths = total[len(total)-1].total_deaths
        death_rate = (latest_total_deaths/latest_total_cases)*100
        title="Death Rate: "+str(round(death_rate,2))
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3

        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_deaths)
            latest_data.append(total[len(total)-1])
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_DEATHS)
            (ratio,predictedX,predictedY,predictor) = generate_model(x,y,degree)
            regressionNumpy(x,y,predictedX,predictedY,file_name,title=title,lineColor="tomato", pointColor="tab:red", ylabel="Total Deaths")

        else:
            print("Not Enough Data to Generate charts TotalDeaths", c)

        total=TotalRecoveredData.objects.filter(country=c)
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3
        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_recovered)
            latest_data.append(total[len(total)-1])
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_RECOVERED)
            (ratio,predictedX,predictedY,predictor) = generate_model(x,y,degree)
            regressionNumpy(x,y,predictedX,predictedY,file_name,lineColor="lightgreen", pointColor="tab:green", ylabel="Total Recovered")

        else:
            print("Not Enough Data to Generate charts Total Recovered", c)

        total=TotalCriticalData.objects.filter(country=c)
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3
        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_critical)
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_CRITICAL)
            (ratio,predictedX,predictedY,predictor) = generate_model(x,y,degree)
            regressionNumpy(x,y,predictedX,predictedY,file_name,lineColor="plum", pointColor="rebeccapurple", ylabel="Total Critical")
        else:
            print("Not Enough Data to Generate charts TotalCritical", c)

        pie_chart_file_name=os.path.join(os.path.abspath(GraphFile.pie_store_path),c.country_name+".png")
        infected_right_now = latest_data[0].total_cases - (latest_data[1].total_deaths + latest_data[2].total_recovered)


        colors=["#fff766","tomato","lightgreen","plum"]

        slice1 = PieSlice(
         label=str(latest_data[0].total_cases),
         legend_label="Total Cases",
         size=latest_data[0].total_cases,
         color=colors[0]
        )
        slice2 = PieSlice(
         label=str(latest_data[1].total_deaths),
         legend_label="Deaths",
         size=latest_data[1].total_deaths,
         color=colors[1]
        )
        slice3 = PieSlice(
         label=str(latest_data[2].total_recovered),
         legend_label="Recovered",
         size=latest_data[2].total_recovered,
         color=colors[2]
        )
        slice4 = PieSlice(
         label=str(infected_right_now),
         legend_label="Active Cases",
         size=infected_right_now,
         color=colors[3]
        )
        slices = [slice1, slice2, slice3, slice4]
        slices.sort(key=lambda x: x.size, reverse=False)
        print("Sorted",slices[0], slices[1], slices[2], slices[3])

        sizes = [slices[0].size, slices[2].size, slices[1].size, slices[3].size]

        labels = [slices[0].label, slices[2].label, slices[1].label, slices[3].label]
        legends = [slices[0].legend_label, slices[2].legend_label, slices[1].legend_label, slices[3].legend_label]

        colors = [slices[0].color, slices[2].color, slices[1].color, slices[3].color]
        explode = (0.03,0.06,0.03,0.06)

        create_pie(legends=legends,labels= labels,sizes= sizes,colors=colors,explode=explode,filename=pie_chart_file_name)
    print("Done")


'''
Combined Charts....
'''
def update_combined_charts():
    update_heatmap()

def update_heatmap():
    countries = Country.objects.all()
    DAY_OFFSET = int(TotalCasesData.objects.count()*0.08 / len(countries))
    print("Total Countries:", len(countries), "OFFSET", DAY_OFFSET)
    heatmap_data = list()
    for c in countries:
        total=TotalCasesData.objects.filter(country=c).order_by("record_date")
        for i in range(0,len(total)-DAY_OFFSET,DAY_OFFSET):
            new_cases = total[i+DAY_OFFSET].total_cases - total[i].total_cases

            if new_cases < 0 or new_cases is None:
                print("E.R.R.O.R.\n!!!!!!!!!!!!!!!!!!!!!!!!ERROR: NEGATIVE new_cases SHOULD BE IMPOSSIBLE!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(total[i+DAY_OFFSET],total[i+DAY_OFFSET].record_date,total[i],total[i].record_date)
                continue

            csv_row = [str(c.country_name),str(total[i+DAY_OFFSET].record_date), int(new_cases)]
            heatmap_data.append(csv_row)

    file_name=os.path.join(os.path.abspath(GraphFile.combined_store_path), "new_cases_heatmap"+".png")
    create_heatmap(file_name, heatmap_data,title="New Cases Heatmap")

def write_csv(rows:list):
    import csv
    with open('main_app/api/new_cases_heatmap.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in rows:
            employee_writer.writerow(row)

