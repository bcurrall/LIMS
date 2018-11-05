from django.db import models
# from archive.models import Individual
import archive



### global def

###models
class Personnel(models.Model):
    # choices
    # fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=2,default="AK")
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return(self.first_name + ' ' + self.last_name)


class PI(models.Model):
    # choices
    # fields
    name = models.ForeignKey(Personnel, null=True, blank=True)

    def __str__(self):
        return (self.name)


class Driver(models.Model):
    # choices
    # fields
    name = models.ForeignKey(Personnel, null=True, blank=True)
    def __str__(self):
        return (self.name)

class CompAnalyst(models.Model):
    # choices
    # fields
    name = models.ForeignKey(Personnel, null=True, blank=True)
    def __str__(self):
        return (self.name)

class LabAnalyst(models.Model):
    # choices
    # fields
    name = models.ForeignKey(Personnel, null=True, blank=True)
    def __str__(self):
        return (self.name)

class Tech(models.Model):
    # choices
    # fields
    name = models.ForeignKey(Personnel, null=True, blank=True)
    capseq = models.BooleanField(default=False)
    rnaseq = models.BooleanField(default=False)
    liwgs = models.BooleanField(default=False)
    bb_liwgs = models.BooleanField(default=False)
    miseq = models.BooleanField(default=False)
    pcr = models.BooleanField(default=False)
    qpcr = models.BooleanField(default=False)
    cell_culture = models.BooleanField(default=False)
    differentiation = models.BooleanField(default=False)

    def __str__(self):
        return (self.name)




class Project(models.Model):
    # choices

    # fields
    name = models.CharField(max_length=50, unique=True)
    lead_pi = models.ForeignKey(PI, null=True, blank=True)
    lead_driver = models.ForeignKey(Driver, null=True, blank=True)
    lead_comp_anlyst = models.ForeignKey(CompAnalyst, null=True, blank=True)
    lead_lab_anlyst = models.ForeignKey(LabAnalyst, null=True, blank=True)
    lead_tech = models.ForeignKey(Tech, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return(self.name)

    # def individual(self):
    #     return archive.Individual.objects.filter(project_id=self)

class Funding(models.Model):
    # choices
    FundingType = (
        ('NIH', 'NIH'),
        ('Foundation', 'Foundation'),
        ('Private', 'Private'),
    )

    # fields
    name = models.CharField(max_length=50)
    project_id = models.ForeignKey(Project, null=True, blank=True)
    funding_type = models.CharField(max_length = 20, choices = FundingType, null = True, blank = True)
    funding_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return(self.first_name)


class PO(models.Model):
    # choices
    CompanyType = (
        ('Broad', 'Broad'),
        ('IDT', 'IDT'),
        ('GeneWiz', 'GeneWiz'),
        ('Partners', 'Partners'),
        ('Quartzy', 'Quartzy'),
        ('StockRoom', 'StockRoom'),
    )

    # fields
    name = models.CharField(max_length=50)
    funding = models.ForeignKey(Funding, null=True, blank=True)
    company = models.CharField(max_length=20, choices=CompanyType, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return(self.first_name)

