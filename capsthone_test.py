#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Written by Minki Hyun.
If you have any question, just contact me : phantom3600@naver.com
"""

import numpy as np
import math as m
import automation as auto
from datetime import datetime

class GridWorld:
    ## Initialise starting data
    def __init__(self,xvdd,target_yield):
        # Set information about the gridworld
        self.height = 10
        self.width = 10
        self.grid = np.zeros(( self.height, self.width))
        self.oper_voltage = xvdd
        self.target_yield = target_yield
        
        # # Set random start location for the agent
        self.current_location = (0,0)
        
        # Set available actions
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        
    
    ## Put methods here:
    def get_available_actions(self):
        """Returns possible actions"""
        location = self.current_location
        real_action = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if location[0] == 0:
            real_action.remove('UP')
        if location[1]==0:
            real_action.remove('LEFT')
        if location[0] == self.height-1:
            real_action.remove('DOWN')
        if location[1] == self.width -1:
            real_action.remove('RIGHT')
        #print("self.available_action:",self.actions)
        #print("current_location :",self.current_location)
        #print("availabe action :",real_action)
        return real_action
    
    def agent_on_map(self):
        """Prints out current location of the agent on the grid (used for debugging)"""
        grid = np.zeros(( self.height, self.width))
        grid[ self.current_location[0], self.current_location[1]] = 1
        return grid
    
    def get_score(self, current_location, target_yield, oper_voltage):
        
        #여기에 PMOS width랑 Kick Cap 바꿔야 됨
        auto.modify_failconstant_spec_spfile(current_location, oper_voltage)
        auto.get_yield("read")
        auto.get_yield("write")
        auto.get_spec("read")
        auto.get_spec("write")
        
       
        # readspec = open("/home/hocl17/dsr/final/read_spec.txt", 'r')
        # readYield = open("/home/hocl17/dsr/final/read_yield.txt", 'r')
        # writespec = open("/home/hocl17/dsr/final/write_spec.txt", 'r')
        # writeYield = open("/home/hocl17/dsr/final/write_yield.txt", 'r')
        
        # avgeng = float(readspec[1])+float(writespec[0])
        # read_speed = float(readspec[0])
        # score = self.sigmoid(float(readYield)-target_yield)*self.sigmoid(float(writeYield)-target_yield)/(avgeng*read_speed)
        
        self.grid[current_location[0], current_location[1]] = auto.get_score(current_location, target_yield, oper_voltage)

    
    def get_reward(self, location):
        """Returns the reward for an input position"""
        #self.grid[location[0], location[1]] = self.get_score(location)
        return self.grid[location[0], location[1]]
    
    #dummy  codes --> use. adopt.
    def write_only_score_on_txt(self):
    
        now = datetime.now()
        time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        #create DB txt file
        default_dir = "."
        fileName = "scoreParamDB_operatingVlt"+str(self.oper_voltage)+"_targetYld"+str(self.target_yield)+".txt"
        file_dir = default_dir+"/"+fileName
        f_out = open(file_dir,'a')
        
        sumOfString = "\n"+str(self.current_location)+"\t\t\t---------------------------------------------->SKIP<----------------------------------------------\t\t\t\t"+time_str
        
        f_out.write(sumOfString.rstrip())
        
        f_out.close()
        
    def make_step(self, action):
        """Moves the agent in the specified direction. If agent is at a border, agent stays still
        but takes negative reward. Function returns the reward for the move."""
        # Store previous location
        
        last_location = self.current_location
        current_score = self.grid[last_location[0],last_location[1]]
        
        # UP
        if action == 'UP':
            # If agent is at the top, stay still, collect reward
            if last_location[0] == 0:
                #reward = self.get_reward(last_location)
                reward = -1e50
            else:
                self.current_location = ( self.current_location[0] - 1, self.current_location[1])
                #modify here
                
               #########Just Delete########
                if self.grid[self.current_location[0],self.current_location[1]] != 0:
                    ##write down Score on .txt
                    self.write_only_score_on_txt()
                    future_score = self.get_reward(self.current_location)
                else:
                    self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                    future_score = self.get_reward(self.current_location)
                #####################
                #self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                #future_score = self.get_reward(self.current_location)
                
                if future_score > current_score:
                    reward = future_score
                else:
                    reward = 0

        
        # DOWN
        elif action == 'DOWN':
            # If agent is at bottom, stay still, collect reward
            if last_location[0] == self.height - 1:
               # reward = self.get_reward(last_location)
               reward = -1e50
            else:
                self.current_location = ( self.current_location[0] + 1, self.current_location[1])
                #########Just Delete########
                if self.grid[self.current_location[0],self.current_location[1]] != 0:
                    ##write down Score on .txt
                    self.write_only_score_on_txt()
                    future_score = self.get_reward(self.current_location)
                else:
                    self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                    future_score = self.get_reward(self.current_location)
                #####################
                #self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                #future_score = self.get_reward(self.current_location)
                
                if future_score > current_score:
                    reward = future_score
                else:
                    reward = 0

            
        # LEFT
        elif action == 'LEFT':
            # If agent is at the left, stay still, collect reward
            if last_location[1] == 0:
                #reward = self.get_reward(last_location)
                reward = -1e50
            else:
                self.current_location = ( self.current_location[0], self.current_location[1] - 1)
                #########Just Delete########
                if self.grid[self.current_location[0],self.current_location[1]] != 0:
                    ##write down Score on .txt
                    self.write_only_score_on_txt()
                    future_score = self.get_reward(self.current_location)
                else:
                    self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                    future_score = self.get_reward(self.current_location)
                #####################
                #self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                #future_score = self.get_reward(self.current_location)
                if future_score > current_score:
                    reward = future_score
                else:
                    reward = 0


        # RIGHT
        elif action == 'RIGHT':
            # If agent is at the right, stay still, collect reward
            if last_location[1] == self.width - 1:
                #reward = self.get_reward(last_location)
                reward = -1e50
            else:
                self.current_location = ( self.current_location[0], self.current_location[1] + 1)
               
                #########Just Delete########
                if self.grid[self.current_location[0],self.current_location[1]] != 0:
                    ##write down Score on .txt
                    self.write_only_score_on_txt()
                    future_score = self.get_reward(self.current_location)
                else:
                    self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                    future_score = self.get_reward(self.current_location)
                #####################
                
                # self.get_score(self.current_location,self.target_yield,self.oper_voltage)
                # future_score = self.get_reward(self.current_location)
                if future_score > current_score:
                    reward = future_score
                else:
                    reward = 0
                    
        # Example for Fail
        # elif action == 'RIGHT':
        #     # If agent is at the right, stay still, collect reward
        #     if last_location[1] == self.width - 1:
        #         #reward = self.get_reward(last_location)
        #         reward = -1e19
        #     else:
        #         self.current_location = ( self.current_location[0], self.current_location[1] + 1)
        #         self.get_score(self.current_location,self.target_yield,self.oper_voltage)
        #         future_score = self.get_reward(self.current_location)
        #         if future_score > current_score:
        #             reward = future_score
        #         else:
        #             reward = 0
                    
        print("reward :",reward)
        return reward
    
    
    # def check_state(self):
    #     """Check if the agent is in a terminal state (gold or bomb), if so return 'TERMINAL'"""
    #     if self.current_location in self.terminal_states:
    #         return 'TERMINAL'




# class RandomAgent():        
#     # Choose a random action
#     def choose_action(self, available_actions):
#         """Returns a random choice of the available actions"""
#         return np.random.choice(available_actions)   

# Should modify from here

class Q_Agent():
    # Intialise
    def __init__(self, environment, epsilon=0.05, alpha=0.1, gamma=1):
        self.environment = environment
        self.q_table = dict() # Store all Q-values in dictionary of dictionaries 
        for x in range(environment.height): # Loop through all possible grid spaces, create sub-dictionary for each
            for y in range(environment.width):
                self.q_table[(x,y)] = {'UP':0, 'DOWN':0, 'LEFT':0, 'RIGHT':0} # Populate sub-dictionary with zero values for possible moves

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        #print("epsilon : "+ str(self.epsilon))
        
    def choose_action(self, available_actions):
        """Returns the optimal action from Q-Value table. If multiple optimal actions, chooses random choice.
        Will make an exploratory random action dependent on epsilon."""
        if np.random.uniform(0,1) < self.epsilon:
            action = available_actions[np.random.randint(0, len(available_actions))]
        else:
            q_values_of_state = self.q_table[self.environment.current_location]
            maxValue = max(q_values_of_state.values())
            if maxValue == 0:
                action = available_actions[np.random.randint(0, len(available_actions))]
            else:
                action = np.random.choice([k for k, v in q_values_of_state.items() if v == maxValue])
        
        return action
    
    def learn(self, old_state, reward, new_state, action):
        """Updates the Q-value table using Q-learning"""
        q_values_of_state = self.q_table[new_state]
        max_q_value_in_new_state = max(q_values_of_state.values())
        current_q_value = self.q_table[old_state][action]
        
        self.q_table[old_state][action] = (1 - self.alpha) * current_q_value + self.alpha * (reward + self.gamma * max_q_value_in_new_state)
        
def play(environment, agent, trials=500, max_steps_per_episode=1000, learn=False, _voltage=0.6 , _yield=6):
    """The play function runs iterations and updates Q-values if desired."""
    reward_per_episode = [] # Initialise performance log
    
    for trial in range(trials): # Run trials
        cumulative_reward = 0 # Initialise values of each game
        step = 0
        
        #trial = episode state
        #create DB txt file
        default_dir = "."
        fileName = "scoreParamDB_operatingVlt"+str(_voltage)+"_targetYld"+str(_yield)+".txt"
        file_dir = default_dir+"/"+fileName
        f_out = open(file_dir,'a')
        
        sumOfString = "\n<<Episode["+str(trial)+"]>>"
        
        if trial == 450: #epsion : 0.2 -> 0.05
            agent.epsilon=0.05
            sumOfString += "change epsilon : 0.2 -> 0.05"
        if trial == 499:
            agent.epsilon = 0
            
        f_out.write(sumOfString.rstrip())
        
        f_out.close()
        
        #game_over = False
        #while step < max_steps_per_episode and game_over != True: # Run until max steps or until game is finished
        while step < max_steps_per_episode:
            old_state = environment.current_location
            action = agent.choose_action(environment.get_available_actions())
            
            #'UP', 'DOWN', 'LEFT', 'RIGHT'
            #if action=="UP" and old_state[0]==0:
                
            
              
            reward = environment.make_step(action)
            new_state = environment.current_location
            
            if learn == True: # Update Q-values if learning is specified
                agent.learn(old_state, reward, new_state, action)
                
            cumulative_reward += reward
            step += 1
            #if environment.check_state() == 'TERMINAL': # If game is in terminal state, game over and start next trial
            #    environment.__init__()
            #    game_over = True     
        environment.current_location=(0,0)       
        reward_per_episode.append(cumulative_reward) # Append reward for current trial to performance log
        
    return reward_per_episode # Return performance log
