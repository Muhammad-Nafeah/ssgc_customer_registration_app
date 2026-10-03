from django.db import models


class CustomerRegistration(models.Model):

    # --- Identity ---
    UR_CONSUMER_S_NO = models.IntegerField(null=True, blank=True, editable=False)
    CLAIM_ID = models.CharField(max_length=19, primary_key=True)    
    CNIC = models.CharField(max_length=15)
    NAME_PREFIX = models.CharField(max_length=15, null=True, blank=True)
    FULL_NAME = models.CharField(max_length=80)
    PHONE_NUMBER = models.CharField(max_length=20, null=True, blank=True)

    # --- Address ---
    ADDRESS1 = models.CharField(max_length=120, null=True, blank=True)
    ADDRESS2 = models.CharField(max_length=120, null=True, blank=True)
    ADDRESS3 = models.CharField(max_length=120, null=True, blank=True)
    ADDRESS4 = models.CharField(max_length=120, null=True, blank=True)
    CITY = models.CharField(max_length=50, null=True, blank=True)

    # --- Organization ---
    UNIT = models.CharField(max_length=32)
    ZONE_NAME = models.CharField(max_length=50)
    SUB_ZONE = models.CharField(max_length=50)
    REGION = models.CharField(max_length=32)
    AREA_CD = models.CharField(max_length=4, null=True, blank=True)
    BILLING_GRP = models.CharField(max_length=4, null=True, blank=True)
    AMG = models.CharField(max_length=50, null=True, blank=True)

        # --- Meter and billing ---
    NEAREST_METER_NBR = models.CharField(max_length=30, null=True, blank=True)
    BULK_METER_NO = models.CharField(max_length=25, null=True, blank=True)
    SWITCHH = models.CharField(max_length=12, null=True, blank=True)
    LAST_BM = models.CharField(max_length=6, null=True, blank=True)
    OVR_VOLUME = models.IntegerField(null=True, blank=True)
    OVR_RATE_AMT = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PREM_ID = models.CharField(max_length=20, null=True, blank=True)
    SP_ID = models.CharField(max_length=255, null=True, blank=True)

    # --- Category and location ---
    CATEGORY_CD = models.CharField(max_length=10, null=True, blank=True)
    CATEGORY_DESCR = models.CharField(max_length=50, null=True, blank=True)
    LOCATION_ID = models.CharField(max_length=20, null=True, blank=True)
    LOCATION_DESCR = models.CharField(max_length=100, null=True, blank=True)
    X_LONGITUDE = models.CharField(max_length=25, null=True, blank=True)
    Y_LATITUDE = models.CharField(max_length=25, null=True, blank=True)

        # --- Committee and case ---
    COMMITTE_VISIT_DATE = models.DateField(null=True, blank=True)
    COMMITTE_APPROVED_DATE = models.DateField(null=True, blank=True)
    COMMITTE_REMARKS = models.CharField(max_length=100, null=True, blank=True)
    CASE_STATUS = models.CharField(max_length=15, null=True, blank=True)
    UR_CONSUMER_STATUS_FLG = models.CharField(max_length=50, null=True, blank=True)

    # --- Audit ---
    SETUP_DT = models.DateField(null=True, blank=True)
    USERID = models.CharField(max_length=50)
    LAST_UPDATED_DT = models.DateField(null=True, blank=True)

    class Meta:
        managed = False #means "the table already exists, don't create or change it."
        db_table = 'customer_registration' #means "use exactly this table name."
