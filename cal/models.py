from django.db import models
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    # end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_info', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    
    @property
    def get_html_time(self):
        if(self.start_time.minute == 0):
            return f'<p> {self.start_time.hour}h00 <p>'
        else:
            return f'<p> {self.start_time.hour}h{self.start_time.minute} <p>'
    
    @property
    def get_hour(self):
        return self.start_time.hour

CURSO_CHOICES = (
    ('d', 'Design'),
    ('c', 'Ciência da Computação')
)
    


class Usuario(models.Model):
    nome = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)
    curso = models.CharField(max_length=1, blank=True, null=False, choices=CURSO_CHOICES)
    matricula = models.IntegerField()
    telefone = models.IntegerField(default=0, verbose_name="Numero do telefone verboso")

