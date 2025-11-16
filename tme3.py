import numpy as np
import math

class Bandit:
    def __init__(self, n:int):
        self.bandits = np.random.rand(n)  

    def play(self, i: int) -> int:
        if i < 0 or i >= len(self.bandits):
            print("Numéro de machine invalide")
        if np.random.rand() < self.bandits[i]:
            return 1
        return 0

class AgentBanditRandom:
    def __init__(self, n:int):
        self.times = [0 for i in range(n)]
        self.rewards = [0 for i in range(n)]
        self.rewards_t=[]

    def play(self,n):
        return np.random.randint(0,len(self.times))  

    def reward(self, i:int,r:int):
        self.times[i]+=1
        self.rewards[i]+=r
        self.rewards_t.append(r)

    def reset(self):
        self.times = [0 for i in range(len(self.times))]
        self.rewards = [0 for i in range(len(self.times))]


class JeuBandit:
    def __init__(self, Bandit,agent):
        self.rewards=[0 for i in range(len(agent.times))]
        self.rewards_t=[]
        self.bandit=Bandit
        self.agent=agent

    def reset(self):
        self.agent.reset()

    def play(self,n:int):
        self.reset()
        for i in range(n):
            coup=self.agent.play(n)
            self.agent.reward(coup,self.bandit.play(coup))
        self.rewards=self.agent.rewards
        self.rewards_t=self.agent.rewards_t


class AgentGlouton:
    def __init__(self, n:int):
         self.times = [0 for i in range(n)]
         self.rewards=[0 for i in range(n)]
         self.rewards_t=[]

    def play(self,n):
        if sum(self.times)<n//10:
            return np.random.randint(0,len(self.times))  
        else:
            prob=[0.5 if self.times[i]==0 else self.rewards[i]/self.times[i] for i in range(len(self.times))]
            return np.argmax(prob)

    def reward(self, i:int,r:int):
        self.times[i]+=1
        self.rewards[i]+=r
        self.rewards_t.append(r)

    def reset(self):
        self.times = [0 for i in range(len(self.times))]
        self.rewards = [0 for i in range(len(self.times))]



class AgentEpsilon:
    def __init__(self, n:int ,epsilon):
         self.times = [0 for i in range(n)]
         self.rewards=[0 for i in range(n)]
         self.epsilon=epsilon
         self.rewards_t=[]

    def play(self,n):
        if sum(self.times)<n//10:
            return np.random.randint(0,len(self.times))  
        else:
            if np.random.rand() < self.epsilon :
                return np.random.randint(0,len(self.times))  
            else: 
                prob=[0.5 if self.times[i]==0 else self.rewards[i]/self.times[i] for i in range(len(self.times))]
                return np.argmax(prob)

    def reward(self, i:int,r:int):
        self.times[i]+=1
        self.rewards[i]+=r
        self.rewards_t.append(r)

    def reset(self):
        self.times = [0 for i in range(len(self.times))]
        self.rewards = [0 for i in range(len(self.times))]
    


class AgentUCB:
    def __init__(self, n:int,K):
         self.times = [0 for i in range(n)]
         self.rewards=[0 for i in range(n)]
         self.rewards_t=[]
         self.K=K

    def play(self,n):
        prob=[0.5 if self.times[i]==0 else self.rewards[i]/self.times[i]+math.sqrt(self.K*math.log(sum(self.times))/self.times[i]) for i in range(len(self.times))]
        
        return np.argmax(prob)

    def reward(self, i:int,r:int):
        self.times[i]+=1
        self.rewards[i]+=r
        self.rewards_t.append(r)

    def reset(self):
        self.times = [0 for i in range(len(self.times))]
        self.rewards = [0 for i in range(len(self.times))]

def regret(bandit,rewards_t):
    #M=max(bandit.bandits)
    #return [(M*i)-np.sum(rewards_t[range(i)]) for i in range(len(bandit.bandits))]
    
    M = max(bandit.bandits)
    
    regrets = []
    cumulative_reward = 0
    
    for t in range(len(rewards_t)):
        
        cumulative_reward += rewards_t[t]
        
        optimal_reward = M * (t + 1)
        regrets.append(optimal_reward - cumulative_reward)
    
    return regrets

        



