from json import detect_encoding
from operator import index
from sys import argv,exit
from time import time

inputTestCase=open(argv[1])
def input():
    return inputTestCase.readline().split()

#constants

INIT_VALUE='-1'
ORK_ZONE="oz"
START_CELL='st'
END_CELL='en'
ORK_CELL='ORK'
NOT_VISITED=0
VISITED=-1
VALID_MOVES=[[-1,0],[0,1],[1,0],[0,-1]]
GONDOR='gh'
START_LORD_HOME='lordSt'
NO_ONE=-1
MAX_DEPTH=100000


#GET INPUTs
n,m= list(map(int,input()))
table=[[INIT_VALUE for i in range(m)] for j in range(n)]
startCell=list(map(int,input()))
endCell=list(map(int,input()))
table[startCell[0]][startCell[1]]=START_LORD_HOME
table[endCell[0]][endCell[1]]=GONDOR

orkZones=dict()
orkNum,lordّFriendsNum=list(map(int,input()))

def addOrkZone(x,y,power,temoOrkId):
    for i in range(x-power,x+power+1):
        for j in range(y-power,y+power+1):
         if((i>=0 and j>=0 and i<n and j<m) and table[i][j]==INIT_VALUE and (abs(x-i)+abs(y-j)<=power)):
                table[i][j]=ORK_ZONE+'-'+str(temoOrkId)
    
    orkZones[f"oz-{temoOrkId}"]=power


for i in range(orkNum):
    x,y,power=list(map(int,input()))
    table[x][y]=ORK_CELL
    addOrkZone(x,y,power,i)

friendsStartCell=dict()
for i in range(lordّFriendsNum):
    x,y=list(map(int,input()))
    table[x][y]=START_CELL+str(i)
    friendsStartCell[i]=[x,y]

friendsEndCell=dict()
for i in range(lordّFriendsNum):
    x,y=list(map(int,input()))
    table[x][y]=END_CELL+str(i)
    friendsEndCell[i]=[x,y]

#-------------------------#
def manhatanDis(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)
class State:
    numOfStates=0
    visitedStates=set()
    def __init__(self,orkZoneCurrPowers,pastZone,pathLen,lordCurrentPosition:list,remainigFriens,remainingGoals,parent,isCarry,friendWith=NO_ONE):
        State.numOfStates+=1
        self.orkZoneCurrPowers=orkZoneCurrPowers
        self.pastZone=pastZone
        self.pathLen=pathLen
        self.lordCurrentPos=lordCurrentPosition
        self.parent=parent
        self.isCarry=isCarry
        self.friendWith=friendWith
        self.remainingFriens=remainigFriens
        self.remainigGoals=remainingGoals
        self.fValue=int()
        if(parent==None):self.fValue=1
        else:self.fValue=self.f()
        #Hash part#
        tempString=str(self)
        self.id=NOT_VISITED
        if tempString in State.visitedStates:
            self.id=VISITED
        else:State.visitedStates.add(tempString)
        
         
    def __str__(self):
        # return f"{self.lordCurrentPos}-{self.isCarry}-{self.friendWith}-{self.remainingFriens}-{self.remainigGoals}"
        return f"{self.h()}-{self.lordCurrentPos}-{self.isCarry}-{self.friendWith}-{self.remainingFriens}-{self.remainigGoals}"
   
    def g(self):
        return self.pathLen
    
    def h(self):
        if(self.remainigGoals==[] and self.isCarry==False):
            return manhatanDis(self.lordCurrentPos[0],self.lordCurrentPos[1],endCell[0],endCell[1])
        
        if(self.isCarry==False):
            maxVal=0
            for i in range(len(self.remainingFriens)):
                friend=self.remainingFriens[i]
                dest=self.remainigGoals[i]
                tempVal1=manhatanDis(self.lordCurrentPos[0],self.lordCurrentPos[1],friend[0],friend[1])
                tempVal2=manhatanDis(dest[0],dest[1],friend[0],friend[1])
                tempVal3=manhatanDis(dest[0],dest[1],endCell[0],endCell[1])
                maxVal=max(tempVal1+tempVal2+tempVal3,maxVal)
            return maxVal
        else:
            tempVal1=manhatanDis(self.lordCurrentPos[0],self.lordCurrentPos[1],self.remainigGoals[self.friendWith][0],self.remainigGoals[self.friendWith][1])
            tempVal2=manhatanDis(endCell[0],endCell[1],self.remainigGoals[self.friendWith][0],self.remainigGoals[self.friendWith][1])
            return (tempVal1+tempVal2)
    def f(self):
        return (self.h())+self.g()
            
def isHomeValid(x,y):
    if x<n and y<m and 0<=x and 0<=y and table[x][y]!=ORK_CELL:
        return True
    else:return False

def isGondor(x,y):
    return (table[x][y]==GONDOR)

def detectDirection(x1,y1,x2,y2):
    if(y2-y1==+1):return ["R"]
    elif(y2-y1==-1):return ["L"]        
    elif(x2-x1==+1):return ["D"]        
    elif(x2-x1==-1):return ["U"]  

def findMin(openList:list):
    minVal=10000
    minInd=-1
    ind=0
    for i in openList:
        if(i.fValue<=minVal):
            minInd=ind
            minVal=i.fValue
        ind+=1
    return minInd
   
def printPath(state:State):
    ans=list()
    tempState=state
    while tempState.parent!=None:
        x2,y2=tempState.lordCurrentPos[0],tempState.lordCurrentPos[1]

        tempParent=tempState.parent
        x1,y1=tempParent.lordCurrentPos[0],tempParent.lordCurrentPos[1]
        tempDirection=detectDirection(x1,y1,x2,y2)
        ans=tempDirection+ans
        tempState=tempParent
    
    print("pathIs:",*ans,sep='')
    print("pathLenIs:",len(ans))
    print("numberOfVisitedStates:",State.numOfStates)
    
#-------------------------#

# #BFS PART#
def BFS():
    startTime=time()
        
    frontierList=list()
    orkZoneOriginalPows=orkZones.copy()
    frontierList.append(State(orkZones,None,0,startCell,list(friendsStartCell.values()),list(friendsEndCell.values()),None,False))

    finished=False
    while not finished: 
        tempChildren=list()
        for child in frontierList:
            if(child.id != VISITED and not finished):
                for move in VALID_MOVES:
                    tempCell=child.lordCurrentPos
                    if (isHomeValid(tempCell[0]+move[0],tempCell[1]+move[1])):
                        tempX,tempY=tempCell[0]+move[0],tempCell[1]+move[1]
                        tempRemFriends=child.remainingFriens.copy()
                        tempRemGoals=child.remainigGoals.copy()
                        tempOrkZone=child.orkZoneCurrPowers.copy()
                        zoneName=table[tempX][tempY]
                        if(isGondor(tempX,tempY) and tempRemFriends==[] and tempRemGoals==[]):
                            tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                            print("BFS finished")
                            printPath(tempState)
                            print("execution Time:",1000*(time()-startTime),"ms")
                            finished=True
                            break
                        
                        if (ORK_ZONE in zoneName):
                            if(tempOrkZone[zoneName]<=0):
                                continue
                            else:
                                if(ORK_ZONE in child.pastZone and child.pastZone!=zoneName):
                                    tempOrkZone[child.pastZone]=orkZoneOriginalPows[child.pastZone]
                                else:
                                    tempOrkZone[zoneName]-=1
                            
                        else:
                            if(child.pastZone!=None and ORK_ZONE in child.pastZone):
                                tempOrkZone[child.pastZone]=orkZoneOriginalPows[child.pastZone]
                            
                        if(child.friendWith==NO_ONE):
                            if [tempX,tempY] in tempRemFriends:
                                indexFriend=tempRemFriends.index([tempX,tempY])
                                
                                tempRemFriends.pop(indexFriend)
                                tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,True,indexFriend)
                                tempChildren.append(tempState)
                                continue
                            else:
                                
                                tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                                tempChildren.append(tempState)
                                continue
                        
                        else:#carries a friend
                            if [tempX,tempY] in tempRemGoals:
                                if(tempRemGoals[child.friendWith]==[tempX,tempY]):
                                    indexFriend=tempRemGoals.index([tempX,tempY])
                                    
                                    tempRemGoals.pop(indexFriend)
                                    tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                                    tempChildren.append(tempState)
                                    continue
                            else:
                                tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,True,child.friendWith)
                                tempChildren.append(tempState)
                                continue
        if(not finished):
            frontierList=tempChildren.copy()
            if(tempChildren==[]):
                exit("finished unsuccesfully")
                        

# #-------------------------#
# #A* PART#
def A_Star():
    startTime=time()
    Openlist=list()
    closedList=list()
    orkZoneOriginalPows=orkZones.copy()
    Openlist.append(State(orkZones,None,0,startCell,list(friendsStartCell.values()),list(friendsEndCell.values()),None,False))

    finished=False
    while Openlist!=[]:
        minNode= findMin(Openlist)
        child=Openlist.pop(minNode)
        tempChildren=list()
        if(child.id != VISITED and not finished):
            for move in VALID_MOVES:
                tempCell=child.lordCurrentPos
                if (isHomeValid(tempCell[0]+move[0],tempCell[1]+move[1])):
                    tempX,tempY=tempCell[0]+move[0],tempCell[1]+move[1]
                    tempRemFriends=child.remainingFriens.copy()
                    tempRemGoals=child.remainigGoals.copy()
                    tempOrkZone=child.orkZoneCurrPowers.copy()
                    zoneName=table[tempX][tempY]
                    if(isGondor(tempX,tempY) and tempRemFriends==[] and tempRemGoals==[]):
                        tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                        tempChildren.append(tempState)
                        print("A* finished")
                        printPath(tempState)
                        print("execution Time:",1000*(time()-startTime),"ms")
                        finished=True
                        break
                    
                    if (ORK_ZONE in zoneName):
                        if(tempOrkZone[zoneName]<=0):
                            continue
                        else:
                            if(ORK_ZONE in child.pastZone and child.pastZone!=zoneName):
                                tempOrkZone[child.pastZone]=orkZoneOriginalPows[child.pastZone]
                            else:
                                tempOrkZone[zoneName]-=1
                        
                    else:
                        if(child.pastZone!=None and ORK_ZONE in child.pastZone):
                            tempOrkZone[child.pastZone]=orkZoneOriginalPows[child.pastZone]
                        
                    if(child.friendWith==NO_ONE):
                        if [tempX,tempY] in tempRemFriends:
                            indexFriend=tempRemFriends.index([tempX,tempY])
                            
                            tempRemFriends.pop(indexFriend)
                            tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,True,indexFriend)
                            tempChildren.append(tempState)
                            continue
                        else:
                            
                            tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                            tempChildren.append(tempState)
                            continue
                    
                    else:#carries a friend
                        if [tempX,tempY] in tempRemGoals:
                            if(tempRemGoals[child.friendWith]==[tempX,tempY]):
                                indexFriend=tempRemGoals.index([tempX,tempY])
                                tempRemGoals.pop(indexFriend)
                                tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                                tempChildren.append(tempState)
                                continue
                        else:
                            tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,True,child.friendWith)
                            tempChildren.append(tempState)
                            continue
            closedList.append(child)
        if(not finished):
            Openlist= Openlist+ tempChildren.copy()
            if(Openlist==[]):
                exit("finished unsuccesfully")


#DFS PART#

finished=False
startTime=time()
def DFS(child:State,tempChildren:list,orkZoneOriginalPows,maxDepth):
    global finished
    if(child.id ==VISITED or child.pathLen>maxDepth):return 

    for move in VALID_MOVES:
        tempCell=child.lordCurrentPos
        if (isHomeValid(tempCell[0]+move[0],tempCell[1]+move[1])):
            tempX,tempY=tempCell[0]+move[0],tempCell[1]+move[1]
            tempRemFriends=child.remainingFriens.copy()
            tempRemGoals=child.remainigGoals.copy()
            tempOrkZone=child.orkZoneCurrPowers.copy()
            zoneName=table[tempX][tempY]
            if(isGondor(tempX,tempY) and tempRemFriends==[] and tempRemGoals==[]):
                tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                print("IDS finished")
                printPath(tempState)
                print("execution Time:",1000*(time()-startTime),"ms")
                finished=True
                return True
            
            if (ORK_ZONE in zoneName):
                if(tempOrkZone[zoneName]<=0):
                    continue
                else:
                    if(ORK_ZONE in child.pastZone and child.pastZone!=zoneName):
                        tempOrkZone[child.pastZone]=orkZoneOriginalPows[child.pastZone]
                    else:
                        tempOrkZone[zoneName]-=1
                
            else:
                if(child.pastZone!=None and ORK_ZONE in child.pastZone):
                    tempOrkZone[child.pastZone]=orkZoneOriginalPows[child.pastZone]
                
            if(child.friendWith==NO_ONE):
                if [tempX,tempY] in tempRemFriends:
                    indexFriend=tempRemFriends.index([tempX,tempY])
                    tempRemFriends.pop(indexFriend)
                    tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,True,indexFriend)
                    tempChildren.append(tempState)
                    continue
                else:
                    tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                    tempChildren.append(tempState)
                    continue
            
            else:#carries a friend
                if [tempX,tempY] in tempRemGoals:
                    if(tempRemGoals[child.friendWith]==[tempX,tempY]):
                        indexFriend=tempRemGoals.index([tempX,tempY])
                        
                        tempRemGoals.pop(indexFriend)
                        tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,False)
                        tempChildren.append(tempState)
                        continue
                else:
                    tempState=State(tempOrkZone,zoneName,child.pathLen+1,[tempX,tempY],tempRemFriends,tempRemGoals,child,True,child.friendWith)
                    tempChildren.append(tempState)
                    continue

def IDS():
    global finished
    frontierList=list()
    orkZoneOriginalPows=orkZones.copy()
    frontierList.append(State(orkZones,None,0,startCell,list(friendsStartCell.values()),list(friendsEndCell.values()),None,False))
    tempLen=0
    while(not finished): 
        tempChildren=list()
        for child in frontierList:
            ans=DFS(child,tempChildren,orkZoneOriginalPows,tempLen)
            tempLen+=1
            if(ans==True):
                break
        frontierList=tempChildren.copy()
        if(tempChildren==[]):
            exit("finished unsuccesfully")
                        

#-----------------#                

A_Star()
# BFS()
# IDS()