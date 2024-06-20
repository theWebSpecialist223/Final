from django.db import models

# Create your models here.



# Create your models here.
class Record(models.Model):
    class TypeChoices(models.TextChoices):
        DIESEL = 'Diesel', 'Diesel'
        PETROL = 'Petrol', 'Petrol'

    class SupplierChoices(models.TextChoices):
        REDAN = 'Redan', 'Redan'
        PETROTRADE = 'Petrotrade', 'Petrotrade'
    
    class PurposeChoices(models.TextChoices):
        CONDITION_OF_SERVICE = 'Condition of Service', 'Condition of Service'
        MONTHLY_ALLOCATION = 'Monthly Allocation', 'Monthly Allocation'

    creation_date = models.DateTimeField(auto_now_add=True)
    fuel_type = models.CharField(max_length=20, choices=TypeChoices.choices)
    serial_number_group = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField(null=True)
    #available = models.PositiveIntegerField(null = True)
    supplier = models.CharField(max_length=50, choices=SupplierChoices.choices)
    purpose = models.CharField(max_length=255, choices=PurposeChoices.choices, null=True)
    amount_for_one = models.IntegerField(null=True)
    amount_in_litres = models.IntegerField(null=True, editable=False)

    '''def coupons_available(self):
        #Calculation
        issued_monthly_coupons = IssuedMonthly.objects.filter(coupon_group=self.serial_number_group)
        service_issue_coupons = ServiceIssue.objects.filter(coupon_group=self.serial_number_group)

        if issued_monthly_coupons.exists():
            issued_monthly_quantity = sum(coupon.quantity for coupon in issued_monthly_coupons)
            available_coupons = self.quantity - issued_monthly_quantity
        elif service_issue_coupons.exists():
            service_issue_quantity = sum(coupon.number_of_coupons for coupon in service_issue_coupons)
            available_coupons = self.quantity - service_issue_quantity

        else:
            available_coupons = self.quantity
        
        return available_coupons
'''

                    

    class Meta:
        ordering = ['-creation_date']
    
    @property
    def amount_in_litres_value(self):
        return self.amount_for_one * self.quantity
        
    def save(self, *args, **kwargs):
        #self.available = self.coupons_available()
        self.amount_in_litres = self.amount_in_litres_value
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.serial_number_group + " " + self.fuel_type  


# receivers
class Recepient(models.Model):
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    monthly_allocation = models.IntegerField(null = True)
    allocation_due = models.IntegerField(null = True)

    def __str__(self):
        return self.last_name + " " + self.designation 

# Issuing Monthly Coupons
class IssuedMonthly(models.Model):
    issued_date = models.DateTimeField(auto_now_add=True)
    issued_to = models.ForeignKey(Recepient, on_delete=models.CASCADE, related_name="receiver")
    amount_issued = models.PositiveIntegerField()
    amount_owing = models.CharField(max_length=50)
    coupon_group = models.ForeignKey(Record, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null = True)

    def __str__(self):
        return self.issued_to + " " + self.amount_issued 
    
    @property
    def amount_in_litres_value(self):
        return self.quantity * 20
    
    def save(self, *args, **kwargs):
        self.amount_issued = self.amount_in_litres_value
        super().save(*args, **kwargs)
    

class ServiceIssue(models.Model):
    issued_date = models.DateTimeField(auto_now_add=True)
    issued_to = models.CharField(max_length=50)
    designation = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    reason = models.CharField(max_length=255)
    coupon_group = models.ForeignKey(Record, on_delete=models.CASCADE, null=True)
    number_of_coupons = models.PositiveIntegerField(null=True)
    amount_issued = models.PositiveIntegerField(null= True)

    def __str__(self):
        return self.issued_to + " " + self.amount_issued 

    @property
    def amount_in_litres_value(self):
        return self.number_of_coupons * 20
    
    def save(self, *args, **kwargs):
        self.amount_issued = self.amount_in_litres_value
        super().save(*args, **kwargs)


