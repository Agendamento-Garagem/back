from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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
        duracao = 2
        if(int(self.start_time.minute) == 0):
            return f'<p> {self.start_time.hour}h00 - {self.start_time.hour + 2}h00<p>'
        else:
            return f'<p> {self.start_time.hour}h{self.start_time.minute} - {self.start_time.hour + 2}h{self.start_time.minute}<p>'
    
    @property
    def get_hour(self):
        return self.start_time.hour

