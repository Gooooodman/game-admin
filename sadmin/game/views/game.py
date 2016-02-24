#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.shortcuts import render_to_response,RequestContext
import  subprocess
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
def game_data(request):
    pass

@csrf_exempt
def game_install(request):
    if request.method == 'POST':
        name = request.POST['name']
        server_id = request.POST['server_id']
        ip = request.POST['ip']
        start_date = request.POST['start_date']
        start_date = start_date.replace(" ","_")
        server_name = request.POST['server_name']
        log_file = "/tmp/game_install.log"
        file=open(log_file,'a')
        port = 22
        ssh_conn = "ssh -A -p %s -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no %s"%(port,ip)
        install_cmd = """echo "Yes" |%s 'bash install.sh %s %s %s %s --server_name "%s"'"""%(ssh_conn,name,server_id,ip,start_date,server_name)
        #install_cmd = """%s 'yum remove vsftpd -y'"""%ssh_conn
        print install_cmd

        pipe = subprocess.PIPE
        install_ret = subprocess.Popen(install_cmd,stdout=pipe,stderr=pipe,shell=True)
        last_line= ""
        while install_ret.poll() == None:
            line = install_ret.stdout.readline()
            if len(line) >0:
                last_line = line
                #print line.strip()
                file.write(line+"</br>")
                file.flush()
        file.close()
        if install_ret.returncode != 0:
            message = "安装失败."
        else:
            message = "安装完成."

        kwvars = {"message":message,}
        return HttpResponse(json.dumps(kwvars),content_type='application/json')

    else:
        kwvars = {
            'request':request,
        }
        return render_to_response('game/install_bak.html',kwvars,RequestContext(request))




def game_read_log_file(request):
    filename = '/tmp/game_install.log'
    with open(filename,'r') as f:
        return HttpResponse(f.read())



def game_clean_log(request):
    cmd = "echo '' > /tmp/game_install.log "
    pipe = subprocess.PIPE
    ret = subprocess.Popen(cmd,stdout=pipe,stderr=pipe,shell=True)
    stdout,stderr = ret.communicate()
    if ret.returncode != 0 :
        message = "清理失败.."
    else:
        message = "清理成功.."
    kwvars = {"message":message,}
    return HttpResponse(json.dumps(kwvars),content_type='application/json')





