from django.db import models

import datetime

BOOL_CHOICES=((True, u"yes"),
              (False, u"no"))

class WUSSubmission(models.Model):
    unique_id = models.CharField(max_length=100, null=True, blank=True)
    wus_name = models.CharField(max_length=100, null=True, blank=True)
    batch_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='wus name')
    num_of_pools = models.IntegerField(null=True, blank=True)
    illumina_chemistry_ends = models.CharField(max_length=100, null=True, blank=True)
    illumina_chemistry_length = models.IntegerField(null=True, blank=True)
    dual_barcode = models.BooleanField(choices=BOOL_CHOICES, null=True, blank=True)
    barcode_size_bp = models.IntegerField(null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    quote_number = models.CharField(max_length=100, null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    submitted_by = models.CharField(max_length=100, null=True, blank=True)
    broad_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return(self.batch_id)

    def save(self, *args, **kwargs):
        super(WUSSubmission, self).save(*args, **kwargs)
        if not self.unique_id:
            t = datetime.date.today()
            print(datetime.date.today())
            self.created = t
            pk_red = self.pk % 10000
            self.unique_id = self.batch_id
            self.save()

class WUSPool(models.Model):
    unique_id = models.CharField(max_length=100, null=True, blank=True)
    parent_name = models.ForeignKey(WUSSubmission, on_delete=models.CASCADE, null=True, blank=True, verbose_name='WUS Name')
    related_name = models.ForeignKey('library.Pool', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Pool Name')  # links to Pool
    num_of_lanes = models.FloatField(default=0)

    def __str__(self):
        return(str(self.parent_name) + '_' + str(self.related_name))

    def save(self, *args, **kwargs):
        super(WUSPool, self).save(*args, **kwargs)
        if not self.unique_id:
            t = datetime.date.today()
            print(datetime.date.today())
            self.created = t
            pk_red = self.pk % 10000
            self.unique_id = str(self.parent_name) + '_' + str(self.related_name)
            self.save()

class WUSResult(models.Model):
    unique_id = models.CharField(max_length=100, null=True, blank=True)
    parent_name = models.ForeignKey(WUSPool, on_delete=models.PROTECT, null=True, blank=True, verbose_name='WUS Pool Name')
    related_name = models.ForeignKey('library.Library', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Library Name')  #links to PoolingAmount
    lane_number = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=100, null=True, blank=True)
    broad_id = models.CharField(max_length=100, null=True, blank=True)
    read = models.CharField(max_length=100, null=True, blank=True)
    fastq_name = models.CharField(max_length=100, null=True, blank=True)
    counts = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(str(self.parent_name) + '_' + str(self.related_name))

    def save(self, *args, **kwargs):
        super(WUSResult, self).save(*args, **kwargs)
        if not self.unique_id:
            self.unique_id = str(self.lane_number) + '_' + str(self.broad_id) + '.' +  str(self.lane_number) + '.' + \
                             str(self.barcode) + '.' + str(self.read)
            self.save()

class WUSSampleResult(models.Model):
    sample_name = models.ForeignKey('sample.Sample', on_delete=models.PROTECT, null=True, blank=True)  #links to PoolingAmount
    counts = models.IntegerField(null=True, blank=True)
    complexity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(self.sample_name)