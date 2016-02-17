# CMS for Meinberlin Project

## Requires

*   python 3.x (+ virtualenv + pip)


## How to start

1.  clone repository
2.  `cd meinberlin_wagtail`
3.  create virtualenv (make sure to add virtualenv name to .gitignore)
4.  run `pip install -r requirements.txt`
5.  run `python manage.py migrate`
6.  run `python manage.py createsuperuser`
7.  run `python manage.py runserver`
8.  Browse to <http://localhost:8000/admin>
