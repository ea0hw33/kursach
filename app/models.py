from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        print('dfgwefgwerrwer')
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('department_head', 'Department Head'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    surename = models.CharField(max_length = 40, null=True)
    
    objects = MyAccountManager()
    
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Fakultety(models.Model):
    
    name = models.CharField(unique=True, max_length=100)
    
    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
    
    
class Kafedry(models.Model):
    
    name = models.CharField(unique=True, max_length=100)
    fakultet_name = models.ForeignKey(Fakultety, on_delete=models.CASCADE)
    zav = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self) -> str:
        return f'{self.name}|{self.fakultet_name}'

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'
    
    
class spetsialnosti(models.Model):
    
    name = models.CharField(unique=True, max_length=100)
    kafedra_name = models.ForeignKey(Kafedry, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    
class gruppy(models.Model):
    
    shifr = models.CharField(unique=True, max_length=100)
    spetsialnost = models.ForeignKey(spetsialnosti, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.shifr}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    
class studenty(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    num_zachetka = models.IntegerField(primary_key=True)
    gruppa = models.OneToOneField(gruppy, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} {self.user.surename}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
    
class sotrudnikyiOnKafedra(models.Model):
    
    jobs_choices = {
        ("te", "teacher"),
        ("as", "asperan")
    }
    
    degree_choices = {
        ("bk", "bakalavr"),
        ("mg", "magistr"),
        ("kn", "kandidat nauk"),
        ("dn", "doktor nauk")
    }
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    kafedra = models.ForeignKey(Kafedry, on_delete=models.CASCADE)
    job = models.CharField(choices=jobs_choices, max_length=3)
    degree = models.CharField(choices=degree_choices, max_length=3)
    
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} {self.user.surename}'

    class Meta:
        verbose_name = 'Сотрудник на кафедре'
        verbose_name_plural = 'Сотрудники на кафедре'
    
class NIR(models.Model):
    
    type_choices = {
        ("kf", "конференция"),
        ("ol", "олимпиада"),
        ("vs", "выставка")
    }
    
    name = models.CharField(unique=True, max_length=255)
    Fakultet = models.ForeignKey(Fakultety, on_delete=models.CASCADE)
    date_start = models.DateTimeField(null=True)
    type = models.CharField(choices=type_choices, max_length=3) 
    
    def get_absolute_url(self):
        return reverse("participateINNIR", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return f'{self.name}|{self.Fakultet}'

    class Meta:
        verbose_name = 'НИР'
        verbose_name_plural = 'НИРы'
    
    
    
class orgkomitety(models.Model):
    
    nir = models.ForeignKey(NIR, on_delete=models.CASCADE)
    user = models.ForeignKey(sotrudnikyiOnKafedra, 
                                            on_delete=models.CASCADE)
    isAgent = models.BooleanField(default=False)
    isParticipent = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.nir}|{self.user}'

    class Meta:
        verbose_name = 'Оргкомитет НИРа'
        verbose_name_plural = 'Огркомитеты НИРа'
    

class uchastnikyOnNIR(models.Model):
    
    user = models.ForeignKey(studenty, on_delete=models.CASCADE)
    nir = models.ForeignKey(NIR, on_delete=models.CASCADE)
    isParticipent = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.nir}|{self.user}'

    class Meta:
        verbose_name = 'Участник НИРа'
        verbose_name_plural = 'Участники НИРа'