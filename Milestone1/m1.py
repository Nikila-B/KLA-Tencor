# import yaml
# import time
# import os
# import sys
# import datetime

# sys.path.insert(0,'C:/Users/nikil/Desktop/Nikki/Placement/KLA-Tencor')
# import Functions

# obj = Functions.Function()
# op_file = "M1A_log.txt"
# here = os.path.dirname(os.path.abspath(__file__))
# filename = os.path.join(here, 'Milestone1A.yaml')
# lt = []
# sublt = []

# with open(filename) as f:
#     dict = yaml.full_load(f)

# def task(string,task_name):

#     function = string['Function']
#     inputs = string['Inputs']

#     if function == 'TimeFunction':
#         op = open(op_file, 'a')
#         ct = datetime.datetime.now()
#         op.write(str(ct)+";"+current_dir+"."+task_name+" Entry"+"\n")
#         op.close()
#         op = open(op_file, 'a')
#         ct = datetime.datetime.now()
#         op.write(str(ct)+";"+current_dir+"."+task_name+" Executing "+function+" ("+string['Inputs']['FunctionInput']+", "+string['Inputs']['ExecutionTime']+")"+"\n")
#         op.close()
#         obj.TimeFunction(int(inputs['ExecutionTime']))
#         op = open(op_file, 'a')
#         ct = datetime.datetime.now()
#         op.write(str(ct)+";"+current_dir+"."+task_name+" Exit"+"\n")
#         op.close()

# workflow = list(dict.keys())[0]
# current_dir = workflow
# op = open(op_file, 'w')
# ct = datetime.datetime.now()
# op.write(str(ct)+";"+current_dir+" Entry"+"\n")
# op.close()
# activities = dict[workflow]['Activities']

# for key in activities:
#     lt.append(key)

# for i in range(len(lt)):
#     if lt[i][0]=='T':
#         task(dict[workflow]['Activities'][lt[i]],lt[i])
#     else:
#         old_dir = current_dir
#         current_dir = current_dir+"."+lt[i]
#         op = open(op_file, 'a')
#         ct = datetime.datetime.now()
#         op.write(str(ct)+";"+current_dir+" Entry"+"\n")
#         op.close()
#         execution = dict[workflow]['Activities'][lt[i]]['Execution']
#         activities = dict[workflow]['Activities'][lt[i]]['Activities']
#         for key in activities:
#             sublt.append(key)
#         for i in range(len(sublt)):
#             if sublt[i][0]=='T':
#                 task(activities[sublt[i]],sublt[i])
        
#         op = open(op_file, 'a')
#         ct = datetime.datetime.now()
#         op.write(str(ct)+";"+current_dir+" Exit"+"\n")
#         op.close()
#         current_dir = old_dir
# op = open(op_file, 'a')
# ct = datetime.datetime.now()
# op.write(str(ct)+";"+current_dir+" Exit"+"\n")
# op.close()

import yaml
import time
import os
import sys
import datetime
import threading
import multiprocessing

sys.path.insert(0,'C:/Users/nikil/Desktop/Nikki/Placement/KLA-Tencor')
import Functions

obj = Functions.Function()
op_file = "M1B_log.txt"
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'Milestone1B.yaml')
lt = []
sublt = []

with open(filename) as f:
    dict = yaml.full_load(f)

ct = datetime.datetime.now()
workflow = list(dict.keys())[0]
current_dir = workflow
op = open(op_file, 'w')
op.write("")
op.close()
activities = dict[workflow]['Activities']



def task(functionname,inputs,history):
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
        #print()


def flow_to_task(dict,name,exec,history):
    if dict['Type']=='Task':
        task(dict['Function'],dict['Inputs'],history)
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
                t = threading.Thread(target=flow_to_task,args=[value,key,dict['Execution'],history+"."+key])
                threadlist.append(t)
                t.start()
            else:
                print(key)
                flow_to_task(value,key,dict['Execution'],history+"."+key)
        if len(threadlist)!=0:
            for i in threadlist:
                i.join()
        op = open(op_file, 'a')
        ct = datetime.datetime.now()
        op.write(str(ct)+";"+history+" Exit"+"\n")
        op.close()
                
    
        
flow_to_task(dict[workflow],workflow,"",workflow)





        




