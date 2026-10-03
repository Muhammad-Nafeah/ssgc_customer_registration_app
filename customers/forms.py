import re
from django import forms
from .models import CustomerRegistration


class CustomerForm(forms.ModelForm):
    #Each entry is (title, icon, [field names])
    SECTIONS = [
        ('Identity', 'bi-person-badge',
         ['CLAIM_ID', 'CNIC', 'NAME_PREFIX', 'FULL_NAME', 'PHONE_NUMBER']),
        ('Address', 'bi-geo-alt',
         ['ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'ADDRESS4', 'CITY']),
        ('Organization', 'bi-diagram-3',
         ['UNIT', 'ZONE_NAME', 'SUB_ZONE', 'REGION', 'AREA_CD', 'BILLING_GRP', 'AMG']),
        ('Meter and Billing', 'bi-speedometer2',
         ['NEAREST_METER_NBR', 'BULK_METER_NO', 'SWITCHH', 'LAST_BM',
          'OVR_VOLUME', 'OVR_RATE_AMT', 'PREM_ID', 'SP_ID']),
        ('Category and Location', 'bi-pin-map',
         ['CATEGORY_CD', 'CATEGORY_DESCR', 'LOCATION_ID', 'LOCATION_DESCR',
          'X_LONGITUDE', 'Y_LATITUDE']),
        ('Committee and Case', 'bi-clipboard-check',
         ['COMMITTE_VISIT_DATE', 'COMMITTE_APPROVED_DATE', 'COMMITTE_REMARKS',
          'CASE_STATUS', 'UR_CONSUMER_STATUS_FLG']),
        ('Audit', 'bi-clock-history',
         ['SETUP_DT', 'USERID', 'LAST_UPDATED_DT']),
    ]

    class Meta:
        model = CustomerRegistration
        exclude = ['UR_CONSUMER_S_NO']
        widgets = {
            'SETUP_DT': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'LAST_UPDATED_DT': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'COMMITTE_VISIT_DATE': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'COMMITTE_APPROVED_DATE': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if self.instance.pk:
                self.fields['CLAIM_ID'].disabled = True

    @property
    def sections(self):
        return [
            {'title': title, 'icon': icon, 'fields': [self[name] for name in names]}
            for title, icon, names in self.SECTIONS
        ]

    def clean_CNIC(self):
        cnic = self.cleaned_data['CNIC']
        if not re.fullmatch(r'\d{5}-\d{7}-\d', cnic):
            raise forms.ValidationError('CNIC must look like 42101-1234567-1')
        return cnic

    def clean_PHONE_NUMBER(self):
        phone = self.cleaned_data.get('PHONE_NUMBER')
        if phone and not re.fullmatch(r'[0-9+\-\s]{7,20}', phone):
            raise forms.ValidationError('Phone may contain only digits, +, - and spaces')
        return phone