from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    pending = models.IntegerField(default=0)
    adm = models.CharField(max_length=200, default='')

    

    MEIA = 30
    UMA = 60
    UMA_MEIA = 90
    DUAS = 120

    DURATION = (
    (MEIA, '30 min'),
    (UMA, '1h'),
    (UMA_MEIA, '1h30min'),
    (DUAS, '2h')
  )

    duration = models.IntegerField(default=0, choices=DURATION)

    @property
    def get_confirmation(self):

        if self.pending == 0:
            return f'<span style="color: #C8BA08"> Pendente </span>'
        elif self.pending == 1:
            return f'<span style="color: lime"> Confirmado </span><span>({self.adm})</span>'
        elif self.pending == 2:
            return f'<span style="color: red"> Negado </span><span>({self.adm})</span>'

    @property
    def get_html_url(self):
        url = reverse('cal:event_info', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    
    @property
    def get_html_time(self):
        duracao = self.duration / 60
        hora = self.start_time.hour
        minuto = self.start_time.minute
        min_format = 0

        def zero(x):
            if(len(str(x))) == 1:
                x = f'0{x}'
            else:
                x = f'{x}'
            return x

        if duracao == 0.5:
            duracao_min = 30

            if(minuto + duracao_min >=60):
                duracao_min = duracao_min - 60
                min_format = minuto + duracao_min
                min_format = zero(min_format)

                if(len(str(minuto))) == 1:
                    return f'<p> {hora}h0{minuto} - {hora + 1}h{min_format}<p>'
                else:
                    return f'<p> {hora}h{minuto} - {hora + 1}h{min_format}<p>'
            else:
                min_format = minuto + duracao_min
                min_format = zero(min_format)

                if(len(str(minuto))) == 1: 
                    return f'<p> {hora}h0{minuto} - {hora}h{min_format}<p>'
                else:
                    return f'<p> {hora}h{minuto} - {hora}h{min_format}<p>'
                    

        elif duracao == 1:
            duracao = int(duracao)
            return f'<p> {hora}h{minuto} - {hora + duracao}h{minuto}<p>'

        elif duracao == 1.5:
            duracao_min = 30

            if(minuto + duracao_min >=60):
                duracao_min = duracao_min - 60
                min_format = minuto + duracao_min
                min_format = zero(min_format)

                if(len(str(minuto))) == 1:
                    return f'<p> {hora}h0{minuto} - {hora + 2}h{min_format}<p>'
                else:
                    return f'<p> {hora}h{minuto} - {hora + 2}h{min_format}<p>'
            else:
                min_format = minuto + duracao_min
                min_format = zero(min_format)

                if(len(str(minuto))) == 1:      
                    return f'<p> {hora}h0{minuto} - {hora + 1}h{min_format}<p>'
                else:
                    return f'<p> {hora}h{minuto} - {hora + 1}h{min_format}<p>'

        elif duracao == 2:
            duracao = int(duracao)
            return f'<p> {hora}h{minuto} - {hora + duracao}h{minuto}<p>'
        
            
    @property
    def get_hour(self):
        return self.start_time.hour

