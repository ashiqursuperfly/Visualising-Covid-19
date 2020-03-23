import requests
import datetime
from ..models import *
# import regression as reg

LIMIT_COUNTRIES=2
class ApiInfo:

    def create_session():
        s = requests.Session()
        s.headers.update({"x-rapidapi-host": "coronavirus-monitor.p.rapidapi.com"})
        s.headers.update({"x-rapidapi-key": "5090fcf701mshd0deef622896cd5p10a420jsnc5ecad3a59b4"})

        return s

    class WorldStat:
        ENDPOINT="https://coronavirus-monitor.p.rapidapi.com/coronavirus/worldstat.php"

    class HistoryByCountry:
        ENDPOINT="https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php"
        PARAM_COUNTRY="country"
        PARAM_STAT_BY_COUNTRY="stat_by_country"
        PARAM_RECORD_DATE="record_date"
        PARAM_TOTAL_CASES="total_cases"
        PARAM_TOTAL_DEATHS="total_deaths"
        PARAM_TOTAL_RECOVERED="total_recovered"
        PARAM_TOTAL_CRITICAL="serious_critical"

    class AffectedCountryList:
        ENDPOINT="https://coronavirus-monitor.p.rapidapi.com/coronavirus/affected.php"
        PARAM_LIST_OF_COUNTRY="affected_countries"

def getAffectedCountries():

    s = ApiInfo.create_session()
    response = s.get(ApiInfo.AffectedCountryList.ENDPOINT)

    countries = list(dict(response.json())[ApiInfo.AffectedCountryList.PARAM_LIST_OF_COUNTRY])[:LIMIT_COUNTRIES]

    for c in countries:
        _ = Country(country_name=c)
        _.save()
    return countries

def getHistoryByCountry(country_name: str):

    s = ApiInfo.create_session()
    PARAMS = {ApiInfo.HistoryByCountry.PARAM_COUNTRY: country_name}
    response = s.get(ApiInfo.HistoryByCountry.ENDPOINT, params=PARAMS)

    country_obj = Country.getCountry(country_name)

    records = list(dict(response.json())[ApiInfo.HistoryByCountry.PARAM_STAT_BY_COUNTRY])

    for record in records:
        data_record_1 = TotalCasesData(country=country_obj)
        data_record_2 = TotalDeathsData(country=country_obj)
        data_record_3 = TotalRecoveredData(country=country_obj)
        data_record_4 = TotalCriticalData(country=country_obj)
        date_time_str = record[ApiInfo.HistoryByCountry.PARAM_RECORD_DATE]
        date_time_obj = datetime.datetime.strptime(date_time_str[:10], '%Y-%m-%d')


        _1 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_CASES]).replace(",",""))
        _2 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_DEATHS]).replace(",",""))
        _3 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_RECOVERED]).replace(",",""))
        _4 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_CRITICAL]).replace(",",""))

        if _1 is not None:
            data_record_1.record_date = date_time_obj
            data_record_1.total_cases = _1
            data_record_1.save()
            print("saved1", data_record_1)

        if _2 is not None:
            data_record_2.record_date = date_time_obj
            data_record_2.total_deaths = _2
            data_record_2.save()
            print("saved2", data_record_2)

        if _3 is not None:
            data_record_3.record_date = date_time_obj
            data_record_3.total_recovered = _3
            data_record_3.save()
            print("saved3", data_record_3)

        if _4 is not None:
            data_record_4.record_date = date_time_obj
            data_record_4.total_critical = _4
            data_record_4.save()
            print("saved4", data_record_4)


def getHistoryOfAllCountries():
    countries = Country.objects.all()
    for c in countries:
        getHistoryByCountry(c.country_name)


def populate_db():
    getAffectedCountries()
    getHistoryOfAllCountries()