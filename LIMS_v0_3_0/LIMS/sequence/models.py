from django.db import models

BOOL_CHOICES=((True, u"yes"),
              (False, u"no"))

class WUSSubmission(models.Model):
    wus_name = models.CharField(max_length=100, null=True, blank=True)
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
        return(self.wus_name)

class WUSPool(models.Model):
    wus_pool_name = models.CharField(max_length=100, null=True, blank=True)
    wus_name = models.ForeignKey(WUSSubmission, on_delete=models.CASCADE, null=True, blank=True)
    pool_name = models.ForeignKey('library.Pool', on_delete=models.PROTECT, null=True, blank=True)  # links to Pool
    num_of_lanes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(self.wuspool_name)

class WUSLaneResult(models.Model):
    lane_id = models.IntegerField(null=True, blank=True)
    wuspool_name = models.ForeignKey(WUSPool, on_delete=models.PROTECT, null=True, blank=True)
    library_name = models.ForeignKey('library.PoolingAmount', on_delete=models.PROTECT, null=True, blank=True)  #links to PoolingAmount
    lane_number = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=100, null=True, blank=True)
    counts = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(self.lane_id)

class WUSSampleResult(models.Model):
    sample_name = models.ForeignKey('sample.Sample', on_delete=models.PROTECT, null=True, blank=True)  #links to PoolingAmount
    counts = models.IntegerField(null=True, blank=True)
    complexity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(self.sample_name)