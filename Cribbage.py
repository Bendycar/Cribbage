# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 13:02:13 2024

@author: bendc
"""

import random
import itertools
import collections

faceCards = {11 : 'Jack', 12 : 'Queen', 13 : 'King', 1 : 'Ace'}
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']

def dealHand(handsize): 
    hand = []
    
    while len(hand) < handsize:
        card = []
        cardValue = random.randint(1,13)
        if cardValue in faceCards:
            card.append(faceCards[cardValue])
        else:
            card.append(cardValue)
        
        card.append(random.choice(suits))
        
        if card not in hand:
            hand.append(card)
        
    return hand

def findValues(hand, topCard): #Should only be used for finding 15s - pairs and runs need to preserve face card type
    values = []
    for i in hand:
        if i[0] == 'Ace':
            values.append(1)
        elif i[0] in faceCards.values():
            values.append(10)
        else:
            values.append(i[0])
    
    if topCard[0] == 'Ace':
        values.append(1)
    elif topCard[0] in faceCards.values():
        values.append(10)
    else:
        values.append(topCard[0])
    
    return values

def flippedCard(hand):
    topCard = []
    flippedValue = random.randint(1,13)
    if flippedValue in faceCards:
        topCard.append(faceCards[flippedValue])
    else:
        topCard.append(flippedValue)
    
    topCard.append(random.choice(suits))
    
    if topCard not in hand:
        return topCard
    else:
        return flippedCard(hand)

def pairs(hand, topCard): #Also finds 3 and 4 of a kind
    fullHand = hand + [topCard]
    cardCounts = {}
    points = 0
    for i in fullHand:
        if i[0] in cardCounts:
            cardCounts[i[0]] += 1
        else:
            cardCounts[i[0]] = 1
    
    for i in cardCounts:
        if cardCounts[i] == 2:
            points += 2
        elif cardCounts[i] == 3:
            points += 6
        elif cardCounts[i] == 4:
            points += 12
    
    return points
        
def flush(hand, topCard):
    suitCounts = {}
    points = 0
    for i in hand:
        if i[1] in suitCounts:
            suitCounts[i[1]] += 1
        else:
            suitCounts[i[1]] = 1
    
    for i in suitCounts:
        if suitCounts[i] == 4:
            points += 4
    
    if topCard[1] in suitCounts:
        suitCounts[topCard[1]] += 1
    else:
        suitCounts[topCard[1]] = 1
    
    for i in suitCounts:
        if suitCounts[i] == 5:
            points += 1
    return points

def rightJack(hand, topCard):
    points = 0
    for i in hand:   
        if i[0] == 'Jack':
            if i[1] == topCard[1]:
                points += 1
    
    return points

def fifteens(values):
    target = 15
    result = [seq for i in range(len(values))
          for seq in itertools.combinations(values, i)
          if sum(seq) == target]
    
    count = len(result)
    
    return (count * 2)

def runs(hand, topCard):
    multiplier = 1
    longestRun = []
    runLength = 0
    newHand = []
    faceReverse = {'Jack' : 11, 'Queen' : 12, 'King' : 13, 'Ace' : 1}
    for i in hand:
        if i[0] in faceReverse:
            newHand.append(faceReverse[i[0]])
        else:
            newHand.append(i[0])
    
    if topCard[0] in faceReverse:
        newHand.append(faceReverse[topCard[0]])
    else:
        newHand.append(topCard[0])
        
    newHand.sort()
    
    handSet = sorted(set(newHand))
    
    currentRun = [handSet[0]]
    for i in range(len(handSet) - 1):
        if handSet[i + 1] == handSet[i] + 1:
            currentRun.append(handSet[i+1])
        else:
            currentrunLength = len(currentRun)
            if currentrunLength > runLength:
                runLength = currentrunLength
                longestRun = currentRun
            currentRun = [handSet[i + 1]]

    currentrunLength = len(currentRun)
    if currentrunLength > runLength:
        runLength = currentrunLength
        longestRun = currentRun
                

            
    dupes = [card for card, count in collections.Counter(newHand).items() if count > 1]
    
    for i in dupes:
        if i in longestRun:
            multiplier *= 2
            
    if runLength >= 3:
        return (runLength * multiplier)
    else:
        return 0

def totalPoints(hand, topCard):
    return (fifteens(findValues(hand, topCard)) + pairs(hand, topCard) + flush(hand, topCard) + rightJack(hand, topCard) + runs(hand, topCard))
    

def optimalToss(hand, topCard):
    tosses = {}
    for i in range(len(hand)):
        handCopy = hand.copy()
        tossedCard = handCopy.pop(i)
        tosses[(tossedCard[0], tossedCard[1])] = totalPoints(handCopy, topCard)
        
    return tosses

def cribSim(trials, hand, topCard):
    points = {}
    for i in range(trials):
        hand = dealHand(5)
        topCard = flippedCard(hand)
        scores = optimalToss(hand, topCard)
        for j in scores:
            if j[0] in points:
                points[j[0]] += scores[j]
            else:
                points[j[0]] = scores[j]
    
    for i in points:
        points[i] = points[i] / trials
        
    return points
hand = dealHand(5)
topCard = flippedCard(hand)

print(hand)
print(topCard)
print(optimalToss(hand, topCard))
