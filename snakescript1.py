# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:08:07 2019

@author: DimasBelousov
"""

from dataclasses import dataclass
from gameobject import *

@dataclass
class Behavior:
    from random import choice, randint
    dir_order = [UP, LEFT, DOWN, RIGHT]
    alglen = 32
    actions = range(alglen-8)
    pop_len = 30
    mutation_rate = 1.2
    
    population : list = None
    prevdeaths : int = None
    prevcycles : int = None
    pop_index : int = 0
    pop_num : int = 0
    best_res : int = 0
    
    def mutate(self, alg, actions, score, result):
        for i in range(self.choice([0]*score*result+[1]*result)):
            index = self.randint(0, len(alg)-1)
            action = self.choice(actions)
            alg[index] = action
        return alg

    def parse(self, alg, cur, data):
        i = 0
        while i<len(alg):
            if alg[i]<4:
                i += ((data[alg[i]][1] =='self')or(data[alg[i]][1] =='barrier'))*((data[alg[i]][2] <= 10) + 1) + (data[alg[i]][1] == 'food')*3
            elif alg[i]<8:
                cur = self.dir_order[alg[i]-4]
                break
            elif alg[i]==8:
                break
            else:
                i += alg[i]-8
        return cur
    
    def run(self, kwargs: KeyWordArguments):
        data = kwargs.data
        cur = kwargs.direction
    #    alg = kwargs['alg'] if 'alg' in kwargs else None
        deaths = kwargs.deaths
        #health = kwargs['health']
        cycles = kwargs.cycles
        #print(len(kwargs))
        #print(population)
    #    print(prevdeaths, deaths)
        if not self.population:
    #        alg = list(map(int, '0 10 9 4 1 10 9 5 2 10 9 6 3 10 9 7 0 10 7 7 0 10 4 4 1 10 5 5 2 10 6 6 3 10 7 7 0 7 7 8'.split()))
    #        alg = alg + [0]*(alglen - len(alg))
            #[choice(actions) for i in range(alglen)]    
#            alg = list(map(int, '0 11 10 4 1 11 10 5 2 11 10 6 3 11 10 7 0 4 10 4 1 5 10 5 2 6 10 6 3 7 10 7 8'.split()))
            alg = [0, 11, 10, 4, 1, 11, 10, 5, 2, 11, 10, 6, 3, 11, 10, 22, 0, 4, 10, 4, 1, 5, 10, 5, 2, 6, 10, 6, 3, 7, 10, 7, 8]
            alg = alg + [0]*(self.alglen - len(alg))
            self.pop_index = 0
            #population = [[[choice(actions) for i in range(alglen)], 0] for j in range(pop_len//2)]+
            self.population = [[alg.copy(), 0] for j in range(self.pop_len)]
        if self.prevdeaths and deaths>self.prevdeaths:
            print('*', end='')
            self.population[self.pop_index][1] = self.prevcycles#+prevhealth
            self.pop_index += 1
        if self.pop_index >= self.pop_len:
            self.pop_num += 1
            print(f'\npopulation #{str(self.pop_num)}')
            succ_pop = sorted(self.population, key=lambda x: x[1])
            stat = str(succ_pop[-1][1])
            print(stat)
            f = open('stats.txt', 'r')
            line = ''.join(f.readlines())
            f.close()
            f = open('stats.txt', 'w')
            f.writelines([line+f' {stat}'])
            f.close()
            if succ_pop[-1][1] > self.best_res:
                self.best_res = int(stat)
                f = open('bestalg.txt', 'w')
                f.writelines([f'{succ_pop[-1][0].__repr__()}'])
                f.close()
            save_rate = int(self.pop_len//self.mutation_rate)
            succ_pop = succ_pop[-save_rate:]
            succ_pop = list(map(lambda x: x[0], succ_pop))
            self.population = succ_pop+[self.mutate(succ_pop[x%(save_rate)], self.actions, -x%save_rate+2, 3) for x in range(self.pop_len-save_rate)]
            self.population = list(map(lambda x: [x]+[0], self.population))
            self.pop_index = 0
        alg = self.population[self.pop_index][0]
        
        cur = self.parse(alg, cur, data)
        self.prevdeaths = deaths
        self.prevcycles = cycles
#        return (1, 1)
        return cur
