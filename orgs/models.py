from django.db import models

# Create your models here.

class Severity(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name
    
class Technology(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name
    
class Analyst(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Condition(models.Model):
    SEVERITYLEVEL = (
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH'),
        ('MED-HIGH', 'MED-HIGH'),
        ('MISSED', 'MISSED'),
        ('GOOD', 'GOOD'),
    )
    
    severity = models.ForeignKey(Severity, null=True, on_delete=models.SET_NULL, blank=True)
    severityLevel = models.CharField(max_length=200, null=True, choices=SEVERITYLEVEL)
    technology = models.ForeignKey(Technology, null=True, on_delete=models.SET_NULL)
    analyst = models.ForeignKey(Analyst, null=True, on_delete=models.SET_NULL)
    entry_date = models.DateField(null=True)
    close_date = models.DateField(null=True, blank=True)
    work_req = models.CharField(max_length=300, null=True)
    work_order = models.CharField(max_length=300, null=True)
    reason = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.severityLevel


class UnitName(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Function(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class PlantTag(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.ForeignKey(UnitName, null=True, on_delete=models.SET_NULL)
    function = models.ForeignKey(Function, null=True, on_delete=models.SET_NULL)
    asset = models.ForeignKey(Asset, null=True, on_delete=models.SET_NULL)
    component = models.ForeignKey(Component, null=True, on_delete=models.SET_NULL)
    plant_tag = models.ForeignKey(PlantTag, null=True, on_delete=models.SET_NULL)
    #report = models.ForeignKey(Report, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.name.name} {self.component}"


class Report(models.Model):
    condition = models.OneToOneField(Condition, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE)

    fault = models.CharField(max_length=1000, null=True)
    comment = models.CharField(max_length=1000, null=True)
    recommendation = models.CharField(max_length=1000, null=True)

    def __str__(self): 
        try:
            return f"{self.unit.name.name}  {self.condition.entry_date}"
        except:
            return f"Dead"