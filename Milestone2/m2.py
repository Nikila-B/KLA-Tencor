import yaml
import time
import os
import sys
import datetime
from threading import *


sys.path.insert(0,'C:/Users/nikil/Desktop/Nikki/Placement/KLA-Tencor')
import Functions

obj = Functions.Function()
op_file = "M2A_log.txt"
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here,'Milestone2A.yaml')

dlhashmp = {}

with open(filename) as f:
    dict = yaml.full_load(f)

ct = datetime.datetime.now()
workflow = list(dict.keys())[0]
current_dir = workflow
op = open(op_file, 'w')
op.write("")
op.close()

mutex = Semaphore(2)

def task(functionname,inputs,history,cond):

    if cond!=None:
        string = cond[2:].split(')')
        checked = False
        if string[0] in dlhashmp.keys():
            checked = True
            checker = cond.replace('$','dlhashmp').replace('(',"['").replace(')',"']")
            if eval(checker)==False:
                op = open(op_file, 'a')
                ct = datetime.datetime.now()
                op.write(str(ct)+";"+history+" Skipped"+"\n")
                op.close()
                op = open(op_file, 'a')
                ct = datetime.datetime.now()
                op.write(str(ct)+";"+history+" Exit"+"\n")
                op.close()
                return 
            else:
                time.sleep(5)

    if functionname == "TimeFunction":
        op = open(op_file, 'a')
        ct = datetime.datetime.now()
        op.write(str(ct)+";"+history+" Executing "+functionname+" ("+inputs['FunctionInput']+", "+inputs['ExecutionTime']+")"+"\n")
        op.close()
        obj.TimeFunction(int(inputs['ExecutionTime']))
        op = open(op_file, 'a')
        ct = datetime.datetime.now()
        op.write(str(ct)+";"+history+" Exit"+"\n")
        op.close()

    if functionname == "DataLoad":
        output = []
        op = open(op_file, 'a')
        ct = datetime.datetime.now()
        op.write(str(ct)+";"+history+" Executing "+functionname+" ("+inputs['Filename']+")"+"\n")
        op.close()
        output = obj.DataLoad(inputs['Filename'])
        dlhashmp[history+".NoOfDefects"] = output[1]
        op = open(op_file, 'a')
        ct = datetime.datetime.now()
        op.write(str(ct)+";"+history+" Exit"+"\n")
        op.close()

def flow_to_task(dict,name,exec,history):
    if dict['Type']=='Task':
        cond=None
        if 'Condition' in dict.keys():
            cond = dict['Condition']
        task(dict['Function'],dict['Inputs'],history,cond)

    else:
        op = open(op_file, 'a')
        ct = datetime.datetime.now()
        op.write(str(ct)+";"+history+" Entry"+"\n")
        op.close()
        threadlist=[]
        for key,value in dict['Activities'].items():
            if value['Type']=='Task':
                op = open(op_file, 'a')
                ct = datetime.datetime.now()
                op.write(str(ct)+";"+history+"."+key+" Entry"+"\n")
                op.close()

            if dict['Execution']=='Concurrent':
                t = Thread(target=flow_to_task,args=[value,key,dict['Execution'],history+"."+key])
                threadlist.append(t)
                t.start()
            else:
                flow_to_task(value,key,dict['Execution'],history+"."+key)
        if len(threadlist)!=0:
            for i in threadlist:
                i.join()
        op = open(op_file, 'a')
        ct = datetime.datetime.now()
        op.write(str(ct)+";"+history+" Exit"+"\n")
        op.close()
                
flow_to_task(dict[workflow],workflow,"",workflow)
print(dlhashmp)