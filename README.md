<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
<!--   <a href="#">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

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
<!-- ## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- GETTING STARTED -->
## Getting Started

In order to be able to add log viewer in you django project you will have to follow some steps which I have shown below.

### Prerequisites

If you are starting from scratch then you must need to configure some things.
1. You have to install Python in your system. Search for python in your web browser then download and install. 
   After successfull installation open terminal and make sure by running
  ```sh
  python --version
  ```
Now you are good to proceed for setting up your project.

### Project Setup

If you are starting from scratch then follow from step 1. If you have an existing django project then follow from step 5.

1. Make a directory where you want to put your project. Open terminal iside the directory.
   <br>Create a virtual environment by running
   ```sh
   python -m venv venv
   ```
   or
   ```sh
   python3 -m venv venv
   ```
   This will create a new directory named venv inside our project folder.
2. Activate the virtual environment.
   <br>gitbash cli
   ```sh
   source/venv/Scripts/activate
   ```
   terminal
   ```sh
   venv\Scripts\activate
   ```
3. Install Django.
   ```sh
   pip install Django
   ```
4. Start a new project
   ```sh
   django-admin startproject django_logger .
   ```
   you will see a new directory name django_logger and a new file manage.py has been created.
   <br> Now to verify your project creation run the following command
   ```sh
   python manage.py runserver
   ```
   Now browse `localhost:8000` or `127.0.0.1:8000`in your browser. You will see a success page. :smile:
5. Create a new app for log viewer by running
   ```sh
   django-admin startapp app_logviewer
   ```
6. In your main app `settings.py`(in our case 'django_logger') iside INSTALLED_APPS add 'app_logviewer'
   ```py
   INSTALLED_APPS = [
      ....,
      ....,
      'app_logviewer',
   ]
   ```
7. Configure templates directory. if you are already configured and working with templates then you can skip.
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
8. Configure static files directory. Again you can skip if you have already configured.
   ```py
   STATIC_URL = 'static/'
   STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static')
   ]
   STATIC_ROOT =os.path.join(BASE_DIR, 'assets')
   ```
9. Logging configuration. You can configure this logger as per as your need. You can check out django logger documentation.
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
            '': {
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
10. Now we will need to register our app_logviewer app url in the main apps(in our case django_logger) `urls.py` file.
    ```py
    from django.urls import path, include

    # logviewer url
    path('logs/', include('app_logviewer.urls'),name='logs'),
    ```
11. Now we make views for our app_logviewer. So open `views.py` of app_logviewer. And just simply paste the following code snippet.
    ```py
    from django.shortcuts import render,redirect
    from django.contrib import messages
    import os
    import re
    from django.core.paginator import Paginator
    # import logging

    # logger = logging.getLogger(__name__)


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
            log_data['all_logs'] = all_logs
            debug_logs.reverse()
            log_data['debug_logs'] = debug_logs
            info_logs.reverse()
            log_data['info_logs'] = info_logs
            warning_logs.reverse()
            log_data['warning_logs'] = warning_logs
            error_logs.reverse()
            log_data['error_logs'] = error_logs
            critical_logs.reverse()
            log_data['critical_logs'] = critical_logs
            logs.append(log_data)
        # print(logs)
        todays_log = logs[0]
        return render(request,'logger/dashboard.html',{'logs':logs, 'todays_log':todays_log})
        # logger.debug('This is a log message.')

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
        log_paginator = Paginator(logs, 20)
        page_number = request.GET.get('page')
        total_pages = log_paginator.num_pages
        logs_per_page = log_paginator.get_page(page_number)
        return render(request,'logger/logs.html',{'logs':logs_per_page, 'file':file, 'total_pages':total_pages})
    ```
12. Now create a new file `urls.py` for app_logviewer app. And paste the following code.
    ```py
    from django.urls import path
    from .views import *

    urlpatterns = [
        path('', dashboard, name='dashboard'),
        path('debug/<str:file>', logs, name='logs'),
    ]
    ```
13. Now we need to collect the templates and static files for the app_logviewer app.
    i. First clone or download the repo from this link. https://github.com/mukulmh/django-logviewer
    ii. Copy the templates and static folder to our projects root directory.
    iii. If you already have static and templates folder then just copy the files and directories inside of the static and templates folders.
    
14. Now it's all done. If you have completed all the above steps as I have shown then you can run your application by running 
    <br>`python manage.py runserver`.
    <br>Open your browser and type `localhost:8000/logs or` `127.0.0.1:8000/logs`. You will see the log viewer dashboard. 😃 Congratulations. 🎆
15. Now to log your site logs you can make a middleware. If you don't want to use middleware and want to log only specific requests/views logs then you will have to write the following code in your desired views.py file.
    ```py
    import logging
    
    # create the logger instance
    logger = logging.getLogger(__name__)
    
    # now you can log whatever you want by adding the follwing line
    logger.info('This is the log message!')
    # now the log will be recorded whenever the view is triggered
    ```
    You can verify by browsing the log file which will be found in the logs directory. You will see a .log file has been created for current day. Every day there will be a new file for writing the logs.<br>
16. Final step if you want to add a middleware configuration.<br>
    i. Create a new directory named middleware inside the main app directory(in our case django_logger). Inside middleware directory create a new file `__init__.py`<br>
    ii. Now copy the code snippet and paste into `__init__.py` file. You can make your own custom middleware. Check out the django custom middleware documentation.
    ```py
    
    """
    Middleware to log `*/api/*` requests and responses.
    """
    import socket
    import time
    import json
    import logging

    request_logger = logging.getLogger('django')


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
    iii. Now register this middleware for you djanog application. Include the middleware at the end of the middleware lists like below.
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
[product-screenshot]: images/screenshot.png
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
