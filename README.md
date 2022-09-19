# Agendamento-Garagem
tutorial 1: (https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html)<br> tutorial 2: [here](https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html)

# Setando o ambiente
Clone repo, setup virtualenv, install Django
```
git clone https://github.com/Agendamento-Garagem/django-calendar.git
cd django-calendar

virtualenv env
source env/bin/activate
pip3 install django

python3 manage.py migrate
python3 manage.py runserver
```
local: http://localhost:8000/calendar/!
