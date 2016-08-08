import mountaincar
from Tilecoder import *
#from Tilecoder import numTiles as n
from pylab import *  #includes numpy
from numpy import *


sizeOfTilings = 9 * 9
numTiles = numTilings * sizeOfTilings
numRuns = 1
numEpisodes = 1000
alpha = 0.5/numTilings
gamma = 1
lmbda = 0.9
Epi = Emu = epsilon = 0
Emu = 0.1
n = numTiles * 3
F = [-1]*numTilings
F2 = [-1]*numTilings
theta = [0] * n
#Calculates the inner product tetha and a given action and state
def innerProduct(theta,state,action,F2):
    #tilecode(state[0],state[1],F2)
    innerProduct = 0
    for features in F2:
        innerProduct += theta[features + (action* numTiles)]
    return innerProduct

#Will find the greedy action of a state
def greedyAction(state):
    Q = [0,0,0]
    
    tilecode(state[0],state[1],F2)
    #Finding Q(s,a) for all actions 
    for features in F2:
                
        #Summing up values for deceleration
        Q[0] += theta[features]
        #Summing up values for coasting 
        Q[1] += theta[features + numTiles]
        #Summing up values for accerlation
        Q[2] += theta[features + (2*numTiles)]
    return argmax(Q)

#Find the probailiy of taking an action in a state under a policy    
def policy(action, nextState):
    greedAction = greedyAction(nextState)
    probGreedy = (1-Epi) + (Epi)/2
    if action == greedyAction:
        return probGreedy
    else:
        return 1- probGreedy 

#Caluates the sum term for a policy         
def policySum(nextState,theta):
    sum = 0
    tilecode(nextState[0],nextState[1],F2)
    for a in range(3):
        sum+= policy(a,nextState) * innerProduct(theta,nextState,a,F2) 
    return sum 
    
#Calulate the new delta
def deltaCalc(R,action,state, nextState,theta, delta):
    #return R + (lmbda*policySum(action,nextState,theta)) - innerProduct(theta,state,action)
    return delta + policySum(nextState,theta) 

def Qs(F):
    Q = [0,0,0]
    
    
    #Finding Q(s,a) for all actions 
    for features in F:
                
        #Summing up values for deceleration
        Q[0] += theta[features]
        #Summing up values for coasting 
        Q[1] += theta[features + numTiles]
        #Summing up values for accerlation
        Q[2] += theta[features + (2*numTiles)]
    return Q
    
def writeF():
    fout = open('value', 'w')
    F = [0]*numTilings
    steps = 50
    for i in range(steps):
        for j in range(steps):
            tilecode(-1.2+i*1.7/steps, -0.07+j*0.14/steps, F)
            height = -max(Qs(F))
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()



runSum = 0.0
for run in xrange(numRuns):
    theta = -0.1* rand(n)
  
    returnSum = 0.0
    for episodeNum in xrange(numEpisodes):
        G = 0
        state = mountaincar.init()
        e = 0 *rand(n)
        step = 0
        
      
        #Going until a terminal state
        while state != None:
            
            #Getting the feature vector
            tilecode(state[0],state[1],F)
            
           
            
            Q = [0,0,0]
            #Finding Q(s,a) for all actions 
            for features in F:
                
                #Summing up values for deceleration
                Q[0] += theta[features]
               
                #Summing up values for coasting 
                Q[1] += theta[features + numTiles]
             
                #Summing up values for accerlation
                Q[2] += theta[features + (2*numTiles)]
              
            #Selecting action to take
            if rand() <= Emu:
                action = randint(3)
            else:
                action = argmax(Q)
               
            
            #Taking the action. Store results  
            result = mountaincar.sample(state,action)
            G += result[0]
            nextState = result[1]
           
            #Calculating delta
            delta = result[0] - Q[action]
            
            
            #Updating traces
            for features in F:
                e[features + (action *numTiles)] = 1;
            
            #Breaking out if next state is none
            if nextState == None:
                theta = theta + (alpha * delta * e)
                break
          
           
            #updating values
            delta = deltaCalc(result[0],action,state,nextState,theta,delta)
            theta = theta + ((alpha * delta) * e)
            e = e * lmbda
            state = nextState
            step+=1
              
            
        print "Episode: ", episodeNum, "Steps:", step, "Return: ", G
        returnSum = returnSum + G
        writeF()
    print "Average return:", returnSum/numEpisodes
    writeF()
    runSum += returnSum
print "Overall performance: Average sum of return per run:", runSum/numRuns
writeF()



