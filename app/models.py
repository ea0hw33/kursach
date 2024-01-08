from django.db import models
from django.urls import reverse



class Fakultety(models.Model):
    
    name = models.CharField(unique=True, max_length=100)
    
    
class Kafedry(models.Model):
    
    name = models.CharField(unique=True, max_length=100)
    fakultet_name = models.ForeignKey(Fakultety, on_delete=models.CASCADE)
    zav_name = models.CharField(max_length=100)
    zav_secname = models.CharField(max_length=100)
    zav_surename = models.CharField(max_length=100, null=True)
    
    
class spetsialnosti(models.Model):
    
    name = models.CharField(unique=True, max_length=100)
    kafedra_name = models.ForeignKey(Kafedry, on_delete=models.CASCADE)
   
    
class gruppy(models.Model):
    
    shifr = models.CharField(unique=True, max_length=100)
    spetsialnost = models.ForeignKey(spetsialnosti, on_delete=models.CASCADE)
    
class studenty(models.Model):
    
    num_zachetka = models.IntegerField(primary_key=True)
    gruppa = models.OneToOneField(gruppy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    secname = models.CharField(max_length=100)
    surename = models.CharField(max_length=100, null=True)
    
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
    
    kafedra = models.ForeignKey(Kafedry, on_delete=models.CASCADE)
    job = models.CharField(choices=jobs_choices, max_length=3)
    name = models.CharField(max_length=100)
    secname = models.CharField(max_length=100)
    surename = models.CharField(max_length=100, null=True)
    degree = models.CharField(choices=degree_choices, max_length=3)
    
class NIR(models.Model):
    
    type_choices = {
        ("kf", "konferensia"),
        ("ol", "olimpiada"),
        ("vs", "vistavka")
    }
    
    name = models.CharField(unique=True, max_length=255)
    Fakultet = models.ForeignKey(Fakultety, on_delete=models.CASCADE)
    date_start = models.DateTimeField(null=True)
    type = models.CharField(choices=type_choices, max_length=3) 
    
    def get_absolute_url(self):
        return reverse("participateINNIR", kwargs={"pk": self.pk})
    
    
    
class orgkomitety(models.Model):
    
    nir = models.ForeignKey(NIR, on_delete=models.CASCADE)
    sotrudnik = models.ForeignKey(sotrudnikyiOnKafedra, 
                                            on_delete=models.CASCADE)
    isAgent = models.BooleanField(default=False)
    isParticipent = models.BooleanField(default=False)
    

class uchastnikyOnNIR(models.Model):
    
    student = models.ForeignKey(studenty, on_delete=models.CASCADE)
    nir = models.ForeignKey(NIR, on_delete=models.CASCADE)
    isParticipent = models.BooleanField(default=False)

    