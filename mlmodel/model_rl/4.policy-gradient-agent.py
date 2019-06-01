#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()




# In[3]:

class Model:
    def __init__(self,
        state_size,
        window_size,
        trend,
        skip,
        iterations,
        initial_reward
    ):
        self.agent = Agent(state_size, window_size, trend, skip)
        self.iterations = iterations
        self.initial_reward = initial_reward

class Agent:

    LEARNING_RATE = 1e-4
    LAYER_SIZE = 256
    GAMMA = 0.9
    OUTPUT_SIZE = 3

    def __init__(self, state_size, window_size, trend, skip):
        self.state_size = state_size
        self.window_size = window_size
        self.half_window = window_size // 2
        self.trend = trend
        self.skip = skip
        self.X = tf.placeholder(tf.float32, (None, self.state_size))
        self.REWARDS = tf.placeholder(tf.float32, (None))
        self.ACTIONS = tf.placeholder(tf.int32, (None))
        feed_forward = tf.layers.dense(self.X, self.LAYER_SIZE, activation = tf.nn.relu)
        self.logits = tf.layers.dense(feed_forward, self.OUTPUT_SIZE, activation = tf.nn.softmax)
        input_y = tf.one_hot(self.ACTIONS, self.OUTPUT_SIZE)
        loglike = tf.log((input_y * (input_y - self.logits) + (1 - input_y) * (input_y + self.logits)) + 1)
        rewards = tf.tile(tf.reshape(self.REWARDS, (-1,1)), [1, self.OUTPUT_SIZE])
        self.cost = -tf.reduce_mean(loglike * (rewards + 1)) 
        self.optimizer = tf.train.AdamOptimizer(learning_rate = self.LEARNING_RATE).minimize(self.cost)
        self.sess = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())
    
    def predict(self, inputs):
<<<<<<< HEAD
        return self.sess.run(self.logits, feed_dict={self.X:inputs})
    
    def get_state(self, t):
=======
        return self.sess.run(self.logits, feed_dict={self.X: inputs})

    def get_state(self, t, reward_state=None):
>>>>>>> c81ce4ab269c757d23c6940d74d5734a3ab7a470
        window_size = self.window_size + 1
        d = t - window_size + 1
        block = self.trend[d : t + 1] if d >= 0 else -d * [self.trend[0]] + self.trend[0 : t + 1]
        res = []
        for i in range(window_size - 1):
            res.append(block[i + 1] - block[i])
        return np.array([res])
    
    def discount_rewards(self, r):
        discounted_r = np.zeros_like(r)
        running_add = 0
        for t in reversed(range(0, r.size)):
            running_add = running_add * self.GAMMA + r[t]
            discounted_r[t] = running_add
        return discounted_r
    
    
    def get_predicted_action(self, sequence):
        prediction = self.predict(np.array(sequence))[0]
        return np.argmax(prediction)
    
    
    def predict_sequence(self, do_action, result_list  ):
        """
          Generate the states, and get action result intoList
        
          dict_res = {         "starting_money" = initial_money
             "states_sell"    = []
             "states_buy"     = []
             "inventory      = []
          result_list = [ dict_res ]
    
        
        """
        state       = self.get_state(0)
        #result_list = []
        
        for t in range(0, len(self.trend) - 1, self.skip):
            action     = self.get_predicted_action(state)
       
            dict_res = do_action(state, action, result_list )  # dict_res
            result_list.append( dict_res )


            next_state = self.get_state(t + 1, dict_res["reward_state"])
            state = next_state



    def buy(self, initial_money):
        starting_money = initial_money
        states_sell    = []
        states_buy     = []
        inventory      = []
        
        
        state = self.get_state(0)
        for t in range(0, len(self.trend) - 1, self.skip):
            action     = self.get_predicted_action(state)
            
            ###### do_action ########################################
            if action == 1 and initial_money >= self.trend[t] and t < (len(self.trend) - self.half_window):
                inventory.append(self.trend[t])
                initial_money -= self.trend[t]
                states_buy.append(t)
                print('day %d: buy 1 unit at price %f, total balance %f'% (t, self.trend[t], initial_money))
                
                
            elif action == 2 and len(inventory):
                bought_price = inventory.pop(0)
                initial_money += self.trend[t]
                states_sell.append(t)
                try:
                    invest = ((close[t] - bought_price) / bought_price) * 100
                except:
                    invest = 0
                print(
                    'day %d, sell 1 unit at price %f, investment %f %%, total balance %f,'
                    % (t, close[t], invest, initial_money)
                )
            ########################################################
            next_state = self.get_state(t + 1)
            state = next_state
            
        invest = ((initial_money - starting_money) / starting_money) * 100
        total_gains = initial_money - starting_money
        return states_buy, states_sell, total_gains, invest
        
    
    def train(self, iterations, checkpoint, initial_money):
        for i in range(iterations):
            ep_history = []
            total_profit = 0
            inventory = []
            state = self.get_state(0)
            starting_money = initial_money
            
            
            for t in range(0, len(self.trend) - 1, self.skip):
                action = self.get_predicted_action(state)
                next_state = self.get_state(t + 1)
                
                
                ######## do_action ###################################
                if action == 1 and starting_money >= self.trend[t] and t < (len(self.trend) - self.half_window):
                    inventory.append(self.trend[t])
                    starting_money -= close[t]
                
                elif action == 2 and len(inventory):
                    bought_price = inventory.pop(0)
                    total_profit += self.trend[t] - bought_price
                    starting_money += self.trend[t]
                ###################################################
                
                
                ep_history.append([state,action,starting_money,next_state])
                state = next_state
            ep_history = np.array(ep_history)
            ep_history[:,2] = self.discount_rewards(ep_history[:,2])
            cost, _ = self.sess.run([self.cost, self.optimizer], feed_dict={self.X:np.vstack(ep_history[:,0]),
                                                    self.REWARDS:ep_history[:,2],
                                                    self.ACTIONS:ep_history[:,1]})
            if (i+1) % checkpoint == 0:
                print('epoch: %d, total rewards: %f.3, cost: %f, total money: %f'%(i + 1, total_profit, cost,
                                                                                  starting_money))

#https://stackoverflow.com/questions/2597278/python-load-variables-in-a-dict-into-namespace
class Bunch(object):
  def __init__(self, adict):
    self.__dict__.update(adict)



def action_example(data_frame, action_dict, inventory=[]):
    x = Bunch(action_dict)

    if x.action == 1 and x.starting_reward >= x.trend[x.iteration_number] and x.iteration_number < (len(x.trend) - x.half_window):
        inventory.append(x.trend[x.iteration_number])
        x.starting_reward -= data_frame[x.iteration_number]
    elif x.action == 2 and len(inventory):
        x.bought_price = inventory.pop(0)
        x.total_reward += x.trend[x.iteration_number] - x.bought_price
        x.starting_reward += x.trend[x.iteration_number]
    return x.starting_reward, x.total_reward
          

def fit(model, data_frame, do_action):
    agent = model.agent
    for i in range(model.iterations):
        ep_history = []
        total_reward = 0
        inventory = [] # passed by reference
        state = agent.get_state(0)
        starting_reward = model.initial_reward
        
        
        for t in range(0, len(agent.trend) - 1, agent.skip):
            action = agent.get_predicted_action(state)
            next_state = agent.get_state(t + 1)
            
            
            ######## do_action ###################################
            action_dict = {"starting_reward": starting_reward, "action": action, "trend": data_frame, "half_window": agent.half_window, "iteration_number": t, "total_reward": total_reward}
            reward, total_reward = do_action(data_frame, action_dict, inventory=inventory)

            ###################################################
            ep_history.append([state,action,reward,next_state])
            state = next_state
        ep_history = np.array(ep_history)
        ep_history[:,2] = agent.discount_rewards(ep_history[:,2])
        cost, _ = agent.sess.run([agent.cost, agent.optimizer], feed_dict={agent.X:np.vstack(ep_history[:,0]),
                                                agent.REWARDS:ep_history[:,2],
                                                agent.ACTIONS:ep_history[:,1]})
        if (i+1) % 10 == 0:
            print('epoch: %d, total rewards: %f.3, cost: %f, total money: %f'%(i + 1, total_reward, cost,
                                                                                starting_reward))

    return agent.sess


def predict(model, sess, data_frame, do_action):
    model.agent.sess = sess
    return model.agent.predict_sequence(do_action, []) #TODO needs an example function to work

def test(filename= 'dataset/GOOG-year.csv'):
    df = pd.read_csv('../dataset/GOOG-year.csv')
    close = df.Close.values.tolist()
    model = Model(window_size, window_size, close, skip, 200, initial_money)
    sess = fit(model, close, action_example)
    agent.sess = sess
    states_buy, states_sell, total_gains, invest = agent.buy(initial_money = initial_money)
    result_list = predict(model, sess, close, action_example)


if __name__ == "__main__":


    # In[2]:


    df = pd.read_csv('../dataset/GOOG-year.csv')
    df.head()


    # In[4]:


    close = df.Close.values.tolist()
    initial_money = 10000
    window_size = 30
    skip = 1
    agent = Agent(state_size = window_size,
                window_size = window_size,
                trend = close,
                skip = skip)
    #agent.train(iterations = 200, checkpoint = 10, initial_money = initial_money)


    # In[5]:


    

    # In[6]:
    model = Model(window_size, window_size, close, skip, 200, initial_money)
    sess = fit(model, close, action_example)
    agent.sess = sess
    states_buy, states_sell, total_gains, invest = agent.buy(initial_money = initial_money)
    test()
    fig = plt.figure(figsize = (15,5))
    plt.plot(close, color='r', lw=2.)
    plt.plot(close, '^', markersize=10, color='m', label = 'buying signal', markevery = states_buy)
    plt.plot(close, 'v', markersize=10, color='k', label = 'selling signal', markevery = states_sell)
    plt.title('total gains %f, total investment %f%%'%(total_gains, invest))
    plt.legend()
    plt.show()
    


    # In[ ]:




