import ruamel.yaml.util
import sys
import os
import subprocess
import argparse
import time

parser = argparse.ArgumentParser(description='Scale number of external workers')
parser.add_argument('-t','--target', type=str, help='Concourse target name', required=True)
parser.add_argument('-c','--config', help='Config file to be used for external worker deployment', required=True)
parser.add_argument('-e','--environment', choices = ['dev','sbox','prod'], help='Environment that is being used (dev,sbox,prod)', required=True)
args = vars(parser.parse_args())
#amount read from config file

config_file = args['config']
target = args['target']
env = args['environment']
time_end = time.time() + 60*8

from ruamel.yaml.util import load_yaml_guess_indent

with open(config_file) as y:
    try:
        #logging.info('opening and reading config file')
        load, ind, bsi1 = load_yaml_guess_indent(y)
        increase_by = load[env]['increment_by']
	decrease_by = load[env]['decrease_by']
        bosh_executable = load[env]['bosh_path']
        flyPath = load[env]['fly_path']
        awkPath = load[env]['awk_path']
	increase_threshold = load[env]['addThreshold']
	decrease_threshold = load[env]['removeThreshold']
	avg_threshold = load[env]['averageThreshold']
    except Exception, exc:
        print str(exc)
if flyPath is None:
    flyPath = 'fly'
if awkPath is None:
    awkPath = 'awk'
if bosh_executable is None:
    bosh_executable = 'bosh'
#print(flyPath)

see_workers = "%s -t %s ws" % (flyPath,target)
worker_list = "%s -t %s workers | %s '{print $1,$2}'" % (flyPath,target,awkPath)
add_workers = "python autoscaleConcourse.py -a add -n %i -e %s -c %s" % (increase_by,env,config_file) 
remove_worker = "python autoscaleConcourse.py -a remove -n %i -e %s -c %s" % (decrease_by,env,config_file)
#output = subprocess.check_output(worker_list, shell=True)
#inputList = output.encode('UTF-8').strip().split("\n")
#workerList = []
#containerList = []
#for line in inputList:
#    worker, container = line.strip().split(" ")
#    workerList.append(worker)
#    containerList.append(int(container))
#workerSize = len(workerList)
#total_container_capacity = int(avg_threshold) * len(workerList)
#if any number in part2List is over 180, then run add command

while time.time() < time_end:
    output = subprocess.check_output(worker_list, shell=True)
    inputList = output.encode('UTF-8').strip().split("\n")
    workerList = []
    containerList = []
    for line in inputList:
        worker, container = line.strip().split(" ")
        workerList.append(worker)
        containerList.append(int(container))
    workerSize = len(workerList)
    total_container_capacity = int(avg_threshold) * len(workerList)
    total_containers = sum(a for a in containerList)
    #print(total_containers)
    #for i in part2List:
    if max(containerList) > increase_threshold and min(containerList) == 0:
	os.system(see_workers)
	print("\n***Pausing for 20 seconds to allow containers to distribute")
	time.sleep(20)
    if max(containerList) > increase_threshold and ((avg_threshold*(workerSize)) > total_containers):
	os.system(see_workers)
	print("***The correct number of workers are running for the current load, pausing for 15 seconds to check for incoming jobs")
	time.sleep(15)
    elif max(containerList) > increase_threshold and ((avg_threshold*(workerSize)) < total_containers):
	#print((avg_threshold*(workerSize)))
	#print(total_containers)
	os.system(see_workers)
	print("\n***Currently adding workers because there is a worker with over %i containers") % (increase_threshold)
	os.system(add_workers)
	print("\n***Pausing for 5 seconds to allow containers to distribute")
	time.sleep(5)
	    #sys.exit()
    #for i in part2List:
    elif (total_containers == 0):
	os.system(see_workers)
	print("\n***There are no jobs running")
	print("***Pausing for 5 seconds to check for incoming build")
	time.sleep(5) 
    if (total_containers > 0) and (max(containerList) < decrease_threshold) or ((avg_threshold*(workerSize-1)) > total_containers):
	os.system(see_workers)
	print("\n***Currently removing worker because the number of containers (%i) can be handled by %i workers") % (total_containers,workerSize - 1)
        os.system(remove_worker)
        print("\n***Pausing for 10 seconds to allow containers to distribute")
        time.sleep(10)
	
    #if max(part2List) <= decrease_threshold:
        #print("removing workers")
	#os.system(remove_worker)
    else:
        os.system(see_workers)
        print("***Scaling up or down is not helpful right now, and is not being done, pauses to check for any change in build")
        time.sleep(5)
            
#if (avg_threshold*(workerSize-1)) <= total_container_capacity:
#    os.system(remove_worker)
#    print(removing worker)
#if any number in part2List is under 140, then run remove command
