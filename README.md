<a href="https://ru.hexlet.io/">
<p align="center">
    <img src="images/hexlet_logo.png" 
        width="200" 
        height="200">
</p>
</a>


### Hexlet tests and linter status:
[![Actions Status](https://github.com/Alex-Iset/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Alex-Iset/python-project-52/actions)
[![my-check](https://github.com/Alex-Iset/python-project-52/actions/workflows/my-check.yml/badge.svg)](https://github.com/Alex-Iset/python-project-52/actions/workflows/my-check.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Alex-Iset_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Alex-Iset_python-project-52)

## Tech Stack:
![Static Badge](https://img.shields.io/badge/django-5.2.4-F?logo=django&color=%23126e41)
![Static Badge](https://img.shields.io/badge/dj_database_url-3.0.1-F?color=%23126e41)
![Static Badge](https://img.shields.io/badge/django_filter-25.1-F?color=%23126e41)
![Static Badge](https://img.shields.io/badge/rollbar-25.1-F?logo=rollbar&color=%23597afa)
<br>
![Static Badge](https://img.shields.io/badge/gunicorn-23.0.0-F?logo=gunicorn&color=%23329f5a)
![Static Badge](https://img.shields.io/badge/psycopg2-2.9.10-F?logo=psycopg&color=yellow)
![Static Badge](https://img.shields.io/badge/dotenv-0.9.9-F?logo=dotenv&color=yellow)
![Static Badge](https://img.shields.io/badge/whitenoise-6.9.0-F?logo=whitenoise&color=white)


## Table of contents:
### [1. «Task Manager»](#task-manager)
### [2. Installing and launch](#installing-and-launch)

## «Task Manager»:
«Task Manager» - a task management system similar to http://www.redmine.org/.
It allows you to set tasks, assign executors, and change their statuses.
To use the system, you need to register and authenticate: [Task Manager](https://python-project-52-09c5.onrender.com)

## Installing and launch
1. Clone the repository and then navigate to it. All subsequent commands should be executed from within the "python-project-52" directory.
```
git clone https://github.com/Alex-Iset/python-project-52.git
```
2. Use the Makefile commands.
```
make build
make dev
```