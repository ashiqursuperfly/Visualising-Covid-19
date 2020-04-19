from django.db import models
import requests

class Country(models.Model):
    country_name = models.CharField(max_length=255)
    continent_id=models.PositiveIntegerField(help_text="EUROPE-1,NORTH-AMERICA-2,ASIA-3,SOUTH-AMERICA-4", default=1)
    code=models.CharField(max_length=3, default="XX")

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

class TotalCasesData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    record_date = models.DateField()
    total_cases = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        try:
            d = TotalCasesData.objects.filter(country=self.country, record_date=self.record_date)
        except:
            d = None

        if d is None:
            return super(TotalCasesData, self).save(*args, **kwargs)
        else:
            d.delete()
            return super(TotalCasesData, self).save(*args, **kwargs)

    def __str__(self):
        return self.country.country_name + ":" + str(self.total_cases)

    class Meta:
        verbose_name_plural = "TotalCases"

class TotalDeathsData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    record_date = models.DateField()
    total_deaths = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        try:
            d = TotalDeathsData.objects.filter(country=self.country, record_date=self.record_date)
        except:
            d = None

        if d is None:
            return super(TotalDeathsData, self).save(*args, **kwargs)
        else:
            d.delete()
            return super(TotalDeathsData, self).save(*args, **kwargs)

    def __str__(self):
        return self.country.country_name + ":" + str(self.total_deaths)
    class Meta:
        verbose_name_plural = "Deaths"

class TotalRecoveredData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    record_date = models.DateField()
    total_recovered = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        try:
            d = TotalRecoveredData.objects.filter(country=self.country, record_date=self.record_date)
        except:
            d = None

        if d is None:
            return super(TotalRecoveredData, self).save(*args, **kwargs)
        else:
            d.delete()
            return super(TotalRecoveredData, self).save(*args, **kwargs)

    def __str__(self):
        return self.country.country_name + ":" + str(self.total_recovered)

    class Meta:
        verbose_name_plural = "Recoveries"

class TotalCriticalData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    record_date = models.DateField()
    total_critical = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        try:
            d = TotalCriticalData.objects.filter(country=self.country, record_date=self.record_date)
        except:
            d = None

        if d is None:
            return super(TotalCriticalData, self).save(*args, **kwargs)
        else:
            d.delete()
            return super(TotalCriticalData, self).save(*args, **kwargs)

    def __str__(self):
        return self.country.country_name + ":" + str(self.total_critical)
    class Meta:
        verbose_name_plural = "CriticalCases"

class EstimatedTotalCasesData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    estimated_date = models.DateField()
    estimated_total_cases = models.PositiveIntegerField()
    estimated_new_cases = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        try:
            d = EstimatedTotalCasesData.objects.filter(country=self.country, estimated_date=self.estimated_date)
        except:
            d = None

        if d is None:
            return super(EstimatedTotalCasesData, self).save(*args, **kwargs)
        else:
            d.delete()
            return super(EstimatedTotalCasesData, self).save(*args, **kwargs)

    def __str__(self):
        return self.country.country_name + ":" + str(self.estimated_total_cases)

    class Meta:
        verbose_name_plural = "EstimatedTotalCases"
