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
    closed = models.BooleanField(null=True, default=False)
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

class FaultGroup(models.Model):
    fault = models.CharField(max_length=200, null=True, blank=True)
    fault_group = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.fault}"

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    condition = models.OneToOneField(Condition, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE)

    fault = models.CharField(max_length=1000, null=True)
    fault_group = models.ManyToManyField(FaultGroup, blank=True)
    comment = models.CharField(max_length=1000, null=True)
    recommendation = models.CharField(max_length=1000, null=True)

    def __str__(self):
        try:
            return f"{self.unit.name.name}  {self.condition.entry_date}"
        except:
            return f"Dead"