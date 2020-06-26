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
maxBid=1000
funds=1000
total=0
winning=2
DURATION=3 #minutes
INTROMESSAGE='''
Dear friend, welcome to my game prototype for
---------------------$tonks-----------------------
$ Stonks is a player vs player live bidding game
$ This prototype will emulate gameplay
$ The final game will be played with real money
$ I hope you find the game challenging and fun
$ You will need to think strategically and use
  the stats to win any significant amount of "money"
$ Proto is full of bugs, I'm only interested in
  gameplay feedback

I have shared an anonymous feedback survey with you
You honest feedback will immensely help the future
of this project

Thank you for giving Stonks a try,
                                            -Chy
'''
RULES='''
HERE ARE THE RULES OF THE GAME:
$ The person with the lowest unique bid wins ALL
  the cash from other players (bots in this game)
$ E.g. if you bid $1 but a bot matches your bid
  your bid is the lowest but not unique.
  If you bid a unique $741, you probably won't
  win because a bot will bid a lower unique bid
$ All bids are final and subtracted from your funds
$ EACH BID will reveal stats of the game, use them
  strategically to improve your winning chances
$ Make sure to continue bidding to update the table
  Bots may have matched you, the ony way to find if
  you are indeed still winning is to continue playing
  FOR THAT, MANAGE YOUR FUNDS to last the whole game
$ Good luck!
'''

#resets all the game variables for a new game
def resetGame():
    global uniqueDict
    global gameover
    global start
    global finish
    global playerBidsList
    global total
    global winning
    uniqueDict={x:[] for x in range(1, maxBid+1)}
    gameover=False
    start=datetime.now()
    finish=start+timedelta(minutes=DURATION)
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
    global winning
    uniqueDict[bid].append(p)
    winning=2
    if len(uniqueDict[bid])==1:
        if p=='player01':
            winning=True
    elif len(uniqueDict[bid])>1:
        print('not unique')
        if uniqueDict[bid][0]=='player01':
            winning=False

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
        elif uniqueness>1:
            playerBidsList['Unique rank'][i]='X'
        for j in range(bid):
            unik=len(uniqueDict[j+1])
            if unik==1:
                countLow+=1
            elif unik==0:
                countUnused+=1
        playerBidsList['# of unique bids lower'][i]=countLow
        playerBidsList['# of lower numbers unused'][i]=countUnused
        for k in range(int(bid),maxBid):
            if len(uniqueDict[k])==1:
                countHigh+=1
        playerBidsList['# of unique bids higher'][i]=countHigh
       
#registers and processes human bid, launches bot bids
def processBid(bid):
    global playerBidsList
    global uniqueDict
    global funds
    funds-=bid
    registerBid('player01', bid)
    isLowestUnique('player01', bid)
    addBid2Dict(bid)
    updateDict()

#sums total amount winnable in the game right now
def gameTotal():
    global total
    bidsList=open('bidsFile.csv','r')
    winTotal=0
    for row in bidsList:
        col=row.split(',')
        cellValue=int(col[1])
        winTotal+=cellValue
    total=winTotal
    bidsList.close()

def processBotBit():
    botPlay=botCompetition()
    registerBid('bot',botPlay)
    isLowestUnique('bot',botPlay)
    print(botPlay)

#a bot that places a set of bids to compete with player
def botCompetition():
    dec=69
    maxList=range(1,100)
    decision=rand.randint(1,20)
    if decision>18:
        botBid=rand.choice(playerBidsList["Bid"])
    elif decision==1:
        for i in range(1,maxBid):
            if len(uniqueDict[i])==1:
                dec=i
                break
        botBid=dec
    else:
        botBid=rand.choice(maxList)
    return botBid

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
    intro=ttk.Label(container, text=INTROMESSAGE)
    startButton=tk.Button(container, text="Start Game", command=lambda: startGame(True,container))
    rules=ttk.Label(container, text=RULES)
    intro.pack()
    startButton.pack()
    rules.pack()

def bidding(container):
    bidding.bidValue=1
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
            b.append(str(playerBidsList["Bid"][i]))
            u.append(str(playerBidsList["Unique rank"][i]))
            l.append(str(playerBidsList["# of unique bids lower"][i]))
            h.append(str(playerBidsList["# of unique bids higher"][i]))
            x.append(str(playerBidsList["# of lower numbers unused"][i]))
        b='\t|'.join([str(v) for v in b])
        u='\t|'.join([str(v) for v in u])
        l='\t|'.join([str(v) for v in l])
        h='\t|'.join([str(v) for v in h])
        x='\t|'.join([str(v) for v in x])
        table=f'''
        Your bids----------------|{b}
        Unique rank-------------|{u}
        # of uniques lower------|{l}
        # of uniques higher-----|{h}
        # of lower bids unused--|{x}
        '''
        return table

    def updateLabels():
        gameTotal()
        avaiLabel.config(text=f'Available funds: ${funds}')
        winLabel.config(text=f'Amount winnable: ${total}')
        table=tableFormat()
        bids.config(text=table)

    #TODO major issues here: check isLowestUnique
    def popUpResult(winning, bid):
        # if winning:
        #     messagebox.showinfo('Information', f'Your bid is currently winning: ${total}')
        # elif not winning:
        #     messagebox.showinfo('Information', f'Your bid of ${bid} did not win')
        return 0

    avaiLabel=ttk.Label(container,text=f'Available funds: ${funds}')
    winLabel=ttk.Label(container, text=f'Amount winnable: ${total}')
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
    rules=ttk.Label(container, text=RULES)
    goal=ttk.Label(container, text="GOAL: Try to reach $3000")

    avaiLabel.pack()
    winLabel.pack()
    bidLabel.pack()
    scale.pack()
    upButton.pack()
    downButton.pack()
    submit.pack()
    frame.pack()
    bids.pack()
    goal.pack()
    rules.pack()

    
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
        global funds
        if finish:
            remainingTime=finish-datetime.now()
            remainingTime=str(remainingTime).split(':')
            remainingTime=f'{remainingTime[1]}:{str(round(float(remainingTime[2])))}'
            timer.config(text=f'Remaining time: {remainingTime}')
            if finish<datetime.now():
                gameover=True
                timer.config(text='Game over')
                winIndex=1
                for i in range(1,maxBid):
                    if len(uniqueDict[i])==1:
                        winIndex=i
                        break 
                if uniqueDict[winIndex][0]=="player01":
                    answer=messagebox.askyesno('Congratulations!!', f'You won the ${total} and the game with bid: ${winIndex}\nCONGRATS\nWanna play again?')
                    funds+=total
                else:
                    answer=messagebox.askyesno('Sorry', f'The computer won with the lowest unique bid: ${winIndex}\nWanna play again?')
                if answer==True:
                    finish=False
                    gameover=False
                    root.destroy()
                    main()
                elif answer==False:
                    root.destroy()
                
        elif not finish:
            timer.config(text='.............')
        
        root.after(1000,updateTimer)  
        root.after(2000,processBotBit)

    timer=ttk.Label(root)
    container=ttk.Frame(root)

    timer.pack()
    container.pack(side="top", fill="both", expand=True)
    introduction(container)

    updateTimer()

    root.mainloop()
if __name__ == "__main__": 
    main()