import requests
import datetime
from ..models import *
from ..logger import *


class ApiInfo:

    country_code_api="https://restcountries.eu/rest/v2/name/{NAME}" #?fullText=true"
    country_flag_api="https://www.countryflags.io/{CODE}/flat/64.png"

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

def get_country_flag(name: str):
    s = requests.Session()
    response=s.get(ApiInfo.country_code_api.replace("{NAME}",name))
    # print(response)
    if response.status_code == 200:
        country_code=dict(list(response.json())[0])["alpha2Code"]
        print(country_code)
        return ApiInfo.country_flag_api.replace("{CODE}",country_code)
    else: return ""

def getAffectedCountries(limit: int):

    s = ApiInfo.create_session()
    response = s.get(ApiInfo.AffectedCountryList.ENDPOINT)

    countries = list(dict(response.json())[ApiInfo.AffectedCountryList.PARAM_LIST_OF_COUNTRY])[:limit]

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

        try:
            _1 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_CASES]).replace(",",""))
            if _1 is not None and len(str(_1).strip())>0:
                data_record_1.record_date = date_time_obj
                data_record_1.total_cases = _1
                data_record_1.save()
                #print("saved1", data_record_1)
        except Exception as e:
            log("ignored-total-cases with error:" + str(e) +" "+ country_obj.country_name)

        try:
            _2 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_DEATHS]).replace(",",""))
            if _2 is not None and len(str(_2).strip())>0:
                data_record_2.record_date = date_time_obj
                data_record_2.total_deaths = _2
                data_record_2.save()
                #print("saved2", data_record_2)
        except Exception as e:
            log("ignored-total-deaths with error:" + str(e) +" "+ country_obj.country_name)

        try:
            _3 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_RECOVERED]).replace(",",""))
            if _3 is not None and len(str(_3).strip())>0:
                data_record_3.record_date = date_time_obj
                data_record_3.total_recovered = _3
                data_record_3.save()
                #print("saved3", data_record_3)
        except Exception as e:
            log("ignored-total-recovered with error:" + str(e) +" "+ country_obj.country_name)

        try:
            _4 = int(str(record[ApiInfo.HistoryByCountry.PARAM_TOTAL_CRITICAL]).replace(",",""))
            if _4 is not None and len(str(_4).strip())>0:
                data_record_4.record_date = date_time_obj
                data_record_4.total_critical = _4
                data_record_4.save()
                #print("saved4", data_record_4)
        except Exception as e:
            log("ignored-total-critical with error:" + str(e) +" "+ country_obj.country_name)

def getHistoryOfAllCountries():
    countries = Country.objects.all()
    for c in countries:
        log("Reading Data:"+c.country_name)
        getHistoryByCountry(c.country_name)

def populate_db(limit: int, shouldLoadCountries = True):
    # print("INFO: not fetching countries from API. fetching only from database")
    clear_log()
    if shouldLoadCountries:
        getAffectedCountries(limit)

    getHistoryOfAllCountries()


