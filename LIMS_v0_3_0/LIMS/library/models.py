from django.db import models

import datetime

class Library(models.Model):
    LibraryType = (
        ('RNASeq', 'RNASeq'),
        ('liWGS', 'liWGS'),
        ('siWGS', 'siWGS'),
        ('matepair', 'matepair'),
        ('PCRSeq', 'PCRSeq'),
    )


    # plate setup
    unique_id = models.CharField(max_length=100, null=True, blank=True)
    gtc_code = models.CharField(max_length=100, null=True, blank=True)
    library_type = models.CharField(max_length=100, choices=LibraryType, null=True, blank=True)
    plate_name = models.CharField(max_length=100, null=True, blank=True)
    well = models.CharField(max_length=100, null=True, blank=True)
    parent_name = models.ForeignKey('sample.Sample', on_delete=models.PROTECT, null=True, blank=True, verbose_name='sample_name') #links to sample
    name = models.CharField(max_length=100, verbose_name='library_name')
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
    tapestation_conc_ng_uL = models.FloatField(null=True, blank=True)
    tapestation_molarity_nM = models.FloatField(null=True, blank=True)
    qpcr_conc_molarity_nM = models.FloatField(null=True, blank=True)
    qubit_conc_ng_uL = models.FloatField(null=True, blank=True)
    qc_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return (str(self.plate_name) + '_' + str(self.name) + '_' + str(self.parent_name))

    def save(self, *args, **kwargs):
        super(Library, self).save(*args, **kwargs)
        if not self.unique_id:
            t = datetime.date.today()
            print(datetime.date.today())
            self.created = t
            pk_red = self.pk % 10000
            self.unique_id = self.name + "_" + t.strftime("%Y%m%d") + '_' + "{0:0=4d}".format(pk_red)
            self.save()



class Pool(models.Model):
    unique_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    tapestation_size_bp = models.IntegerField(null=True, blank=True)
    tapestation_conc = models.FloatField(null=True, blank=True)
    tapestation_molarity_nM = models.FloatField(null=True, blank=True)
    qpcr_conc = models.FloatField(null=True, blank=True)
    qubit_conc = models.FloatField(null=True, blank=True)
    made_date = models.FloatField(default=0, null=True, blank=True)
    made_by = models.CharField(max_length=100, null=True, blank=True)
    pool_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return(self.name)

    def save(self, *args, **kwargs):
        super(Pool, self).save(*args, **kwargs)
        if not self.unique_id:
            t = datetime.date.today()
            print(datetime.date.today())
            self.created = t
            pk_red = self.pk % 10000
            self.unique_id = self.name + "_" + t.strftime("%Y%m%d") + '_' + "{0:0=4d}".format(pk_red)
            self.save()



class PoolingAmount(models.Model): # integrates pools and amount of each library used
    pool_name = models.ForeignKey(Pool, on_delete=models.CASCADE, null=True, blank=True) #links to pool
    library_name = models.ForeignKey(Library, on_delete=models.PROTECT, null=True, blank=True) #links to library
    name = models.CharField(max_length=100, verbose_name='pooled_lib_name', null=True, blank=True)
    rel_proportion = models.CharField(max_length=100, null=True, blank=True)
    amount_of_library_used = models.FloatField(default=0, null=True, blank=True)
    library_amount = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return(str(self.pool_name) + '_' + str(self.library_name))

    # def save(self, *args, **kwargs):
    #     super(PoolingAmount, self).save(*args, **kwargs)
    #     if not self.unique_id:
    #         t = datetime.date.today()
    #         print(datetime.date.today())
    #         self.created = t
    #         pk_red = self.pk % 10000
    #         self.unique_id = self.name + "_" + t.strftime("%Y%m%d") + '_' + "{0:0=4d}".format(pk_red)
    #         self.save()