from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import project


# # An elegant solution to year of birth, but not yet tested
# YEAR_CHOICES = []
# for r in range(1900, (datetime.datetime.now().year+1)):
#     YEAR_CHOICES.append((r,r))

# global def

def default_start_time():
    now = datetime.now()
    start = now.replace(hour=22, minute=0, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1)

###models
class Individual(models.Model):
    # choices
    SpeciesType = (
        ('Homo_sapiens', 'Homo_sapiens'),
        ('Mus_musculus', 'Mus_musculus'),
    )

    GenderType = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    )
    # fields
    name = models.CharField(max_length=100)
    alt_name1 = models.CharField(max_length=100, null=True, blank=True)
    alt_name2 = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey('project.Project', null=True, blank=True)
    species = models.CharField(max_length=100, choices=SpeciesType, null=True, blank=True)
    family_id = models.CharField(max_length=100, null=True, blank=True)
    relationship = models.CharField(max_length=30, null=True, blank=True)
    karyotype = models.CharField(max_length=100, null=True, blank=True)
    other_genetic_info = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderType, null=True, blank=True)
    year_of_birth = models.IntegerField(null=True, blank=True)
    #year_of_birth = models.IntegerField(_('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year) #a more elegant solution

    def __str__(self):
        return(self.name)


class Freezer(models.Model):
    # choices
    FreezerType = (
        ('-80', '-80'),
        ('LN2', 'LN2'),
        ('-20', '-20'),
        ('Fridge', 'Fridge'),
    )
    # fields
    name = models.CharField(max_length=50)
    freezer_type = models.CharField(max_length=20, choices=FreezerType, null=True, blank=True)
    shelves = models.IntegerField(null=True, blank=True)
    racks = models.IntegerField(null=True, blank=True)
    rows = models.IntegerField(null=True, blank=True)
    columns = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return(self.name)

class FreezerPos(models.Model):
    # choices
    # fields
    freezer = models.ForeignKey(Freezer, on_delete=models.CASCADE, blank=True)
    shelf = models.IntegerField(null=True, blank=True)
    rack = models.IntegerField(null=True, blank=True)
    row = models.IntegerField(null=True, blank=True)
    column = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(str(self.freezer) + '_Pos' + str(self.shelf) + '-' + str(self.rack) + '-' + str(self.row) + '-' + str(self.column))

class Box(models.Model):
    # choices
    BoxType = (
        ('box', 'box'),
        ('matrix_box', 'matrix_box'),
        ('plate', 'plate'),
    )
    # fields
    name = models.CharField(max_length=50)
    freezer_pos = models.ForeignKey(FreezerPos, null=True, blank=True)
    box_type = models.CharField(max_length=20, choices=BoxType, null=True, blank=True)
    rows = models.IntegerField(null=True, blank=True)
    columns = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return (self.name)

class BoxPos(models.Model):
    # choices

    # fields
    box = models.ForeignKey(Box, null=True, blank=True)
    row = models.CharField(max_length=3, null=True, blank=True)
    column = models.CharField(max_length=3, null=True, blank=True)
    def __str__(self):
        return (str(self.box) + '_' + str(self.row) + str(self.column))

class BoxHistory(models.Model):
    # choices
    HistoryType = (
        ('Made', 'Made'),
        ('Moved', 'Moved'),
        ('Deleted', 'Deleted'),
    )
    # fields
    box_id = models.ForeignKey(Box, null=True, blank=True)
    history_type = models.CharField(max_length=20, choices=HistoryType, null=True, blank=True)
    prev_freezer_pos = models.ForeignKey(FreezerPos, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    timestamp = models.DateTimeField(default=default_start_time)




class Sample(models.Model):
    # choices
    SampleType = (
        ('DNA', 'DNA'),
        ('RNA', 'RNA'),
        ('Cells', 'Cells'),
        ('RNASeq_Lib', 'RNASeq_Lib'),
        ('liWGS_Lib', 'liWGS_Lib'),
        ('CAPSeq_Lib', 'CAPSeq_Lib'),
        ('RNACAPSeq_Lib', 'RNACAPSeq_Lib'),
    )

    OTissueType = (
        ('LCL', 'LCL'),
        ('iPS', 'iPS'),
        ('NSC', 'NSC'),
        ('iNeurons', 'iNeurons'),
        ('brain', 'brain'),
        ('blood', 'blood'),
    )

    # fields
    individual = models.ForeignKey(Individual)
    sample_name = models.CharField(max_length=100)
    tube_name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, choices=SampleType, null=True, blank=True)
    o_tissue = models.CharField(max_length=100, choices=OTissueType, null=True, blank=True)
    parent_id = models.CharField(max_length=100, null=True, blank=True)
    box_pos = models.ForeignKey(BoxPos, null=True, blank=True)
    conc = models.FloatField(default=0, null=True, blank=True)
    vol = models.FloatField(default=0, null=True, blank=True)
    weight = models.FloatField(default=0, null=True, blank=True)
    cells = models.FloatField(default=0, null=True, blank=True)
    active = models.NullBooleanField(default=False)

    def __str__(self):
        return(self.sample_name)

class SampleHistory(models.Model):
    # choices
    EventType = (
        ('Entered', 'Entered'),
        ('Received', 'Received'),
        ('Moved', 'Moved'),
        ('Nanodrop', 'Nanodrop'),
        ('TapeStation', 'TapeStation'),
        ('Pico', 'Pico'),
        ('Weighed', 'Weighed'),
    )

    # fields
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100, choices=EventType, null=True, blank=True)
    prev_box_pos = models.ForeignKey(BoxPos, null=True, blank=True)
    prev_freezer_pos = models.ForeignKey(FreezerPos, null=True, blank=True)
    prev_conc = models.FloatField(default=0)
    prev_vol = models.FloatField(default=0)
    prev_weight = models.FloatField(default=0)
    prev_cells = models.FloatField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)
    timestamp = models.DateTimeField(default=default_start_time)


# class SampleCsv(CsvModel):
#
#     class Meta:
#         dbModel = Sample
#         delimiter = ';'




