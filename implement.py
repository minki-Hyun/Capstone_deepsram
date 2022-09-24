#!/usr/bin/python

# -*- coding: utf-8 -*-

import capsthone_test as capsthone
import matplotlib.pyplot as plt
import automation as auto
import numpy as np
import os

# plt.close()
xvdd = 0.70
target_yield = 6
epi_num = 500
step_num = 300

#create DB txt file
default_dir = "./final"
fileName = "scoreParamDB_operatingVlt"+str(xvdd)+"_targetYld"+str(target_yield)+".txt"
file_dir = default_dir+"/"+fileName
f_out = open(file_dir,'a')
textStr = "[location]\t[wrtieYield]\t[writeEnergy]\t\t[readYield]\t[readSpeed]\t\t[readEnergy]\t\t[score]\t\t\t\t[simulationTime]"
f_out.write(textStr)
f_out.close()

os.chdir(default_dir)

#auto.modify_sesitivity_spfile(xvdd)
auto.get_sensitivity("read")
auto.get_sensitivity("write")

environment = capsthone.GridWorld(xvdd,target_yield)
agentQ = capsthone.Q_Agent(environment, epsilon=0.2,alpha=0.5,gamma=0.99)
# Note the learn=True argument!
reward_per_episode = capsthone.play(environment, agentQ, trials=epi_num, max_steps_per_episode= step_num,learn=True, _voltage=xvdd, _yield=target_yield)

# Export reward_per_episode =========================================================
f_out1 = open("reward_per_episode.txt", "w")
for i in reward_per_episode:
    f_out1.write(str(i)+"\n")
f_out1.close()
# =============================================================================

# Export Q_table ==================================================================
height = environment.height
width = environment.width

a= np.zeros((height*width,4))
key = ['UP','DOWN','LEFT','RIGHT']

for x in range(height):
    for y in range(width):
        for i in range(4):
            a[10*x+y,i]=agentQ.q_table[x,y][key[i]]

np.savetxt("Qtable.txt",a,header="'UP'\t\t\t'DOWN'\t\t\t'LEFT'\t\t\t'RIGHT'",fmt="%e",delimiter = "\t\t")
# =============================================================================



# np.savetxt("Q_table.txt",agentQ.q_table,)

# Simple learning curvei
#epi_numList = np.linspace(start=1, stop=epi_num, num=epi_num,endpoint=True,dtype=int)
#plt.scatter(epi_numList,reward_per_episode,marker='+',color='b',s=5)
#plt.xlabel('Episode')
#plt.ylabel('Cumulative Score')
#plt.savefig('Epi_CumulativeScore.png')
