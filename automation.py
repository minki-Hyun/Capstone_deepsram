#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 09:05:03 2022

@author: hocl17
"""
import numpy as np
import matplotlib.pyplot as plt
import math as m
import os
from datetime import datetime

def modify_sesitivity_spfile(oper_voltage):
    #os.chdir("./final")
    print("Modify Sensitivity SPfile")
    opvoltage = "{operating_voltage}"
    xList = ["dvth_pdr", "dvth_pdl", "dvth_pur", "dvth_pul", "dvth_pgr", "dvth_pgl"]
    os.getcwd()
    # Read sensitivity
    f1 = open("read_sensitivity_uncomplete.sp")
    f1_content = f1.readlines()
    for x in xList:
        f1_outname = x+"_read.sp"
        f1_out = open(f1_outname, "w")
        for line in f1_content:
            
            if "{dvth}" in line:
                line = line.replace("{dvth}", x)
            
            if opvoltage in line:
                line = line.replace(opvoltage,str(oper_voltage))

            f1_out.write(line)
        f1_out.close()
        os.system("runHspice "+f1_outname)
    f1.close()

    for x in xList:
        os.system("grep snm= "+x+"_read.lis | sed 's/=/ /' | awk '{print $2}' > "+x+"_read.txt")
    
    # Write sensitivity
    f2 = open("write_sensitivity_uncomplete.sp")
    f2_content = f2.readlines()
    for x in xList:
        f2_outname = x+"_write.sp"
        f2_out = open(f2_outname, "w")
        for line in f2_content:
            
            if "{dvth}" in line:
                line = line.replace("{dvth}", x)
            
            if opvoltage in line:
                line = line.replace(opvoltage,str(oper_voltage))

            f2_out.write(line)
        f2_out.close()
        os.system("runHspice "+f2_outname)
    f2.close()

    for x in xList:
        os.system("grep wwtv= "+x+"_write.lis | sed 's/=/ /' | awk '{print $2}' > "+x+"_write.txt")
    print("Finish Modifying Sensitivity SPfile")

def get_sensitivity(type):
    print("Get sensitivity")
    #os.chdir("./final")

    if type == "read":
        f = open("dvth_pdl_read.txt","r")
        line_pdl = f.readlines()
        f = open("dvth_pdr_read.txt","r")
        line_pdr = f.readlines()
        f = open("dvth_pul_read.txt","r")
        line_pul = f.readlines()
        f = open("dvth_pur_read.txt","r")
        line_pur = f.readlines()
        f = open("dvth_pgl_read.txt","r")
        line_pgl = f.readlines()
        f = open("dvth_pgr_read.txt","r")
        line_pgr = f.readlines()
        fileOUTNAME = "slope_snm.txt"
        figNAME="merit_sensitivity_read_plot.jpg"
    else:
        f = open("dvth_pdl_write.txt","r")
        line_pdl = f.readlines()
        f = open("dvth_pdr_write.txt","r")
        line_pdr = f.readlines()
        f = open("dvth_pul_write.txt","r")
        line_pul = f.readlines()
        f = open("dvth_pur_write.txt","r")
        line_pur = f.readlines()
        f = open("dvth_pgl_write.txt","r")
        line_pgl = f.readlines()
        f = open("dvth_pgr_write.txt","r")
        line_pgr = f.readlines()
        fileOUTNAME = "slope_wwtv.txt"
        figNAME="merit_sensitivity_write_plot.jpg"

    for i in range(0,len(line_pdl)):
        line_pdl[i] = float(line_pdl[i])
    for i in range(0,len(line_pdr)):
        line_pdr[i] = float(line_pdr[i])
    for i in range(0,len(line_pul)):
        line_pul[i] = float(line_pul[i])
    for i in range(0,len(line_pur)):
        line_pur[i] = float(line_pur[i])
    for i in range(0,len(line_pgl)):
        line_pgl[i] = float(line_pgl[i])
    for i in range(0,len(line_pgr)):
        line_pgr[i] = float(line_pgr[i])
    
    sigma_start = -6
    sigma_final=6   
    sigma_nmbr_of_samples = 25 #0.48 step
    xx = np.linspace(sigma_start, sigma_final, sigma_nmbr_of_samples)

    plt.close("all")
    plt.title("Merit sensitivity (each of 6-TR)")
    plt.xlabel("sigma")
    plt.ylabel("merit")

    plt.plot(xx,line_pdl,"r-")
    plt.plot(xx,line_pdr,"g*-")
    plt.plot(xx,line_pul,"b-")
    plt.plot(xx,line_pur,"m-")
    plt.plot(xx,line_pgl,"y-")
    plt.plot(xx,line_pgr,"c-")
    plt.legend(['pdl','pdr','pul','pur','pgl','pgr'])
    plt.savefig(figNAME)
    
    _slope_point_start =6#-3
    _slope_point_final = 18#3
    sigma_range =3 

    slope_line_pdl = ( line_pdl[_slope_point_final] - line_pdl[_slope_point_start] ) / (2*sigma_range)
    slope_line_pdr = ( line_pdr[_slope_point_final] - line_pdr[_slope_point_start] ) / (2*sigma_range)
    slope_line_pul = ( line_pul[_slope_point_final] - line_pul[_slope_point_start] ) / (2*sigma_range)
    slope_line_pur = ( line_pur[_slope_point_final] - line_pur[_slope_point_start] ) / (2*sigma_range)
    slope_line_pgl = ( line_pgl[_slope_point_final] - line_pgl[_slope_point_start] ) / (2*sigma_range)
    slope_line_pgr = ( line_pgr[_slope_point_final] - line_pgr[_slope_point_start] ) / (2*sigma_range)

    slope = [ str(slope_line_pdl)+"\n", str(slope_line_pdr)+"\n", str(slope_line_pul)+"\n", str(slope_line_pur)+"\n", str(slope_line_pgl)+"\n", str(slope_line_pgr)+"\n"]

    f_out = open(fileOUTNAME, "w")

    for i in slope:
        f_out.write(i)
    
    f_out.close()

    if type == "read":
        os.system("mv -f dvth*_read.* ./rest_readsensitivity/")
        os.system("mv -f merit* ./rest_readsensitivity/")
    else:
        os.system("mv -f dvth*_write.* ./rest_readsensitivity/")
        os.system("mv -f merit* ./rest_writesensitivity/")
    
    print("Finish Getting Sensitivity")

def modify_failconstant_spec_spfile(current_location, oper_voltage):
    # 가로가 Cap 세로가 Pmos width
    # read fail constant
    
    #os.chdir("./final")

    pmos_finnum = "{pmos_finnum}"
    kick_cap = "{kick_cap}"
    xList = ["{dvth_pdl}", "{dvth_pdr}", "{dvth_pul}", "{dvth_pur}", "{dvth_pgl}", "{dvth_pgr}"]
    opvoltage = "{operating_voltage}"

    sensitivity_Read = open("slope_snm.txt",'r')
    sensitivity_ReadContent= sensitivity_Read.readlines()
    sensitivity_Write = open("slope_wwtv.txt",'r')
    sensitivity_WriteContent= sensitivity_Write.readlines()
    
    f1 = open("read_failconstant_uncomplete.sp",'r')
    f1_content = f1.readlines()
    f1_out = open("read_failconstant.sp",'w')
    for line in f1_content:
        i=0
        for x in xList:
            if x in line:
                line = line.replace(x, sensitivity_ReadContent[i].strip('\n'))
            i+=1
        if pmos_finnum in line:
                line = line.replace(pmos_finnum, str(3 + 1*current_location[0]))
        if opvoltage in line:
                line = line.replace(opvoltage,str(oper_voltage))
        f1_out.write(line)
    f1_out.close()
    f1.close()

    f2 = open("write_failconstant_uncomplete.sp",'r')
    f2_content = f2.readlines()
    f2_out = open("write_failconstant.sp",'w')
    for line in f2_content:
        i=0
        for x in xList:
            if x in line:
                line = line.replace(x, sensitivity_WriteContent[i].strip('\n'))
            i+=1
        if pmos_finnum in line:
                line = line.replace(pmos_finnum, str(3 + 1*current_location[0]))
        if opvoltage in line:
                line = line.replace(opvoltage,str(oper_voltage))
        if kick_cap in line:
            line = line.replace(kick_cap, str(1 + (2*current_location[1])))
        f2_out.write(line)
    f2_out.close()
    f2.close()

    f3 = open("read_spec_uncomplete.sp",'r')
    f3_content = f3.readlines()
    f3_out = open("read_spec.sp",'w')
    for line in f3_content:
        if opvoltage in line:
                line = line.replace(opvoltage,str(oper_voltage))
        if pmos_finnum in line:
            line = line.replace(pmos_finnum, str(3 + 1*current_location[0]))
        f3_out.write(line)
    f3_out.close()
    f3.close()

    f4 = open("write_spec_uncomplete.sp",'r')
    f4_content = f4.readlines()
    f4_out = open("write_spec.sp",'w')    
    for line in f4_content:
        
        if opvoltage in line:
                line = line.replace(opvoltage,str(oper_voltage))

        if pmos_finnum in line:
            line = line.replace(pmos_finnum, str(3 + 1*current_location[0]))
        
        if kick_cap in line:
            line = line.replace(kick_cap, str(1 + (2*current_location[1])))

        f4_out.write(line)
    f4_out.close()
    f4.close()
    print("** Finish Modifying Failconstant & Spec Simulation File")

def get_yield(type):
    
    print()
    print("Get "+type+"_Yield Start")
    #os.chdir("./final")

    if type == "read":
        file = "read_failconstant"
        file_REF = "slope_snm.txt"
        file_skew_REF = "read_skew.txt"
        fOUTName = "read_yield.txt"

    else:
        file = "write_failconstant"
        file_REF = "slope_wwtv.txt"
        file_skew_REF = "write_skew.txt"
        fOUTName = "write_yield.txt"

   # os.chdir("./final")
    os.system("runHspice "+file+".sp")
    os.system("grep 'skew =' "+file+".lis | awk '{print $4}' > "+type+"_skew.txt")
    
    f_in  = open(file_REF, 'r') 
    lines = f_in.readlines()
    
    hfin = 32e-9
    nfin = 1
    tfin = 6.5e-9
    l    = 20e-9

    denominator = m.sqrt((2*hfin+tfin)*nfin*l*1e12)
    sigmaVth = 1.2e-3/denominator

    f_skew_in = open(file_skew_REF,'r')
    skew = f_skew_in.readlines()
    k=float(skew[0])

    _sum =0 

    for line in lines:
        line=float(line)
        x=m.pow(k*line/sigmaVth,2)
        _sum+=x

    _yield = round(pow(_sum,0.5),4)

    f_out = open(fOUTName, "w")
    yield_str = str(_yield)
    f_out.write(yield_str)
    f_out.close()

    print(type+"_yield : %f"%_yield)

    if type == "read":
        os.system("mv read_failconstant.ic0 read_failconstant.pa0 \
            read_failconstant.lis read_failconstant.mt0 read_failconstant.st0 read_failconstant.tr0 ./rest_readfailconstant")
    else:
        os.system("mv write_failconstant.ic0 write_failconstant.pa0 \
            write_failconstant.lis write_failconstant.mt0 write_failconstant.st0 write_failconstant.tr0 ./rest_writefailconstant")
    
        
def get_spec(type):
    
    #os.chdir("./final")
    print()
    print("Get Spec")
    if type == "read":
        os.system("runHspice read_spec.sp")
        os.system("grep 'wl2sae=\|e_total=' read_spec.lis | awk '{print $2}' > read_spec.txt")
        os.system("mv read_spec.ic0 read_spec.lis read_spec.mt0 read_spec.pa0 read_spec.st0 read_spec.tr0 ./rest_readspec")
    else:
        os.system("runHspice write_spec.sp")
        os.system("grep 'etotal_write=' write_spec.lis | awk '{print $2}' > write_spec.txt")
        os.system("mv write_spec.ic0 write_spec.lis write_spec.mt0 write_spec.pa0 write_spec.st0 write_spec.tr0 ./rest_writespec")
    print("Finish Getting Spec")
    
    
# sigmoid slope : 50
def sigmoid(x):
    # return 1/(1+m.exp(x))
    # if x>0 : 
    #     #return 1.0/(1+m.exp(-50*x))
    #     return 100.0
    # else:
    #     #return 1.0/(1+m.exp(-x))
    #     return 200.0/(1+m.exp(-x))
    if x>=0 : 
        return 1.0#/(1+m.exp(-50*x))
    else:
        return 1.0/(1+m.exp(-25*x))
 
def get_score(current_location, target_yield, oper_voltage):
    
    now = datetime.now()
    time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
    readspec_un = open("./read_spec.txt", 'r')
    readspec = readspec_un.readlines()
    readYield_un = open("./read_yield.txt", 'r')
    readYield=readYield_un.readlines()
    writespec_un = open("./write_spec.txt", 'r')
    writespec=writespec_un.readlines()
    writeYield_un = open("./write_yield.txt", 'r')
    writeYield = writeYield_un.readlines()
    
    #2022.05.25 9PM edit 
    #write energy output data prefix type must be converted 
    # data type of every single .txt file is "LIST". So must be converted to string type for the next stage
    writespec_str = listToStringConversion(prefixTypeConversion(writespec[0]))
   
    read_speed_str=listToStringConversion(readspec[0])
    
    read_power_str=listToStringConversion(readspec[1])
    readYield_str = listToStringConversion(readYield[0])
    writeYield_str = listToStringConversion(writeYield[0])
   
    #create DB txt file
    # default_dir = "/home/hocl17/dsr/final"
    # fileName = "scoreParamDB_operatingVlt"+str(oper_voltage)+"_targetYld"+str(target_yield)+".txt"
    # file_dir = default_dir+"/"+fileName
    # f_out = open(file_dir,'a')
    # sumOfString = "\n"+current_location+"\t\t"+writeYield_str+"\t\t"+writespec_str+"\t\t"+readYield_str+"\t\t"+read_speed_str+"\t\t"+read_power_str+"\t\t"+time_str
    # f_out.write(sumOfString.rstrip())
    # f_out.close()

    """
    f_out = open("/home/hocl17/dsr/final/score_param_DB.txt",'a')
    sumOfString = "\n"+writeYield_str+"\t\t"+writespec_str+"\t\t"+readYield_str+"\t\t"+read_speed_str+"\t\t"+read_power_str+"\t\t"+time_str
    f_out.write(sumOfString.rstrip())
    f_out.close()
    """
    
#    avgeng = float(read_power_str)+float(writespec_str)
    avgeng = (float(read_power_str)+float(writespec_str))/2
    read_speed = float(read_speed_str)
    score = sigmoid(float(readYield_str)-target_yield)*sigmoid(float(writeYield_str)-target_yield)/(avgeng*read_speed)
    print("score : "+str(score))
    
    
    # Just Revise this
    default_dir = "."
    fileName = "scoreParamDB_operatingVlt"+str(oper_voltage)+"_targetYld"+str(target_yield)+".txt"
    file_dir = default_dir+"/"+fileName
    f_out = open(file_dir,'a')
    sumOfString = "\n"+str(current_location)+"\t\t"+writeYield_str+"\t\t"+writespec_str+"\t\t"+readYield_str+"\t\t"+read_speed_str+"\t\t"+read_power_str+"\t\t"+str(score)+"\t\t"+time_str
    f_out.write(sumOfString.rstrip())
    f_out.close()
    
    return score#*10e-20
    
"""
param 1 > in_str    : original data in .lis file => ex 7.3u 
return    > out_str  : converted data => ex 7.3e-06
"""
def prefixTypeConversion(in_str):
    
    """
    prefix      value
    m           e-03
    u            e-06
    n            e-09
    p            e-12
    f             e-15
    a            e-18
    z            e-21
    y            e-24
    """
    prefix = ['m', 'u', 'n', 'p', 'f', 'a', 'z', 'y']
    prefix_conv = ["e-03", "e-06" , "e-09", "e-12", "e-15", "e-18", "e-21", "e-24"]
    
    out_str=0
    count =0
    for pref in prefix:
        if pref in in_str:
            in_str = in_str.replace(pref, prefix_conv[count])            
            out_str = in_str;
        count+=1
    if out_str == 0:
        print("**Error!  : Conversion Error (prefixTypeConversion)")
        
    return out_str

"""
param 1 > in_list    : list data
return    > out_str  :  string data
"""
def listToStringConversion(in_list):
    
    out_str=""
    for s in in_list:
        out_str += s
    return out_str.strip()
