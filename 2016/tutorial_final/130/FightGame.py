from pybrain.utilities import Named
from pybrain.rl.environments.environment import Environment

from collections import Counter
from random import random, choice
from enum import Enum

#Defines the kind of attack that is done
class Attack(Enum):
    high = 0
    low = 1
    unblockable = 2
    delay = 3


class FightGame(Environment, Named):
    # attacks. Notation is (<high/low/unblockable/misc>, damage, meter gain, startup)
    high = (Attack.high, 2, 2, 2)
    low = (Attack.low, 1, 1, 1)
    special = (Attack.unblockable, 10, -5, 4)
    delay = (Attack.delay, 0, 0, 1)

    allActions = [high, low, special,delay]

    blockTable = None
    history = None
    
    maxHealth = 0   #the maximum health
    maxMeter = 10   #the maximum meter
    maxTime = 0     #the starting time
    n = 0           #the amount of history we remember
    maxDelay = 0    #the maximum amount of time where delay is meaningful. For simplicity this will be n
    
    startState = None
    gameState = None

    def __init__(self, blockTable, n, startingHealth, startingMeter, startingTime, **args):
        self.setArgs(**args)
        self.blockTable = blockTable

        self.maxHealth = startingHealth
        self.maxMeter = 10
        self.maxTime = startingTime
        self.n = n
        self.maxDelay = self.n
        
        self.history = (Attack.delay,) * n
        if self.startState == None:
            self.startState = (startingHealth, startingMeter, startingTime, 0)
        self.reset()
        
    def getSensors(self):
        obs = zeros(1)
        obs[0] = self.gameState
        return obs
    
    def reset(self):
        self.gameState = self.startState

    def randomBlock(self):
        block = choice([Attack.high, Attack.low])
        return block
        
    def performAction(self, action):
        currentHealth = self.gameState[0]
        currentMeter = self.gameState[1]
        currentTime = self.gameState[2]
        currentDelay = self.gameState[3]

        attack = self.allActions[action]
        attackType = attack[0]
        attackDamage = attack[1]
        attackMeter = attack[2]
        attackTime = attack[3]
        
        newHealth = max(currentHealth - attackDamage, 0)
        newMeter = min(currentMeter + attackMeter, self.maxMeter)
        newTime = max(currentTime - attackTime,0)
        newDelay = currentDelay + attackTime % self.n

        if(self.history not in self.blockTable):
            blockType = self.randomBlock()
        else:
            timeIndex = (currentDelay + attackTime - 1) % len(self.blockTable[self.history])
            blockType = self.blockTable[self.history][timeIndex]
        
        self.history = self.history[1:] + (attackType, )
            
        if attackType == Attack.delay:
            self.gameState = (newHealth, newMeter, newTime, newDelay)
        if attackType == Attack.unblockable:
            if(newMeter >= 0):
                self.gameState = (newHealth, newMeter, newTime, 0)
            else:
                self.gameState = (currentHealth, currentMeter, newTime, newDelay)
        if attackType == Attack.high:
            if(blockType == Attack.high):
                self.gameState = (currentHealth, currentMeter, newTime, 0)
            else:
                self.gameState = (newHealth, newMeter, newTime, 0)
        if attackType == Attack.low:
            if(blockType == Attack.low):
                self.gameState = (currentHealth, currentMeter, newTime, 0)
            else:
                self.gameState = (newHealth, newMeter, newTime, 0)