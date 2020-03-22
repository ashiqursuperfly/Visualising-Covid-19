import requests
import datetime
from ..models import *
# import regression as reg

LIMIT_COUNTRIES=10
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

    countries = list(dict(response.json())[ApiInfo.AffectedCountryList.PARAM_LIST_OF_COUNTRY])[:10]

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
        data_record = TotalCasesData(country=country_obj)
        date_time_str = record[ApiInfo.HistoryByCountry.PARAM_RECORD_DATE]
        date_time_obj = datetime.datetime.strptime(date_time_str[:10], '%Y-%m-%d')

        try:
            data_record.total_cases = record[ApiInfo.HistoryByCountry.PARAM_TOTAL_CASES]
            # data_record.total_deaths = record[ApiInfo.HistoryByCountry.PARAM_TOTAL_DEATHS]
            # data_record.total_recovered = record[ApiInfo.HistoryByCountry.PARAM_TOTAL_RECOVERED]
            # data_record.total_critical = record[ApiInfo.HistoryByCountry.PARAM_TOTAL_CRITICAL]
            data_record.record_date = date_time_obj
            data_record.save()
            print("saved", data_record)
        except:
            continue

def getHistoryOfAllCountries():
    countries = Country.objects.all()
    for c in countries:
        getHistoryByCountry(c.country_name)


