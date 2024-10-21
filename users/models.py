from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def email_validator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('Email invalid, only @esprit.tn domain is allowed')

class participant(AbstractUser):
    cin_validator=RegexValidator(regex=r'^\d{8}$',message="This field must contain 8 digits")
    cin=models.CharField(primary_key=True,max_length=8,validators=[cin_validator])
    email=models.EmailField(unique=True,max_length=255,validators=[email_validator])
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(unique=True,max_length=255)
    USERNAME_FIELD='username'
    CHOICES=(
        ('etudiant','etudiant'),
        ('chercheur','chercheur'),
        ('docteur','docteur'),
        ('enseignant','enseignant'),
    )
    participant_category=models.CharField(max_length=255,choices=CHOICES)
    reservations=models.ManyToManyField(conference,through='reservation',related_name='reservations')
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural="participants"

class reservation(models.Model):
    conference=models.ForeignKey(conference,on_delete=models.CASCADE)
    participant=models.ForeignKey(participant,on_delete=models.CASCADE)
    confirmed=models.BooleanField(default=False)
    reservation_date=models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.conference.start_date < timezone.now().date():
            raise ValidationError('you can only reserve for upcoming conference')
        reservation_count=reservation.objects.filter(participant=self.participant,reservation_date__date=timezone.now()).count()
        if reservation_count>=3 :
            raise ValidationError("You can only make up to 3 reservation per a day")

    class Meta:
        unique_together=('conference','participant')
        verbose_name_plural="reservations"