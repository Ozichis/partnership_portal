from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime, django
import django.contrib.humanize
from dateutil.relativedelta import relativedelta
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'church'),
        (2, 'individual'),
        (3, 'admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    main_target = models.IntegerField(null=True)
    church_name = models.CharField(max_length=500, null=True, blank=True)
    current_church = models.ForeignKey('Church', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super(User, self).save(*args, **kwargs)
        if self.user_type ==1:
            if Church.objects.filter(userinfo=self).exists():
                person = Church.objects.get(userinfo=self)
                person.church_name=self.church_name
                person.main_target=self.main_target
                person.save()
            else:
                Church.objects.create(userinfo=self, church_name=self.church_name, main_target=self.main_target)
        if self.user_type == 2:
            if Individual.objects.filter(user=self):
                person = Individual.objects.get(user=self)
                person.name=f"{self.first_name} {self.last_name}"
                person.main_target=self.main_target
                person.church=self.current_church
                person.save()
            else:
                Individual.objects.create(user=self, name=f"{self.first_name} {self.last_name}", main_target=self.main_target, church=self.current_church)
        

class Church(models.Model):
    userinfo = models.ForeignKey(User, on_delete=models.CASCADE)
    church_name = models.CharField(max_length=255, null=True)
    main_target = models.IntegerField(null=True)


    def __str__(self):
        return self.church_name

class Individual(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    main_target = models.IntegerField(null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class PatnershipArm(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Patnership(models.Model):
    arm = models.ForeignKey(PatnershipArm, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    owner = models.ForeignKey(Individual, on_delete=models.CASCADE)
    date_payed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{format(self.amount, 'd')} given by {self.owner.name}"

    def contrib(self):
        target = self.owner.main_target
        cont = round((self.amount / target ) * 100)
        return str(cont) + "%"

    def contrib_church(self):
        target = self.owner.church.main_target
        cont = round((self.amount / target ) * 100)
        return str(cont) + "%"


class TargetIndividual(models.Model):
    arm = models.ForeignKey(PatnershipArm, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=False)
    owner = models.ForeignKey(Individual, on_delete=models.CASCADE)
    is_frequent = models.BooleanField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    CHOICES = (
        (1, "monthly"),
        (2, "yearly"),
        (3, "quarterly"),
    )
    frequency = models.PositiveIntegerField(choices=CHOICES, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    passed_time = models.BooleanField(default=False)

    def get_completion(self):
        result = {}
        all_targets = TargetIndividual.objects.filter(owner=self.owner, arm=None, is_active=True).order_by('created_at')
        all_partnerships = Patnership.objects.filter(owner=self.owner)
        sum_of_partnership = 0
        for partnership in all_partnerships:
            sum_of_partnership += partnership.amount

        
        for target in all_targets:
            if sum_of_partnership > 0:
                if not target.arm:
                    if sum_of_partnership > target.amount:
                        result[target.id] = [100, False]
                        sum_of_partnership -= target.amount
                    elif sum_of_partnership == target.amount:
                        result[target.id] = [100, False]
                        sum_of_partnership = 0
                    else:
                        if target.end_date < django.utils.timezone.now():
                            if target.is_frequent:
                                self.start_date = django.utils.timezone.now()
                                if self.frequency == 1:
                                    self.end_date = self.start_date + relativedelta(months=1)
                                if self.frequency == 2:
                                    self.end_date = self.start_date + relativedelta(years=1)
                                if self.frequency == 3:
                                    self.end_date = self.start_date + relativedelta(months=3)
                                result[target.id] = [round((sum_of_partnership / target.amount) * 100), False]
                            else:
                                target.passed_time = True
                                target.save()
                                result[target.id] = [round((sum_of_partnership / target.amount) * 100), True] 
                              
                        result[target.id] = [round((sum_of_partnership / target.amount) * 100), False]
                        sum_of_partnership = 0
            else:
                break
        
        for arm in PatnershipArm.objects.all():
                all_targets = TargetIndividual.objects.filter(arm=arm, is_active=True)
                all_partnerships = Patnership.objects.filter(arm=arm)
                sum_ = 0
                for partnership in all_partnerships:
                    sum_ += partnership.amount
                for target in all_targets:
                    if sum_ > 0:
                        if sum_ > target.amount:
                            result[target.id] = [100, False]
                            sum_ -= target.amount
                        elif sum_ == target.amount:
                            result[target.id] = [100, False]
                            sum_ = 0
                        else:
                            if target.end_date < django.utils.timezone.now():
                                if target.is_frequent:
                                    self.start_date = django.utils.timezone.now()
                                    if self.frequency == 1:
                                        self.end_date = self.start_date + relativedelta(months=1)
                                    if self.frequency == 2:
                                        self.end_date = self.start_date + relativedelta(years=1)
                                    if self.frequency == 3:
                                        self.end_date = self.start_date + relativedelta(months=3)
                                    result[target.id] = [round((sum_ / target.amount) * 100), False]
                                else:
                                    target.passed_time = True
                                    target.save()
                                    result[target.id] = [round((sum_ / target.amount) * 100), True]
                            else:
                                result[target.id] = [round((sum_ / target.amount) * 100), False]
                            sum_ = 0
                    elif sum_ == 0:
                        if target.end_date < django.utils.timezone.now():
                            if target.is_frequent:
                                self.start_date = django.utils.timezone.now()
                                if self.frequency == 1:
                                    self.end_date = self.start_date + relativedelta(months=1)
                                if self.frequency == 2:
                                    self.end_date = self.start_date + relativedelta(years=1)
                                if self.frequency == 3:
                                    self.end_date = self.start_date + relativedelta(months=3)
                                result[target.id] = [0, False]
                            else:
                                target.passed_time = True
                                target.save()
                                result[target.id] = [0, True]
                        else:
                            result[target.id] = [0, False]
        return result

    def curr_completion(self):
        completion = self.get_completion()
        ans = [0, True]
        for key, value in completion.items():
            if self.id == key:
                ans = value
                break
        return ans[0], ans[1]

    def save(self, *args, **kwargs):
        if self.is_frequent:
            self.start_date = django.utils.timezone.now()
            if self.frequency == 1:
                self.end_date = self.start_date + relativedelta(months=1)
            if self.frequency == 2:
                self.end_date = self.start_date + relativedelta(years=1)
            if self.frequency == 3:
                self.end_date = self.start_date + relativedelta(months=3)
        else:
            self.frequency = None
        super(TargetIndividual, self).save(*args, **kwargs)


class TargetChurch(models.Model):
    arm = models.ForeignKey(PatnershipArm, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(null=False)
    owner = models.ForeignKey(Church, on_delete=models.CASCADE)
    is_frequent = models.BooleanField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    CHOICES = (
        (1, "monthly"),
        (2, "yearly"),
        (3, "quarterly"),
    )
    frequency = models.PositiveIntegerField(choices=CHOICES, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    passed_time = models.BooleanField(default=False)
    
    def get_completion(self):
        result = {}
        all_targets = TargetChurch.objects.filter(owner=self.owner, arm=None, is_active=True).order_by('created_at')
        all_partnerships = Patnership.objects.filter(owner__church=self.owner)
        sum_of_partnership = 0
        for partnership in all_partnerships:
            sum_of_partnership += partnership.amount
        
        for target in all_targets:
            if sum_of_partnership > 0:
                if not target.arm:
                    if sum_of_partnership > target.amount:
                        result[target.id] = [100, False]
                        sum_of_partnership -= target.amount
                    elif sum_of_partnership == target.amount:
                        result[target.id] = [100, False]
                        sum_of_partnership = 0
                    else:
                        if target.end_date < django.utils.timezone.now():
                            if target.is_frequent:
                                self.start_date = django.utils.timezone.now()
                                if self.frequency == 1:
                                    self.end_date = self.start_date + relativedelta(months=1)
                                if self.frequency == 2:
                                    self.end_date = self.start_date + relativedelta(years=1)
                                if self.frequency == 3:
                                    self.end_date = self.start_date + relativedelta(months=3)
                                result[target.id] = [round((sum_of_partnership / target.amount) * 100), False]
                            else:
                                target.passed_time = True
                                target.save()
                                result[target.id] = [round((sum_of_partnership / target.amount) * 100), True] 
                              
                        result[target.id] = [round((sum_of_partnership / target.amount) * 100), False]
                        sum_of_partnership = 0
            else:
                break
        
        for arm in PatnershipArm.objects.all():
                all_targets = TargetChurch.objects.filter(arm=arm, is_active=True, owner=self.owner)
                all_partnerships = Patnership.objects.filter(arm=arm, owner__church=self.owner)
                sum_ = 0
                for partnership in all_partnerships:
                    sum_ += partnership.amount
                print(sum_)
                for target in all_targets:
                    if sum_ > 0:
                        if sum_ > target.amount:
                            result[target.id] = [100, False]
                            sum_ -= target.amount
                        elif sum_ == target.amount:
                            result[target.id] = [100, False]
                            sum_ = 0
                        else:
                            if target.end_date < django.utils.timezone.now():
                                if target.is_frequent:
                                    self.start_date = django.utils.timezone.now()
                                    if self.frequency == 1:
                                        self.end_date = self.start_date + relativedelta(months=1)
                                    if self.frequency == 2:
                                        self.end_date = self.start_date + relativedelta(years=1)
                                    if self.frequency == 3:
                                        self.end_date = self.start_date + relativedelta(months=3)
                                    result[target.id] = [round((sum_ / target.amount) * 100), False]
                                else:
                                    target.passed_time = True
                                    target.save()
                                    result[target.id] = [round((sum_ / target.amount) * 100), True]
                            else:
                                result[target.id] = [round((sum_ / target.amount) * 100), False]
                            sum_ = 0
                    elif sum_ == 0:
                        if target.end_date < django.utils.timezone.now():
                            if target.is_frequent:
                                self.start_date = django.utils.timezone.now()
                                if self.frequency == 1:
                                    self.end_date = self.start_date + relativedelta(months=1)
                                if self.frequency == 2:
                                    self.end_date = self.start_date + relativedelta(years=1)
                                if self.frequency == 3:
                                    self.end_date = self.start_date + relativedelta(months=3)
                                result[target.id] = [0, False]
                            else:
                                target.passed_time = True
                                target.save()
                                result[target.id] = [0, True]
                        else:
                            result[target.id] = [0, False]
        print(result)
        return result

    def curr_completion(self):
        completion = self.get_completion()
        ans = [0, True]
        for key, value in completion.items():
            if self.id == key:
                ans = value
                break
        return ans[0], ans[1]

    def save(self, *args, **kwargs):
        if self.is_frequent:
            self.start_date = django.utils.timezone.now()
            if self.frequency == 1:
                self.end_date = self.start_date + relativedelta(months=1)
            if self.frequency == 2:
                self.end_date = self.start_date + relativedelta(years=1)
            if self.frequency == 3:
                self.end_date = self.start_date + relativedelta(months=3)
        else:
            self.frequency = None
        super(TargetChurch, self).save(*args, **kwargs)