from django.db import models

#This is a super model - its done purposely (and not very databasey) in case db falls apart and have to go back to excel files
class Sample(models.Model):
    ## choices
    SpeciesType = (
        ('Homo_sapiens', 'Homo_sapiens'),
        ('Mus_musculus', 'Mus_musculus'),
    )
    GenderType = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    )
    FreezerType = (
        ('-80', '-80'),
        ('LN2', 'LN2'),
        ('-20', '-20'),
        ('Fridge', 'Fridge'),
    )
    SampleType = (
        ('DNA', 'DNA'),
        ('RNA', 'RNA'),
        ('Cells', 'Cells'),
        ('RNASeq_Lib', 'RNASeq_Lib'),
        ('liWGS_Lib', 'liWGS_Lib'),
        ('CAPSeq_Lib', 'CAPSeq_Lib'),
        ('RNACAPSeq_Lib', 'RNACAPSeq_Lib'),
    )

    SourceTissueType = (
        ('brain', 'brain'),
        ('brain_hippocampus', 'brain_hippocampus'),
        ('brain_cortex', 'brain_cortex'),
        ('brain_cerebellum', 'brain_cerebellum'),
        ('blood', 'blood'),
        ('liver', 'liver'),
        ('adipose', 'adipose'),
        ('skin', 'skin'),
    )
    CellLineType = (
        ('LCL', 'LCL'),
        ('iPS', 'iPS'),
        ('NSC', 'NSC'),
        ('iNeurons', 'iNeurons'),
        ('fibroblast', 'fibroblast'),
    )
    BoxType = (
        ('box', 'box'),
        ('matrix_box', 'matrix_box'),
        ('plate', 'plate'),
    )

    ## fields
    # id's
    sample_name = models.CharField(max_length=100, null=False, blank=True)
    aliquot_id = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=100, null=True, blank=True)
    sample_type = models.CharField(max_length=100, choices=SampleType, null=True, blank=True)
    source_tissue = models.CharField(max_length=100, choices=SourceTissueType, null=True, blank=True)
    conc = models.FloatField(default=0, null=True, blank=True)
    vol = models.FloatField(default=0, null=True, blank=True)
    weight = models.FloatField(default=0, null=True, blank=True)
    cells = models.FloatField(default=0, null=True, blank=True)
    alt_name1 = models.CharField(max_length=100, null=True, blank=True)
    alt_name2 = models.CharField(max_length=100, null=True, blank=True)

    # sample vitals - general
    species = models.CharField(max_length=100, choices=SpeciesType, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderType, null=True, blank=True)
    family_id = models.CharField(max_length=100, null=True, blank=True)
    relationship = models.CharField(max_length=30, null=True, blank=True)
    study_model = models.CharField(max_length=30, null=True, blank=True)
    case_control = models.CharField(max_length=30, null=True, blank=True)
    collected_by = models.CharField(max_length=30, null=True, blank=True)
    date_collected = models.IntegerField(null=True, blank=True)
    collection_batch = models.CharField(max_length=30, null=True, blank=True)

    # sample vitals - human
    year_of_birth = models.IntegerField(null=True, blank=True) # human specific
    race = models.CharField(max_length=30, null=True, blank=True)
    ethnicity = models.CharField(max_length=30, null=True, blank=True)


    # sample vitals - non-human
    date_of_birth = models.IntegerField(null=True, blank=True)  # non-human specific
    strain = models.CharField(max_length=30, null=True, blank=True)
    brood = models.CharField(max_length=30, null=True, blank=True)

    # sample vitals - cell lines
    cell_line_id = models.CharField(max_length=30, null=True, blank=True)
    passage_number = models.CharField(max_length=30, null=True, blank=True)
    cell_line_mutation = models.CharField(max_length=30, null=True, blank=True)
    cell_line_type = models.CharField(max_length=100, choices=CellLineType, null=True, blank=True)


    # sample genotype/phenotye
    karyotype = models.CharField(max_length=100, null=True, blank=True)
    genetic_array = models.CharField(max_length=100, null=True, blank=True)
    other_genetic_info = models.CharField(max_length=200, null=True, blank=True)

    # location
    freezer_name = models.CharField(max_length=50, null=True, blank=True)
    freezer_type = models.CharField(max_length=20, choices=FreezerType, null=True, blank=True)
    freezer_shelf = models.IntegerField(null=True, blank=True)
    freezer_rack = models.IntegerField(null=True, blank=True)
    freezer_row = models.IntegerField(null=True, blank=True)
    freezer_column = models.IntegerField(null=True, blank=True)
    box_name = models.CharField(max_length=50, null=True, blank=True)
    box_type = models.CharField(max_length=20, choices=BoxType, null=True, blank=True)
    aliquot_pos_row = models.IntegerField(null=True, blank=True)
    aliquot_pos_column = models.IntegerField(null=True, blank=True)


    # year_of_birth = models.IntegerField(_('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year) #a more elegant solution

    def __str__(self):
        return(self.sample_name)


