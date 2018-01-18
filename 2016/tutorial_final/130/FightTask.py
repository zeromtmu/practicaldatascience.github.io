from pybrain.rl.environments import Task
from scipy import array

class FightTask(Task):
    
    #metadata used for tracking wins and losses. Used primarily for showing the results of the algorithm
    wins = 0 
    losses = 0 
            
    def getReward(self):
        if(self.env.gameState[0] < self.currentHealth):
            if self.env.gameState[0] <= 0:   #the opponent has 0 health, the agent won
                self.env.reset()
                reward = self.env.maxHealth
                self.wins += 1
            else:
                reward = self.currentHealth - self.env.gameState[0]
        elif self.env.gameState[2] <= 0:#    the time ran out, the agent lost
            self.env.reset()
            reward = -self.env.gameState[0]
            self.losses += 1
        else:
            reward = 0.
        return reward
    
    def performAction(self, action):
        Task.performAction(self, int(action[0]))

    def getObservation(self):
        self.currentHealth = self.env.gameState[0]
        self.currentMeter = self.env.gameState[1]
        self.currentTime = self.env.gameState[2]
        self.currentDelay = self.env.gameState[3]
        
        index = self.currentHealth * self.env.maxMeter * self.env.maxTime * self.env.n + \
                self.currentMeter * self.env.maxTime * self.env.n + \
                self.currentTime * self.env.n + \
                self.currentDelay
        obs = array([index])
        return obs