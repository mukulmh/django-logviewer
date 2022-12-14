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
