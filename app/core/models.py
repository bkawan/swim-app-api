from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from django.conf import settings
from django.utils.safestring import mark_safe


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
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


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
    current_club = models.CharField(max_length=100, null=True,blank=True)
    current_coach = models.CharField(max_length=100, null=True,blank=True)



    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)

    age = property(age)

    def thumbnail(self):
        return mark_safe(u'<img height="30px" width="30px" src="%s" />'
                         % self.image.url)

    thumbnail.short_description = 'Photo'
    thumbnail.allow_tags = True

    def __str__(self):
        return self.user.name


class Game(models.Model):
    """
    Game models i.e swimming event
    """
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Competition(models.Model):
    freestyle_50 = models.DecimalField(max_digits=5,
                                       decimal_places=2, null=True)
    freestyle_100 = models.DecimalField(max_digits=5,
                                        decimal_places=2, null=True)
    freestyle_200 = models.DecimalField(max_digits=5,
                                        decimal_places=2, null=True)
    freestyle_400 = models.DecimalField(max_digits=5,
                                        decimal_places=2, null=True)
    freestyle_800 = models.DecimalField(max_digits=5,
                                        decimal_places=2, null=True)
    freestyle_1500 = models.DecimalField(max_digits=5,
                                         decimal_places=2, null=True)

    backstroke_50 = models.DecimalField(max_digits=5,
                                        decimal_places=2, null=True)
    backstroke_100 = models.DecimalField(max_digits=5,
                                         decimal_places=2, null=True)
    backstroke_200 = models.DecimalField(max_digits=5,
                                         decimal_places=2, null=True)

    breaststroke_50 = models.DecimalField(max_digits=5,
                                          decimal_places=2, null=True)
    breaststroke_100 = models.DecimalField(max_digits=5,
                                           decimal_places=2, null=True)
    breaststroke_200 = models.DecimalField(max_digits=5,
                                           decimal_places=2, null=True)

    butterfly_50 = models.DecimalField(max_digits=5,
                                       decimal_places=2, null=True)
    butterfly_100 = models.DecimalField(max_digits=5,
                                        decimal_places=2, null=True)
    butterfly_200 = models.DecimalField(max_digits=5,
                                        decimal_places=2, null=True)

    ind_Medley_200 = models.DecimalField(max_digits=5,
                                         decimal_places=2, null=True)
    ind_Medley_400 = models.DecimalField(max_digits=5,
                                         decimal_places=2, null=True)

    game = models.ForeignKey(Game, related_name='competitions',
                             on_delete=models.CASCADE)
    swimmer = models.ForeignKey(Swimmer, related_name='competitions',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.game.name


class Tag(models.Model):
    """Tag to be used for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
