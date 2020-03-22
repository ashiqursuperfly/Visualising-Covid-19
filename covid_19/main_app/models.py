from django.db import models
import requests

country_code_api="https://restcountries.eu/rest/v2/name/{NAME}"
country_flag_api="https://www.countryflags.io/{CODE}/flat/64.png"

class Country(models.Model):
    country_name = models.CharField(max_length=255)

    def getCountry(country: str):
        try:
            c = Country.objects.get(country_name=country.upper())
        except:
            c = None
        return c

    def save(self, *args, **kwargs):
        try:
            c = Country.objects.get(country_name=self.country_name.upper())
        except:
            c = None

        if c is None:
            self.country_name=str(self.country_name).upper()
            return super(Country, self).save(*args, **kwargs)
        else:
            #print("Log:Already Exists. Deleting.", Country.objects.all())
            c.delete()
            #print("Log:after deleting", Country.objects.all())
            self.country_name=str(self.country_name).upper()
            return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name_plural = "Countries"


class Covid19Data(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    record_date = models.DateField()
    total_cases = models.PositiveIntegerField()
    total_deaths = models.PositiveIntegerField()
    total_critical = models.PositiveIntegerField()
    total_recovered = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        try:
            d = Covid19Data.objects.get(country=self.country, record_date=self.record_date)
        except:
            d = None

        if d is None:
            return super(Covid19Data, self).save(*args, **kwargs)
        else:
            d.delete()
            return super(Covid19Data, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Covid19Data"


