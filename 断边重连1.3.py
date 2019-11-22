import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
#import xlwt
b = 1.04 #Temptation
N = 50#define the number of players
SIZE = N*N
G = nx.grid_2d_graph(N, N, periodic=True)
K = 0.1 # Noise
MCS = 20# Define the Monte Carlo steps
file = open('frequency.txt',mode = 'w')
f = open('test.gexf',mode='wb')

for i in range(N):
    for j in range(N):
        G.nodes[(i,j)]['strategy'] = random.randint(0,1)#Initial the strategy of every player
def Cal_payoff(G,player):
    L = nx.all_neighbors(G,player)#Get all the neighbors of the choosen player
    strate = G.nodes[player]['strategy']#Get strategy of the chooosen player
    payoff  = 0#Initial the payoff
    for i in L:#Calculate the payoff
        if strate == 1:
            if G.nodes[i]['strategy'] == 1:
                payoff = payoff + 0
            else:
                payoff  = payoff + b
        else:
            if G.nodes[i]['strategy'] == 1:
                payoff = payoff + 0
            else:
                payoff  = payoff + 1
    return payoff
# Star Monte Carlo Steps
'''
def relink(G,player):
    
    L = nx.all_neighbors(G,player)
    L = list(L)
    min_pay_neighbor = min_payoff_neighbor(G,player)
    G.remove_edge(player,min_pay_neighbor)#remove
    

    L_2_order = two_order_neighbors(G,player)
    L_2_order = list(L_2_order)
    pay_list = []
    for i in L_2_order:
        p = Cal_payoff(G,i)
        pay_list.append(p)
    max_index = pay_list.index(max(pay_list))
    G.add_edge(player,L_2_order[max_index])#add
    
def two_order_neighbors(G,player):
    L = nx.all_neighbors(G,player)
    L = list(L)
    L_two = []
    for i in L:
        for j in list(nx.all_neighbors(G,i)):
            L_two.append(j)
        
    L_two = list(set(L_two))
    #L_two.remove(player)
    return L_two
    
def min_payoff_neighbor(G,player):
    L = nx.all_neighbors(G,player)
    L = list(L)
    pay = []
    for i in L:
        p =Cal_payoff(G,i)
        pay.append(p)
    min_index = pay.index(min(pay))
    return L[min_index]
'''
def relink(G,player,min_nei):
    
    #L = nx.all_neighbors(G,player)
    #L = list(L)
    #min_pay_neighbor = min_payoff_neighbor(G,player)
    
    

    L_2_order = two_order_neighbors(G,player,min_nei)
    L_2_order = list(L_2_order)
    pay_list = []
    for i in L_2_order:
        p = Cal_payoff(G,i)
        pay_list.append(p)
        #print('fuck')
    max_index = pay_list.index(max(pay_list))
    if(L_2_order[max_index] in list(nx.all_neighbors(G,player))):
        pass
    else:
        G.add_edge(player,L_2_order[max_index])#add
        G.remove_edge(player,min_nei)#remove
    
def two_order_neighbors(G,player,min_nei):
    L = nx.all_neighbors(G,min_nei)
    L = list(L)        
    L.remove(player)
    return L
def min_payoff_neighbor(G,player):
    L = nx.all_neighbors(G,player)
    L = list(L)
    pay = []
    for i in L:
        p =Cal_payoff(G,i)
        pay.append(p)
    min_index = pay.index(min(pay))
    return L[min_index]
def Cal_cooperation(G):
    cooperator = 0
    for i in range(N):
        for j in range(N):
            if G.nodes[(i,j)]['strategy'] == 0:
                cooperator += 1
    fraction = cooperator/(N*N)
    return fraction

for k in range(MCS):
    for i in range(N):
        for j in range(N):
            #player = random.randint(0,N-1)#Choose a random player
            rand_i = random.randint(0,N-1)
            rand_j = random.randint(0,N-1)
            player = (rand_i,rand_j)
            payoff_player = Cal_payoff(G,player)
            L = nx.all_neighbors(G,player)
            L = list(L)
            length = len(L)
            '''
            nei = list(nx.all_neighbors(G,player))
            print(nei)
            print("\n")
            '''
            random_neighbor = L[random.randint(0,length-1)]
            payoff_neighbor = Cal_payoff(G,random_neighbor)
            if G.nodes[player]['strategy'] !=G.nodes[random_neighbor]['strategy']:
                random_num = random.random()
                try:
                    Fermi_value = 1/(1+math.exp((payoff_player - payoff_neighbor)/K))
                except OverflowError:
                    Fermi_value = 0
                if (random_num <= Fermi_value):
                    G.nodes[player]['strategy'] = G.nodes[random_neighbor]['strategy']
            
            
            #two_nei = two_order_neighbors(G,player)
            min_nei = min_payoff_neighbor(G,player)
            #nei = list(nx.all_neighbors(G,player))
            if(len(list(nx.all_neighbors(G,min_nei)))>=2):#最小收益邻居的邻居数大于1
                #G.remove_edge(player,min_nei)
                relink(G,player,min_nei)
            else:
                pass
            #print(nei)
            #print("\n")
    fraction = Cal_cooperation(G)
    print(fraction)
    #file.write(str(fraction)+'\n')
file.close()
#nx.draw(G,node_size = 1)
#plt.show()
nx.write_gexf(G,f)
f.close()
