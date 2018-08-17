import ruamel.yaml.util
import sys
import os
import signal
import subprocess
import argparse
import logging
import json
from logging.handlers import TimedRotatingFileHandler
import shutil
import smtplib
import time
import socket
from filelock import FileLock

from string import Template

fh = TimedRotatingFileHandler('autoscaleLog.log',  when='midnight')
fh.suffix = '%Y_%m_%d.log'

logging.basicConfig(filename='autoscaleLog.log',level=logging.DEBUG)
hostname = socket.gethostname()

logging.info('\n worker scaling script starting')
parser = argparse.ArgumentParser(description='Adding or Removing external workers')
parser.add_argument('-a','--action', type=str, choices=['add', 'remove'], help='add/remove Workers (add or remove)', required=True)
parser.add_argument('-n','--number', choices=list(map(str,range(1,101)))+['all'], help='Amount that you want to add or remove (positive number or all if to remove all)', required=True)
parser.add_argument('-e','--environment', choices = ['dev','sbox','prod'], help='Environment that is being used (dev,sbox,prod)', required=True)
parser.add_argument('-c','--config', help='Config file to be used for external worker deployment', required=True)
args = vars(parser.parse_args())
#except Exception, e:
#    print("You will need to login using fly -t [target] login to access your pipeline") 
logging.info('All input information accepted')
config_file = args['config']
add_remove = args['action']
env = args['environment']
amount = args['number']

from ruamel.yaml.util import load_yaml_guess_indent
shutil.copy2(config_file,'copy_config_file.yml')
logging.info('copy of config file stored in copy_config_file.yml')
with open(config_file) as y:
    
    try:
        logging.info('opening and reading config file')
        load, ind, bsi1 = load_yaml_guess_indent(y)
        deployment_config_file = load[env]['bosh_deployment_configuration_file']
        bosh_env = load[env]['bosh_environment']
        deployment_name = load[env]['bosh_external_deployment_name']
        worker_config = load[env]['bosh_external_worker_configuration']
        max_workers = load[env]['max_number_external_workers']
        bosh_executable = load[env]['bosh_path']
	flyPath = load[env]['fly_path']
	awkPath = load[env]['awk_path']
        myEmail = load[env]['my_email']
	toEmail = load[env]['to_emails']
	running_time = load[env]['runningTime']
    except Exception, exc:
        print str(exc)
	logging.exception(exc)

logging.info('configuration file information has been loaded')
sender = 'ConcourseHelp@motorolasolutions.com'
receivers = toEmail

message = """From: ConcourseHelp <from@fromdomain.com>
To: ConcourseUser
Subject: SMTP e-mail test

This is a test e-mail message for your adding/removing workers program from %s
""" % (hostname)

if flyPath is None:
    flyPath = 'fly'
if awkPath is None:
    awkPath = 'awk'
if bosh_executable is None:
    bosh_executable = 'bosh'

instances_command = "%s -e %s instances -d concourse-ext-worker --json" % (bosh_executable, bosh_env)
out = subprocess.check_output(instances_command, shell=True)
item_dict = json.loads(out)
running_external_workers = len(item_dict['Tables'][0]['Rows'])
logging.info('current number of external workers is : %i' % running_external_workers)

scale_command = '%s -n -e %s deploy -d %s %s -l %s' % (bosh_executable, bosh_env, deployment_name, worker_config, deployment_config_file)
deployment_file_name = '%s' % (deployment_config_file)

def handler(signum, frame):
    print "Signal Handler called with Signal", signum
    smtpObj = smtplib.SMTP('smtp.mot.com')
    smtpObj.sendmail(sender, receivers, message)
    print "Successfully sent email"

signal.signal(signal.SIGALRM, handler)  
signal.alarm(running_time)

if amount == 'all':
     amount = int(max_workers)
if add_remove == 'add':
     change = int(amount)
elif add_remove == 'remove':
     change = int(amount)*-1

new_instances = running_external_workers + change
too_few = new_instances < 0
too_many = new_instances > max_workers

with open(deployment_file_name) as f:
    try:
        data, indent1, bsi = load_yaml_guess_indent(f)
	with FileLock(deployment_file_name):
	    logging.info("deployment configuration file has been opened")
	    if too_few:
                print("Number of workers requested to remove was more than the number of workers running, so number of workers has been set to 0")
                data['externalWorkerInstances'] = 0
		logging.info('external workers have been set to the minimum number of workers')
            if too_many:
                print("Number of workers requested to add was more than the maximum number of workers allowed, so number of workers has been set to %i" % int(max_workers))
		data['externalWorkerInstances'] = int(max_workers)
		logging.info('external workers have been set to the maximum number of workers')
            if too_few == False and too_many == False:
                data['externalWorkerInstances'] = new_instances
		logging.info('external workers have been set to the input number of workers')
	ruamel.yaml.round_trip_dump(data, open(deployment_file_name, 'w'), indent=indent1, block_seq_indent=bsi)
        #os.system(scale_command)
    except Exception, e:
        print str(e)
	logging.exception(e)

os.system(scale_command)
