# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 11:10:52 2017

@author: user
"""
import codecs
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
from collections import defaultdict
from operator import itemgetter
# read and clean the data from artists.dat
fp = codecs.open("artists.dat", encoding="utf-8")
aid2name={}    #Create dictionary to store data  from artist.dat
fp.readline()  #skip first line of headers
for line in fp:
    line = line.strip()
    fields = line.split('\t')
    aid = int(fields[0])
    name = fields[1]
    aid2name[aid]=name
fp.close()
artist=Series(aid2name)  # create Series from dict aid2name

#read and clean data from user_artist.dat
fp=codecs.open("user_artists.dat",encoding="utf-8")
aid2numplays=defaultdict(int)   #Using defaultdict to store data
uid2numplays={}     
uid_aid=defaultdict(int); # store how many listerners evey artist have  
uid_count=defaultdict(int)# store how many times every user play
fp.readline()
for line in fp:
    line=line.strip()
    fields=line.split("\t")
    userid=int(fields[0])
    aid=int(fields[1])
    numplay=int(fields[2])
    aid2numplays[aid]+=numplay  
    uid2numplays[userid]=numplay
    uid_aid[aid]+=1;     
    uid_count[userid]+=numplay
             
fp.close()             
sorted_aidnumplays=sorted(aid2numplays.items(),key=itemgetter(1),reverse=True)
            
#Question 1
print(" ")
for i in range(40):
    print("!",end="")
print("")
print("")
print("1: Who are the top artists in terms of play counts.")
print("Description: Create dict sorted_aidnumplays to sort aid2numplays.Use aid\
 to find artist name in Series artists")
sorted_aidnumplays_top10=sorted_aidnumplays[:10]
for (aid,counts) in sorted_aidnumplays_top10:
    print(artist[aid],end="")
    print("(",aid,")",sep="" ,end=" ")
    print(counts)
    

sorted_aid_uid=sorted(uid_aid.items(),key=itemgetter(1),reverse=True)
#Question2
#Read from user_artist.dat 
print(" ")
for i in range(40):
    print("!",end="")
print("")
print("")
print("2:What artists have the most listeners? .")
print("Description: Create dict sorted_aid_uid to sort uid_aid.Use aid\
 to find artist name in Series artists")
sorted_aid_uid_top10=sorted_aid_uid[:10]
for(aid,counts) in sorted_aid_uid_top10:
    print(artist[aid],end="")
    print("(",aid,")",sep="" ,end=" ")
    print(counts) 



#Question3

print(" ")
for i in range(40):
    print("!",end="")
print("")
print("")
print("3.Who are the top users?")
print("Description: Create dict sorted_uid_count to sort uid_count.Use aid\
 to find artist name in Series artists")
sorted_uid_count=sorted(uid_count.items(),key=itemgetter(1),reverse=True)
sorted_uid_count_top10=sorted_uid_count[:10]
for(uid,counts) in sorted_uid_count_top10:
    print(uid,counts,sep=" ")

artist_count_average=defaultdict(int)
for aid in aid2numplays:
    count_listener=uid_aid[aid]
    artist_count_average[aid]=aid2numplays[aid]/uid_aid[aid]

sorted_artist_count_average=sorted(artist_count_average.items(),key=itemgetter(1),reverse=True)


    

#Question4

print(" ")
for i in range(40):
    print("!",end="")
print("")
print("")
print("5 What artists with at least 50 listeners have the highest average number of plays per listener")
print("Description: Create dict sorted_artist_count_average to sort artist_count_average.Use aid\
 previous dict to find other required info")

sorted_average_top10=sorted_artist_count_average[:10]
for(aid,counts) in sorted_average_top10:
    for (i,name) in aid2name.items():
        if i==aid:
            print("Name=",name,end=" ")
    print("Aid=",aid,end=" ")
    for (i, count) in aid2numplays.items():
        if i==aid:
            print("Total play=",count,end=" ")
    for(i,uid) in uid_aid.items():
        if i==aid:
            print("Total listeners=",uid,end=" ")
    print("average counts=",counts)
    print()
    
    
    

#Question5

print(" ")
for i in range(40):
    print("!",end="")
print("")
print("")
print("5 What artists with at least 50 listeners have the highest average number of plays per listener")
print("Description: Create dict sorted_average_top10 to sort artist_count_average which have more than \
50 listner.Use aid in previous dict to find other required info")
print("")
average_top10=defaultdict(int)
count=0
for (count_listener, average) in artist_count_average.items():
    if count_listener>=50 and count<10:
        count+=1
        average_top10[count_listener]=average
sorted_average_top10=sorted(average_top10.items(),key=itemgetter(1),reverse=True)

for(aid,counts) in sorted_average_top10:
    for (i,name) in aid2name.items():
        if i==aid:
            print("Name=",name,end=" ")
    print("Aid=",aid,end=" ")
    for (i, count) in aid2numplays.items():
        if i==aid:
            print("Total play=",count,end=" ")
    for(i,uid) in uid_aid.items():
        if i==aid:
            print("Total listeners=",uid,end=" ")
    print("average counts=",counts)
    print()
    
    
 #Question6

print(" ")
for i in range(40):
    print("!",end="")
print("")
print("")
print("Do users with five or more friends listen to more songs?")
print("Description: Create dict uid_friendcount to store info about how many friends each\
user have. Loop through the dict to find which user have more than five friend.Sum up\
the total plays using uid_count dict ")
print("")

#read user_friend.dat
fp = codecs.open("user_friends.dat", encoding="utf-8")
uid_friendcount=defaultdict(int)   #Create dictionary to store data  from user_friend.dat
fp.readline()  #skip first line of headers
for line in fp:
    line = line.strip()
    fields = line.split('\t')
    userid = int(fields[0])
    fid = fields[1]
    uid_friendcount[userid]+=1  #store info about how many friends each user have.
fp.close()

count_morefriend=0
count_lessfriend=0
totalplay_lessfriend=0
totalplay_morefriend=0
for (userid,count) in uid_friendcount.items():
    if count>=5:
        count_morefriend+=1
        totalplay_morefriend+=uid_count[userid]
    else:
        count_lessfriend+=1
        totalplay_lessfriend+=uid_count[userid]
        
print("The average songs played by users who have more than five friends",
      totalplay_morefriend/count_morefriend)

print("The average songs played by users who have less than five friends",
      totalplay_lessfriend/count_lessfriend)