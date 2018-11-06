# MACHINE LEARNING OPGAVE WEEK 2

import numpy as np
from random import randint
from uitwerkingen import *

#Laden van de data en zetten van de variabelen.
data = np.load('opgave2_data.npz')
weights = np.load('weights.npz')
X,y = data['arr_0'], data['arr_1']
Theta1, Theta2 = weights['arr_0'], weights['arr_1']

#Zetten van belangrijke variabelen
m = X.shape[0] # aantal datapunten in de trainingsset


# ========================  OPGAVE 1 ======================== 
rnd = randint(0, X.shape[0])
print ("Tekenen van data op regel {}".format(rnd))
hyp = y[rnd]
if (hyp==10): hyp=0
print ("Dit zou een {} moeten zijn.".format(hyp))
plotNumber(X[rnd,:])

input ("Druk op een toets om verder te gaan..."); 


# ========================  OPGAVE 2 ======================== 
print ("Sigmoid-functie met een relatief groot negatief getal zou bijna 0 moeten zijn")
print ("Sigmoid van -10 = {}".format(sigmoid(-10)))

print ("Sigmoid-functie van 0 zou 0,5 moeten zijn.");
print ("Sigmoid van 0 = {}".format(sigmoid(0)))

print ("Sigmoid-functie met een relatief groot positief getal zou bijna 1 moeten zijn")
print ("Sigmoid van 10 = {}".format(sigmoid(10)))

print ("Simoid aangeroepen met 1×3 vector [-10, 0, 10]")
print (sigmoid(np.matrix( [-10, 0, 10] )))
print ("Simoid aangeroepen met 3×1 vector [-10, 0, 10]")
print (sigmoid(np.matrix( ([-10], [0], [10]) )))

input ("Druk op een toets om verder te gaan..."); 


# ========================  OPGAVE 3 ======================== 
print ("Aanroepen van de methode predictNumber");
pred = predictNumber(Theta1, Theta2, X)
acc = np.count_nonzero([pred - y == 0])
print ("De accuratessse van het netwerk is {} %".format(100 * acc/ m))
print ("Dit zou zo rond de 97,5% moeten liggen.)")

