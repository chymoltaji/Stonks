import csv
import random as rand
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
#changes
#global variables
uniqueDict={}
gameover=True
start=0
finish=0
playerBidsList={
'Bid':[],
'Unique rank':[],
'# of unique bids lower':[],
'# of unique bids higher':[],
'# of lower numbers unused':[]
}
maxBid=10000
funds=10000
total=0
winning=2

#resets all the game variables for a new game
def resetGame():
    global uniqueDict
    global gameover
    global start
    global finish
    global playerBidsList
    global total
    global winning
    uniqueDict={x:[] for x in range(1, maxBid)}
    gameover=False
    start=datetime.now()
    finish=start+timedelta(minutes=1)
    playerBidsList={
    'Bid':[],
    'Unique rank':[],
    '# of unique bids lower':[],
    '# of unique bids higher':[],
    '# of lower numbers unused':[]
    }
    total=0
    winning=2
    with open('bidsFile.csv','w+') as bidsFile:
        bidsFile.close()

#enter a user and a bid into a csv file. "p" is either bot or player01
#this is meant to be replaced by a live database
def registerBid(p,bid):
    with open('bidsFile.csv','a',newline='') as bidsFile:
        bidLine=csv.writer(bidsFile)
        bidLine.writerow([p, bid, datetime.now()])
        bidsFile.close()

#finds whether a bid is the lowest unique bid and returns list
def isLowestUnique(p, bid):
    global uniqueDict
    global playerBidsList
    global winning
    uniqueDict[bid].append(p)
    winning=2
    if len(uniqueDict[bid])==1:
        if p=='player01':
            winning=True
            #TODO display you are winning
    elif len(uniqueDict[bid])>1:
        print('not unique')
        if uniqueDict[bid][0]=='player01':
            winning=False
        print(f'informing {uniqueDict[bid][0]}')
    else:
        print('not unique')

def addBid2Dict(bid):
    global playerBidsList
    playerBidsList['Bid'].append(bid)
    playerBidsList['Unique rank'].append('0')
    playerBidsList['# of unique bids lower'].append('0')
    playerBidsList['# of unique bids higher'].append('0')
    playerBidsList['# of lower numbers unused'].append('0')

def updateDict():
    global playerBidsList
    for i in range(len(playerBidsList['Bid'])):
        bid=playerBidsList['Bid'][i]
        countLow=0
        countHigh=0
        countUnused=0
        uniqueness=len(uniqueDict[bid])
        if uniqueness==1:
            rank=0
            for j in range(bid):
                unik=len(uniqueDict[j+1])
                if unik==1:
                    rank+=1
            playerBidsList['Unique rank'][i]=rank
            #TODO make actual rank
        elif uniqueness>1:
            playerBidsList['Unique rank'][i]='N'
        for j in range(bid):
            unik=len(uniqueDict[j+1])
            if unik==1:
                countLow+=1
            elif unik==0:
                countUnused+=1
        playerBidsList['# of unique bids lower'][i]=countLow-1
        playerBidsList['# of lower numbers unused'][i]=countUnused
        for k in range(int(bid),maxBid):
            if len(uniqueDict[k])==1:
                countHigh+=1
        playerBidsList['# of unique bids higher'][i]=countHigh-1
       
#registers and processes human bid, launches bot bids
def processBid(bid):
    global playerBidsList
    global uniqueDict
    global funds
    global total
    funds-=bid
    registerBid('player01', bid)
    isLowestUnique('player01', bid)
    addBid2Dict(bid)
    updateDict()
    total=gameTotal()

#sums total amount winnable in the game right now
def gameTotal():
    bidsList=open('bidsFile.csv','r')
    winTotal=0
    for row in bidsList:
        col=row.split(',')
        cellValue=int(col[1])
        winTotal+=cellValue
    return int(winTotal)

##################################################
###################GUI SECTION####################
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV#
#some formating information for UX
bgMain='#67C391'
fgMain='#F9F6F4'
bgSec=fgMain
fgSec='#508B66'

#clears the main frame of the root window
def refreshFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#launches the game backend and enters game interface
def startGame(value,container):
    if value == True:
        resetGame()
        refreshFrame(container)
        bidding(container)

#creates a launch page with start game button
def introduction(container):
    startButton=tk.Button(container, text="Start Game", command=lambda: startGame(True,container))
    startButton.pack()

def bidding(container):
    bidding.bidValue=100
    def slider(value):
        bidding.bidValue=int(round(float(value)))
        bidLabel.config(text=bidding.bidValue)
        submit.config(text=f'Bid ${bidding.bidValue}')
    def spinBox(change):
        bidding.bidValue+=change
        bidLabel.config(text=bidding.bidValue)
        submit.config(text=f'Bid ${bidding.bidValue}')
    def send(bid):
        global winning
        processBid(bid)
        updateLabels()
        popUpResult(winning, bid)

    def tableFormat():
        length=len(playerBidsList["Bid"])
        b,u,l,h,x=[],[],[],[],[]
        for i in range(length):
            b.append(str(playerBidsList["Bid"][i])+" "*(5-len(str(playerBidsList["Bid"][i]))))
            u.append(str(playerBidsList["Unique rank"][i])+" "*(5-len(str(playerBidsList["Unique rank"][i]))))
            l.append(str(playerBidsList["# of unique bids lower"][i])+" "*(5-len(str(playerBidsList["# of unique bids lower"][i]))))
            h.append(str(playerBidsList["# of unique bids higher"][i])+" "*(5-len(str(playerBidsList["# of unique bids higher"][i]))))
            x.append(str(playerBidsList["# of lower numbers unused"][i])+" "*(5-len(str(playerBidsList["# of lower numbers unused"][i]))))
        b='|'.join([str(v) for v in b])
        u='|'.join([str(v) for v in u])
        l='|'.join([str(v) for v in l])
        h='|'.join([str(v) for v in h])
        x='|'.join([str(v) for v in x])
        table=f'''
        Your bids----------------|{b}
        Unique rank-------------|{u}
        # of uniques lower------|{l}
        # of uniques higher-----|{h}
        # of lower bids unused--|{x}
        '''
        return table

    def updateLabels():
        avaiLabel.config(text=f'Available funds: {funds}')
        winLabel.config(text=f'Amount winnable: {total}')
        text=tableFormat()
        bids.config(text=text)

    #TODO sync with win tracking
    def popUpResult(winning, bid):
        if winning:
            messagebox.showinfo('Information', f'Your bid is currently winning: ${total}')
        elif not winning:
            messagebox.showinfo('Information', f'Your bid of ${bid} did not win')

    avaiLabel=ttk.Label(container,text=f'Available funds: {funds}')
    winLabel=ttk.Label(container, text=f'Amount winnable: {total}')
    bidLabel=ttk.Label(container, text=bidding.bidValue)
    scale=ttk.Scale(container, length=400,from_=1, to=funds, command=slider)
    upButton=ttk.Button(container, text='^', command=lambda: spinBox(1))
    downButton=ttk.Button(container, text='V', command=lambda: spinBox(-1))
    submit=ttk.Button(container, text=f'Bid ${bidding.bidValue}', command=lambda: send(bidding.bidValue))
    frame=ttk.Frame(container)
    bids=ttk.Label(frame, text=f'''
    Your bids----------------{playerBidsList["Bid"]}
    Unique rank--------------{playerBidsList["Unique rank"]}
    # of uniques lower-------{playerBidsList["# of unique bids lower"]}
    # of uniques higher------{playerBidsList["# of unique bids higher"]}
    # of lower bids unused---{playerBidsList["# of lower numbers unused"]}
    ''')

    avaiLabel.pack()
    winLabel.pack()
    bidLabel.pack()
    scale.pack()
    upButton.pack()
    downButton.pack()
    submit.pack()
    frame.pack()
    bids.pack()
    
def userStats(container):
    pass

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
###################GUI SECTION####################
##################################################

def main():
    root = tk.Tk()
    root.title('$tonks')
    root.config(background=bgMain)
    root.state('zoomed')
    root.resizable(False,False)

    def updateTimer():
        global finish
        global gameover
        if finish:
            remainingTime=finish-datetime.now()
            remainingTime=str(remainingTime).split(':')
            remainingTime=f'{remainingTime[1]}:{str(round(float(remainingTime[2])))}'
            timer.config(text=f'Remaining time: {remainingTime}')
        elif not finish:
            timer.config(text='.............')
        elif gameover:
            timer.config(text='Game over')

        root.after(1000,updateTimer)
            

    timer=ttk.Label(root)
    container=ttk.Frame(root)

    timer.pack()
    container.pack(side="top", fill="both", expand=True)
    introduction(container)

    updateTimer()
    root.mainloop()
if __name__ == "__main__": 
    main()

# if datetime.now()>=finish:
#     print("#################### GAME OVER ####################")
#     backGame.game=False
# #clears the csv file at the end of the game
# with open('bidsFile.csv','w',newline='') as bidsFile:
#     bidsFile.close()