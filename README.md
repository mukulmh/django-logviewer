<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="#">
    <img src="static/img/logo.png" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">Django Log Viewer</h3>

  <p align="center">
    An UI based log viewer to debug you Django Applications!
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#project-setup">Project Setup</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Dashboard
[![Project Screen Shot][project-screenshot1]](https://example.com)
Logs
[![Project Screen Shot][project-screenshot2]](https://example.com)

Did you ever feel lazy about configuring a logger and used print() instead?... I did, yet logging is fundamental to every application and eases the process of debugging. So I have made this log viewer with user interface for Django Applications which is very user friendly. This log viewer can be implemented on any Django applications very easily. Both beginner or expert can integrate this log viewer with their applications with minimum amount of efforts. 😃


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

In order to be able to add log viewer in you django project you will have to follow some steps which I have shown below.

### Prerequisites

You will need to have Python installed in your system. Download and install Python from [here](https://www.python.org/downloads/). After successfull installation open terminal and make sure by running
  ```sh
  python --version
  ```
Now we are good to proceed.

### Project Setup

If you are starting from scratch then follow from step 1. If you have an existing django project then jump to step 5.

#### Step: 1 
Make a directory where you want to put your project. Open terminal iside the directory.
   <br>Create a virtual environment by running
   ```sh
   python -m venv venv
   ```
   or
   ```sh
   python3 -m venv venv
   ```
   This will create a new directory named venv inside our project folder.
#### Step: 2
Activate the virtual environment.
   <br>gitbash cli
   ```sh
   source venv/Scripts/activate
   ```
   terminal
   ```sh
   venv\Scripts\activate
   ```
#### Step: 3
Install Django.
   ```sh
   pip install Django
   ```
   or
   ```sh
   pip3 install Django
   ```
#### Step: 4
Start a new project named django_logger.
   ```sh
   django-admin startproject django_logger .
   ```
   you will see a new directory name django_logger and a new file manage.py has been created.
   <br> Now to verify your project creation run the following command.
   ```sh
   python manage.py runserver
   ```
   Now browse `localhost:8000` or `127.0.0.1:8000`in your browser. You will see a success page. :smile:
#### Step: 5 (Integrating log viewer to our Django Application)
Create a new app for log viewer by running
   ```sh
   django-admin startapp app_logviewer
   ```
#### Step: 6
In your main app `settings.py`(in our case `django_logger`) in INSTALLED_APPS list add 'app_logviewer' as shown below.
   ```py
   INSTALLED_APPS = [
      ....,
      ....,
      'app_logviewer',
   ]
   ```
#### Step: 7
Configure templates directory. if you are already configured and working with templates then you can skip.
   ```py
   TEMPLATES_DIR = BASE_DIR / 'templates' # templates will be the folder from where we will render our HTML files.
    
   TEMPLATES = [
     {
       ....
       'DIRS': [TEMPLATES_DIR],
       ....
       ....
     }
   ]
   ```
#### Step: 8
Configure static files directory. Again you can skip if you have already configured.
   ```py
   STATIC_URL = 'static/'
   STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static')
   ]
   STATIC_ROOT =os.path.join(BASE_DIR, 'assets')
   ```
#### Step: 9
Logging configuration. You can configure this logger as per as your need. You can check out django [logging](https://docs.djangoproject.com/en/4.1/topics/logging/) documentation.
   ```py
   # logging configuration below
   from datetime import date
   today = str(date.today())
   # LOGFILE_SIZE = 7 * 1024
   # LOGFILE_COUNT = 20
   Path("logs").mkdir(parents=True, exist_ok=True)

   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'class': 'logging.handlers.RotatingFileHandler',
               'filename': 'logs/' + today + '.log',
               'level': 'DEBUG',
               'formatter': 'verbose',
               # 'maxBytes': LOGFILE_SIZE,
               # 'backupCount': LOGFILE_COUNT,
           },
        },
        'loggers': {
            'djangoapi': {
                'level': 'DEBUG',
                'handlers': ['file'],
            },
        },
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {funcName} {message}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
   }
   ```
#### Step: 10
Now we will need to register our app_logviewer app url in the main apps(in our case django_logger) `urls.py` file.
   ```py
  from django.urls import path, include

  # logviewer url
  path('logs/', include('app_logviewer.urls'),name='logs'),
   ```
#### Step: 11
Now we make views for our app_logviewer. So open `views.py` of `app_logviewer`. And just simply paste the following code snippet.
   ```py
  from django.http import HttpResponse
from django.shortcuts import render,redirect
import os
import re
from django.core.paginator import Paginator
import logging
import mimetypes
from django.http.response import HttpResponse

logger = logging.getLogger('django')


# Create your views here.
# logs
def dashboard(request):
    files = os.listdir('logs')
    files.reverse()
    logs = []
    for file in files:
        log_data = {}
        all_count = 0
        debug_count = 0
        info_count = 0
        error_count = 0
        warning_count = 0
        critical_count = 0

        with open('logs/'+file) as fp:
            all_logs = []
            debug_logs = []
            info_logs = []
            warning_logs = []
            error_logs = []
            critical_logs = []
            for line in fp:
                if line.strip():
                    if re.findall(r'DEBUG|INFO|ERROR|WARNING|CRITICAL',line):
                        all_count += 1
                        all_logs.append(line)
                    if line.find('DEBUG') != -1:
                        debug_count += 1
                        debug_logs.append(line)
                    if line.find('INFO') != -1:
                        info_count += 1
                        info_logs.append(line)
                    if line.find('ERROR') != -1:
                        error_count += 1
                        error_logs.append(line)
                    if line.find('WARNING') != -1:
                        warning_count += 1
                        warning_logs.append(line)
                    if line.find('CRITICAL') != -1:
                        critical_count += 1
                        critical_logs.append(line)
        log_data['file'] = file
        file = file.split('.', 1)
        log_data['date'] = file[0]
        log_data['all_count'] = all_count
        log_data['info_count'] = info_count
        log_data['debug_count'] = debug_count
        log_data['error_count'] = error_count
        log_data['warning_count'] = warning_count
        log_data['critical_count'] = critical_count
        all_logs.reverse()
        log_data['all_logs'] = all_logs[:100]
        debug_logs.reverse()
        log_data['debug_logs'] = debug_logs[:100]
        info_logs.reverse()
        log_data['info_logs'] = info_logs[:100]
        warning_logs.reverse()
        log_data['warning_logs'] = warning_logs[:100]
        error_logs.reverse()
        log_data['error_logs'] = error_logs[:100]
        critical_logs.reverse()
        log_data['critical_logs'] = critical_logs[:100]
        logs.append(log_data)
    # print(logs)
    todays_log = logs[0]
    logger.warning('Accesed log dashboard!')
    return render(request,'logger/dashboard.html',{'logs':logs[:7], 'todays_log':todays_log})

# logs
def logs(request, file):
    logs=[]
    with open('logs/'+file) as fp:
        log_no = 0
        for line in fp:
            log_data = {}
            if re.findall(r'DEBUG|INFO|ERROR|WARNING|CRITICAL',line):
                log_data['log'] = line
                message = line.split(' ', 4)
                log_data['message'] = message[4]
                log_no += 1
                log_data['log_number'] = log_no
                logs.append(log_data)
    logs.reverse()
    log_paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    total_pages = log_paginator.num_pages
    logs_per_page = log_paginator.get_page(page_number)
    return render(request,'logger/logs.html',{'logs':logs_per_page, 'file':file, 'total_pages':total_pages})


# download 
def download_log(request, file=''): 
    if file != '': 
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        filepath = BASE_DIR + '/logs/' + file 
        path = open(filepath, 'rb') 
        mime_type, _ = mimetypes.guess_type(filepath) 
        response = HttpResponse(path, content_type=mime_type) 
        response['Content-Disposition'] = "attachment; filename=%s" % file 
        return response 
    else: 
        return redirect('dashboard') 
 
# delete 
def delete_log(request, file=''): 
    if file != '': 
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        filepath = BASE_DIR + '/logs/' + file 
        if os.path.isfile(filepath):
            try:
                os.remove(filepath) 
            except Exception as e:
                logger.error(e)
    return redirect('dashboard')

   ```
#### Step: 12
Now create a new file `urls.py` in app_logviewer directory. And paste the following code.
   ```py
  from django.urls import path
  from .views import *

  urlpatterns = [
      path('', dashboard, name='dashboard'),
      path('debug/<str:file>', logs, name='logs'),
      path('download_log/<str:file>', download_log, name='download_log'),
      path('delete_log/<str:file>', delete_log, name='delete_log'),
  ]
   ```
#### Step: 13
Now we need to collect the templates and static files for the app_logviewer app.<br>
    i. First clone or download the repo from this [link](https://github.com/mukulmh/django-logviewer). <br>
    ii. Copy the templates and static folder to our projects root directory.<br>
    iii. If you already have static and templates folder then just copy the files and directories from the static and templates folders.
    
#### Step: 14
Now it's all set. If you have completed all the above steps as I have shown then you can run your application by running the server again.
    <br>`python manage.py runserver`.
    <br>Open your browser and type `localhost:8000/logs or` `127.0.0.1:8000/logs`. You will see the log viewer dashboard. 😃 Congratulations. 🎆
#### Step: 15
Now to log your applications logs you can make a middleware. If you don't want to use middleware and want to log only specific requests/routes then you will have to write the following code in your desired views.py file. For better understanding please browse this [link](https://docs.djangoproject.com/en/4.1/howto/logging/)
   ```py
  import logging

  # create the logger instance
  logger = logging.getLogger(__name__)

  # now you can log whatever you want by adding the follwing line
  logger.info('This is the log message!')
  # now the log will be recorded whenever the view is triggered
   ```
You can verify by browsing the log file which will be found in the logs directory. You will see a .log file has been created for current day. Every day there will be a new file for storing the logs.<br>
#### Step: 16(Optional)
Final step if you want to add a middleware configuration.<br>
   i. Create a new directory named middleware inside the main app directory(in our case django_logger). Inside middleware directory create a new file `__init__.py`<br>
   ii. Now copy the code snippet and paste into `__init__.py` file. You can make your own custom middleware. Check out the django custom [middleware](https://docs.djangoproject.com/en/4.1/topics/http/middleware/) documentation.
   ```py
    
  """
  Middleware to log `*/api/*` requests and responses.
  """
  import socket
  import time
  import json
  import logging

  request_logger = logging.getLogger('djangoapi')


  class RequestLogMiddleware:
      """Request Logging Middleware."""

      def __init__(self, get_response):
          self.get_response = get_response

      def __call__(self, request):
          start_time = time.time()
          log_data = {
              "remote_address": request.META["REMOTE_ADDR"],
              "server_hostname": socket.gethostname(),
              "request_method": request.method,
              "request_path": request.get_full_path(),
          }

          # Only logging "*/api/*" patterns
          if "/api/" in str(request.get_full_path()):
              req_body = json.loads(request.body.decode(
                  "utf-8")) if request.body else {}
              log_data["request_body"] = req_body

          # request passes on to controller
          response = self.get_response(request)

          # add runtime to our log_data
          if response and response["content-type"] == "application/json":
              response_body = json.loads(response.content.decode("utf-8"))
              log_data["response_body"] = response_body
          log_data["run_time"] = time.time() - start_time

          request_logger.info(msg=log_data)

          return response

      # Log unhandled exceptions as well
      def process_exception(self, request, exception):
          try:												
              raise exception
          except Exception as e:
              request_logger.exception("Unhandled Exception: " + str(e))
          return exception
  ```
  iii. Now register this middleware for you django application. Include the middleware at the end of the middleware lists like below.
  ```py
  MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',

      'django_logger.middleware.RequestLogMiddleware', # this is the custom middleware
  ]
   ```
Now if you run the server again, you will see that every time a request is made there will be log entry for that request containing informations like remote address, hostname, method, request url, request body or response body etc.

Phew... That was a very lengthy documentation. If you have successfully completed all the steps and faced no issue then hats off to you. 🤝 <br>
If you have any confusion or face any error or don't get expected output then feel free to contact me. 
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Mehedy Hassan Mukul - [Telegram 📞](https://t.me/mhmukul) - mukulseu@gmail.com 📧

Project Link: https://github.com/mukulmh/django-logviewer

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 -->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[project-screenshot1]: static/img/logger-dashboard.png
[project-screenshot2]: static/img/log-viewer.png
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
