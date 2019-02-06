from django.db import models

BOOL_CHOICES=((True, u"yes"),
              (False, u"no"))

class WUSSubmission(models.Model):
    wus_name = models.CharField(max_length=100, null=True, blank=True)
    pool_name = models.ForeignKey('library.Pool', on_delete=models.PROTECT, null=True, blank=True)  # links to Pool
    illumina_chemistry_ends = models.CharField(max_length=100, null=True, blank=True)
    illumina_chemistry_length = models.IntegerField(null=True, blank=True)
    dual_barcode = models.BooleanField(choices=BOOL_CHOICES, null=True, blank=True)
    barcode_size_bp = models.IntegerField(null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    requested_number_of_lanes = models.IntegerField(null=True, blank=True)
    quote_number = models.CharField(max_length=100, null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    submitted_by = models.CharField(max_length=100, null=True, blank=True)
    broad_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return(self.walk_up_submission_name)

class WUSResult(models.Model):
    library_name = models.ForeignKey('library.PoolingAmount', on_delete=models.PROTECT, null=True, blank=True)  #links to PoolingAmount
    lane_id = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=100, null=True, blank=True)
    counts = models.IntegerField(null=True, blank=True)
    illumina_chemistry_ends = models.CharField(max_length=100, null=True, blank=True)
    illumina_chemistry_length = models.IntegerField(null=True, blank=True)
    dual_barcode = models.BooleanField(choices=BOOL_CHOICES, null=True, blank=True)
    barcode_size_bp = models.IntegerField(null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    requested_number_of_lanes = models.IntegerField(null=True, blank=True)
    quote_number = models.CharField(max_length=100, null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    submitted_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return(self.library_name)

walk_up_submission = models.ForeignKey('library.PoolingAmount', on_delete=models.PROTECT, null=True, blank=True) #links to PoolingAmoun