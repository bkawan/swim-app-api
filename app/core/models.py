from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user models that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Swimmer(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    user = models.OneToOneField(User, related_name='swimmer',
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=25,
                              choices=GENDER_CHOICES,
                              default='Male')
    city_of_birth = models.CharField(max_length=255, null=True)
    school = models.CharField(max_length=255, null=True)
    phone_no = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    fathers_name = models.CharField(max_length=255, null=True)
    mothers_name = models.CharField(max_length=255, null=True)
    height_in_cm = models.IntegerField(default=0)
    weight_in_pound = models.IntegerField(default=0)
    rest_heart_rate = models.CharField(max_length=10, null=True)
    max_heart_rate = models.CharField(max_length=10, null=True)
    distance = models.CharField(max_length=10, null=True)
    stroke_rate = models.IntegerField(null=True)
    main_stroke = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='', null=True)


class Game(models.Model):
    """
    Game models i.e swimming event
    """
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()


class Competition(models.Model):
    TYPE_CHOICE = (
        ('Freestyle_50', 'Freestyle_50'),
        ('Freestyle_100', 'Freestyle_100'),
        ('Freestyle_200', 'Freestyle_200'),
        ('Freestyle_400', 'Freestyle_400'),
        ('Freestyle_800', 'Freestyle_800'),
        ('Freestyle_1500', 'Freestyle_1500'),

        ('Backstroke_50', 'Backstroke_50'),
        ('Backstroke_100', 'Backstroke_100'),
        ('Backstroke_200', 'Backstroke_200'),

        ('Breaststroke_50', 'Breaststroke_50'),
        ('Breaststroke_100', 'Breaststroke_100'),
        ('Breaststroke_200', 'Breaststroke_200'),

        ('Butterfly_50', 'Butterfly_50'),
        ('Butterfly_100', 'Butterfly_100'),
        ('Butterfly_200', 'Butterfly_200'),

        ('IndMedley200', 'IndMedley200'),
        ('IndMedley400', 'IndMedley400')
    )

    game = models.ForeignKey(Game, related_name='competitions',
                             on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=TYPE_CHOICE)
    swimmers = models.ManyToManyField(Swimmer, related_name='competitions')


class Tag(models.Model):
    """Tag to be used for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
