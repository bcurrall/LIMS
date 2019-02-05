from django.db import models

class Library(models.Model):
    LibraryType = (
        ('RNASeq', 'RNASeq'),
        ('liWGS', 'liWGS'),
        ('siWGS', 'siWGS'),
        ('matepair', 'matepair'),
        ('PCRSeq', 'PCRSeq'),
    )


    # plate setup
    gtc_code = models.CharField(max_length=100, null=True, blank=True)
    library_type = models.CharField(max_length=100, choices=LibraryType, null=True, blank=True)
    plate_name = models.CharField(max_length=100, null=True, blank=True)
    well = models.CharField(max_length=100, null=True, blank=True)
    sample_name = models.ForeignKey('sample.Sample', on_delete=models.PROTECT, null=True, blank=True) #links to sample
    library_name = models.CharField(max_length=100)
    amount_of_sample_used = models.FloatField(default=0, null=True, blank=True)
    amount_of_water_used = models.FloatField(default=0, null=True, blank=True)
    plate_comments = models.TextField(null=True, blank=True)

    # library QC
    illumina_barcode_plate = models.CharField(max_length=100, null=True, blank=True)
    barcode_well = models.CharField(max_length=100, null=True, blank=True)
    i7_barcode = models.CharField(max_length=100, null=True, blank=True)
    i5_barcode = models.CharField(max_length=100, null=True, blank=True)
    library_amount = models.CharField(max_length=100, null=True, blank=True)
    tapestation_size_bp = models.IntegerField(null=True, blank=True)
    tapestation_conc = models.FloatField(null=True, blank=True)
    tapestation_molarity_nM = models.FloatField(null=True, blank=True)
    qpcr_conc = models.FloatField(null=True, blank=True)
    qubit_conc = models.FloatField(null=True, blank=True)
    qc_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return(self.library_name)


class Pool(models.Model):
    pool_name = models.CharField(max_length=100)
    tapestation_size_bp = models.IntegerField(null=True, blank=True)
    tapestation_conc = models.FloatField(null=True, blank=True)
    tapestation_molarity_nM = models.FloatField(null=True, blank=True)
    qpcr_conc = models.FloatField(null=True, blank=True)
    qubit_conc = models.FloatField(null=True, blank=True)
    made_date = models.FloatField(default=0, null=True, blank=True)
    made_by = models.CharField(max_length=100, null=True, blank=True)
    pool_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return(self.pool_name)


class PoolingAmount(models.Model): # integrates pools and amount of each library used
    pool_name = models.ForeignKey(Pool, on_delete=models.PROTECT, null=True, blank=True) #links to pool
    library_name = models.ForeignKey(Library, on_delete=models.PROTECT, null=True, blank=True) #links to library
    rel_proportion = models.CharField(max_length=100)
    amount_of_library_used = models.FloatField(default=0, null=True, blank=True)
    library_amount = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return(str(self.pool_name) + '_' + str(self.library_name))