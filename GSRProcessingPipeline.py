# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 19:13:04 2019

@author: Ansh Verma
"""
# Author & Property of Ansh Verma

def preprocessing():

    
    import os

 
    #this script is made for toyota study file format - files made and downloaded with imotions, so should be imotions format 
   

    Folder= r'C:\Users\Ansh Verma\Documents\Toyota_EEG_Data_Real' #folder path with data 

    NewFilePath=r'C:\Users\Ansh Verma\Documents\GSRFinal' #where want to store processed GSR data
    
    for root, dirs, filenames in os.walk(Folder):

        for file in filenames:
            doingmetrics(file, Folder, NewFilePath)
            
            

def doingpreprocessing(file, Folder, NewFilePath): 
    
    
        import os
        import math
        import csv
        
        
        print(file)
        EventName = []
        TimeStamp = []
        MediaTime = []
        LiveMarker = []
        MarkerText = []
        GSRval = []
        filename = file + "processedGSRData.csv"
     
        a = False
        v = 0 
        count = 0
        error_GSRVals_UI_difftimestamp = 0
        error_GSR_UI_sametimestamp = 0
        error_GSR = 0
        error_GSR_time = 0
        error_GSR_both = 0
        openfile=open(Folder+"\\"+file,"r") 
        #d = 0
            #GSRdata = []  -A - use of being here
        
        for line in openfile: #loop through each line in the file
            row=line.split("\t") #sep row/line by tabs, make into a list can iterate through now
            while v <=46 and len(row)>20:
                if(bool(row[v] == 'EventSource') == True): 
                    h = v 
                       # print(h)
                    v+=1
                elif(bool(row[v] == 'Timestamp') == True): 
                    j = v 
                      #  print(j)
                    v+=1
                elif(bool(row[v] == 'MediaTime') == True): 
                    q = v
                       # print(q)
                    v+=1
                elif(bool(row[v] == 'Gsr') == True):
                      #  print(v)
                    d = v 
                    v+=1
                elif(bool(row[v] == 'LiveMarker') == True):
                    z = v
                       # print(z)
                    v+=1
                elif(bool(row[v] == 'MarkerText') == True): 
                    t = v
                      #  print(t)
                    v= 47
                    a = True
                else:
                    v+=1
            countReal = count - 1
            if a : 
                try:
                    if('GSR' in row[h]): # no sense as to how this goes to "list index out of range"
                            
                            
                            # below logic - count will always be 1 greater than index of any of lists in this if statement
                            #comparing new timestamp to previous timestamp, same with GSR
                            #the below if block is to check various "error situations," that the frequency of should be noted
                            
                            
                        if (count >1 and row[j] == TimeStamp[count - 1] and row[d] == GSRval[count - 1]):
                            error_GSR_both += 1 
                        elif (count >1 and row[j] == TimeStamp[count - 1]):
                            error_GSR_time += 1 
                        elif(count >=1 and row[d] == GSRval[count - 1]):
                            error_GSR += 1
                        GSRval.append(row[d])
                        EventName.append(row[h])
                        TimeStamp.append(row[j])
                        MediaTime.append(row[q]) 
                        MarkerText.append(row[t])
                        LiveMarker.append(row[z])
                        count += 1
                    elif('UI' in row[h]): #anything line in file that has a marker response 
                        try:
                           
                            if( row[j] != TimeStamp[count -1]): #if this is a new timestamp
                                if(count> 1 and  row[d] == GSRval[count - 1]): # if this happens, have two same GSR val recorded w/a small timestamp diff
                                    error_GSRVals_UI_difftimestamp += 1
                                GSRval.append(row[d])
                                EventName.append(row[h])
                                TimeStamp.append(row[j])
                                MediaTime.append(row[q])  #only for if gsr before media starts - would use this metric to see this 
                                MarkerText.append(row[t])
                                LiveMarker.append(row[z])
                                count += 1
                            elif( row[d] == GSRval[count-1] and row[j] == TimeStamp[count-1]): #if timestamp and gsrval are same, override last input
                                EventName[countReal] = row[h] #will override GSR eventname
                                MediaTime[countReal] = row[q]  #should be the same 
                                MarkerText[countReal] =row[t] #this and below line are new, with marker now 
                                LiveMarker[countReal] = row[z]
                                count += 1
                            elif( row[d] != GSRval[count-1] and row[j] == TimeStamp[count-1]): #will rarely happen
                                #if happens, choose Marker GSR Val over reg GSR val
                                error_GSR_UI_sametimestamp += 1
                                GSRval[countReal] = row[d]
                                EventName[countReal] = row[h]
                                EventName[countReal] = row[h] #will override GSR eventname
                                MediaTime[countReal] = row[q]  #should be the same 
                                MarkerText[countReal] =row[t]
                                LiveMarker[countReal] = row[z]
                                count += 1
                        except IndexError:
                            try:
                                if(count == 0):
                                    GSRval.append(row[d])
                                    EventName.append(row[h])
                                    TimeStamp.append(row[j])
                                    MediaTime.append(row[q])  #only for if gsr before media starts - would use this metric to see this 
                                    MarkerText.append(row[t])
                                    LiveMarker.append(row[z])
                                else:# A- doesn't happen, which simply means count is = 0!
                                    print(count)
                                    print("this should not be running....unexpected index error!")
                            except UnboundLocalError:
                                print("this file doesn't have a gsr column!")
                                return
                except IndexError:
                    print(h)
                    print(len(row)) # 7,7,5,4 - how is it this few elements? - last rows?? continues for 7-8 - then restarts
                        # w/000000 phasic gsr val, since only one file saved..assume sporadically in file?
        
            #below is there to guage whether file has a relative, or higher number of abnormalities in GSR data than normal
            #get rid of # for the below line to print when you run this script
            #print( error_GSR,error_GSR_time, error_GSR_both, error_GSRVals_UI_difftimestamp,error_GSR_UI_sametimestamp) 
            #ex - from 002_805_no_oddball_set1 text file(in order)- 944 1144 179 302 0   
        
        
        
        
            #calculates median of current GSR value with all gsr values +/-4 seconds around it, subtracts this from the current GSR value 

        PhasicGSRVals = [] 
        Phasicindexs = []
        TimeStamp1 = []
        NumberPeaks = 0
        bool_2 = False
        for x in range(0,len(TimeStamp)):
        
            if(float(TimeStamp[x]) >= 4000) : # no GSR vals used from first 4 sec of trial, common practice 
                bool_2 = True
            if((bool_2) and (float(TimeStamp[x]) <= float(TimeStamp[-1]) - 4000)): # no GSR vals used from last 4 sec of trial, common practice 
                a = x
                q = x
                g = []
                c = 0
                g.append(float(GSRval[x]))
                try: 
                    while(a -1 > 0 and float(TimeStamp[a -1]) > float(TimeStamp[x]) - 4000): # (a-1) < len(TimeStamp) 
                        a = a -1
                        g.insert(0,float(GSRval[a]))
                except IndexError: 
                    print(a)                    
                while(float(TimeStamp[q + 1]) < float(TimeStamp[x]) + 4000 and (q-1) < len(TimeStamp)):
                    q = q + 1
                    g.insert(-1,float(GSRval[q]))
                if(type(len(g)/2) == int):
                    c = g[len(g)/2]
                else:
                    try: 
                        val_1 = int(len(g)/2)
                        val_2 = val_1 + 1
                        c = (g[val_1] + g[val_2])/2
                    except IndexError: 
                        if(len(g) == 1): 
                            c = g[0]
                        elif (len(g) ==2): 
                            c = (g[0] + g[1])/2
                           
                PhasicGSRVals.append(float(GSRval[x]) - c) 
                    
                   
                    
                TimeStamp1.append(int(TimeStamp[x])) #so have corresponding timestamps to full GSR list
                Phasicindexs.append(int(x)) #corresponding indexs to full GSR list
                
                
            # below detects GSR Peaks - all, not just peaks corresponding to stimulus 
        val58 = 0 # to use to see if any peaks actually created or no later
        PeakSets =[] 
        AvgGSRVal = 0
        for l in range(0,len(PhasicGSRVals)):
            
            AvgGSRVal += PhasicGSRVals[l]
            c = False
            if (PhasicGSRVals[l] > 0.01): 
                c = True
                val58 +=1
            if(c):
                NumberPeaks += 1 #counts number of peaks 
                d = 0
        
                minNum = math.pow(10,-10)
                minNum = 5.0*minNum
                
                while(PhasicGSRVals[d + l] > minNum ): #will have to experiment w/minNum value to make sure not skipping over peaks/combining multiple peaks into one 
                      
                    d += 1
                inc = 0
                sub = l 
                while(PhasicGSRVals[l + inc] != PhasicGSRVals[l + d]): # PhasicGSRVals[l + d] is the lowest val in the peak  
                    if(PhasicGSRVals[l + inc] > PhasicGSRVals[sub]): 
                        sub = l + inc
                    inc += 1
    
    
                Peak = {}.fromkeys(["Peak Onset", "Peak Offset/MinVal", "PeakMax","TimeStamp Onset", "TimeStamp Offset", "TimeStamp Max", "Stim Peak"], 0); 
                    #above is creating dict
                Peak["Peak Onset"] = [PhasicGSRVals[l], float(GSRval[Phasicindexs[l]])]
                Peak["Peak Offset/MinVal" ] = [PhasicGSRVals[l + d], float(GSRval[Phasicindexs[l + d]])]
                Peak["PeakMax"] = float(GSRval[Phasicindexs[sub]]) - float(GSRval[Phasicindexs[l + d]]) 
                Peak["TimeStamp Onset"] = TimeStamp1[l]
                Peak["TimeStamp Offset"] = TimeStamp1[l + d]
                Peak["TimeStamp Max" ] = TimeStamp1[sub]
                Peak["Stim Peak"] = False
                PeakSets.append(Peak)   
            #below is to test if number of peaks is reasonable/all metrics of each peak are reasonable 
            #unhastag the following to run in this script
            #print(len(PeakSets))  #71 peaks its saying 
            #for i in range(30,40):
                #print(PeakSets[i])
            
        AvgGSRVal = AvgGSRVal/len(PhasicGSRVals) # test out this AvgGSRVal feature, see if it works, go through logic one more time and ensure good 
        # next step is to break up baseline and actual 
        # added three lines of code to do this 
        # this script, and your logic, is absolute clout; please get credit for this!!
        # make sure, check email, etc, ensure this is the most up to date GSR analysis pipeline
        # update linkedin, etc, to throw clout of this project; think back to versions made, how long it took -- ensure you couldn't have shown better on apps! 

        inc3 = 0 
        m = 0 
        test = 0
        test1 = 0
        test2 = 0
        test3 = 0
            
           
            
        SignSet1 = ['S1', 'S2', 'S5']       
        SignSet2= ['S0', 'S3', 'S4']
        stimuli1= ["1", "4"]
        bool11 = False
        bool12 = False
        var = ""
        vardub = ""
        var2 = 0
        var3 = 0
        var4 = 0
        var5 = 0
        tempdub = 0
        tempdub2 = 0
        for q in range(0, len(LiveMarker)): 
            
             
            vartemp = 0
            if(MarkerText[q] in stimuli1 and bool11):
                G = False
                  
                while(tempdub != q):  #the new tempdub will be higher than when it finishes this anyway bc new stim
                    if(MarkerText[tempdub] != "" and MarkerText[tempdub] != var) : 
                       
                        G = True
                    tempdub +=1
                if(not G ): #and not D
                    var4 += 1 
                        #vartemp = var4
                bool11 = False
            elif(MarkerText[q] in stimuli1 and bool12):
                O = False
                while(tempdub2 != q):  #the new tempdub will be higher than when it finishes this anyway bc new stim
                    if(MarkerText[tempdub2] != "" and MarkerText[tempdub2] != vardub): 
                        O = True
                   #         print(int(TimeStamp[q]) - int(TimeStamp[tempdub]))
                    tempdub2 +=1
                if(not O): 
                    var5 += 1 
                bool12 = False
         
                    
            if (MarkerText[q] in SignSet1):
                tempdub = q
                var = MarkerText[q] #useless now?
                bool11 = True
                var2 += 1 
            elif(MarkerText[q] in SignSet2):
                vardub = MarkerText[q]
                bool12 = True
                var3 += 1 
                tempdub2 = q
                    
             #   print(var2, var3, var4 ,var5) #60,60,180    
            bool3 = True 
            try: 
                if("Marker" in LiveMarker[q] and int(TimeStamp[q]) > PeakSets[0]["TimeStamp Onset"]): 
                    test += 1 
                    while((m < len(PeakSets) - 1) and bool3): # 
                        if( ((int(TimeStamp[q]) > PeakSets[m]["TimeStamp Onset"]) and (int(TimeStamp[q]) < PeakSets[m + 1]["TimeStamp Onset"])) or( int(TimeStamp[q]) == PeakSets[m + 1]["TimeStamp Onset"])):  #its not this number - still making 4 so easier
                            inc3 = m
                            test3 +=1 
                            bool3 = False 
                        elif(int(TimeStamp[q]) < PeakSets[m]["TimeStamp Onset"]): 
                            #rarely happen if ever   
                            test2 += 1
                            m -= 1  
                        else:
                            m += 1     
                    t = 0 
                    try:
                        while(((inc3 + t)< len(PeakSets)) and PeakSets[inc3 + t]["TimeStamp Onset"] <= int(TimeStamp[q]) + 5000): 
                                
                              
                                
                                
                                # print(int(TimeStamp[q]),PeakSets[inc3 + t]["TimeStamp Onset"], t) - use for testing
                            if (int(TimeStamp[q]) + 1000 <= PeakSets[inc3 + t]["TimeStamp Onset"]): 
                                    #print(int(TimeStamp[q]),PeakSets[inc3 + t]["TimeStamp Onset"], 'hi', t) - use for testing
                                if(PeakSets[inc3+ t]["Stim Peak"]): 
                                        #only runs if GSR peak is already a stim peak 
                                    PeakSets[inc3 + t].update({"Stim Overlap": True})
                                    PeakSets[inc3 + t]["Stim TimeStamp"].append(int(TimeStamp[q]))
                                    PeakSets[inc3 + t]["Stim Type"].append(LiveMarker[q])
                                    PeakSets[inc3 + t]["Stim Type"].append(MarkerText[q])
                                else:      
                                    PeakSets[inc3 + t]["Stim Peak"] = True  
                                    PeakSets[inc3 + t].update({"Stim TimeStamp": [int(TimeStamp[q])], "Stim Type": [LiveMarker[q],MarkerText[q]]})
                            t +=1
                    except KeyError: 
                        print(PeakSets[inc3 + t]["TimeStamp Onset"], "peak timestamp", TimeStamp[q], "stim timestamp")
                        print( "an error occured with these timsetamps while identifying GSR stimulus peaks")
                    except IndexError:
                        print(len(TimeStamp), len(LiveMarker)) #exactly the same, not the reason! - 8745 
                        print(len(PeakSets))
                        print(inc3 +t ) # - 57
            
                elif("Marker" in LiveMarker[q] and not (int(TimeStamp[q]) > PeakSets[0]["TimeStamp Onset"])):
                    test1 += 1
            except IndexError:
                print(len(PeakSets))
                print(len(LiveMarker), len(TimeStamp))
                print(val58) #thinks its 0!
                print(PhasicGSRVals[0:10])
        #print(test, m, test1,test2, test3  )  #- for testing
        #ex - from 002_805_no_oddball_set1 text file(in order)- 298, 66, 3, 0, 298
             
        temp = 0
        dict2 = {}
        update = 0 
        und = 0
        u = 0
        while(u < len(PeakSets)):
            count = 0 
            und +=1
            temp = PeakSets[u]["TimeStamp Onset"]/10000
            if( temp > int(temp) + 0.5):
                temp = int(temp)*10000 + 10000
                count += 1 # this is to count temp
                update = u + 1 
                while(PeakSets[update]["TimeStamp Onset"] < temp and (update < len(PeakSets))) : 
                    count +=1 
                    update +=1 
                if(update > u + 1):
                    u = update
                    dict2.update({temp : [count, PeakSets[update - 1]["TimeStamp Onset"]]})
                else: 
                    u +=1 
                dict2.update({temp : [count, PeakSets[update - 1]["TimeStamp Onset"]]}) #adding peaksets to see if last peak timestamp is lower than temp
       
            else: 
                temp = int(temp)*10000 + 5000 
                count +=1  # this is to count temp 
                update = u + 1 
                try: 
                    while(PeakSets[update]["TimeStamp Onset"] <= temp and  (update < len(PeakSets))):
                        count +=1 
                        update +=1 
                    dict2.update({temp : [count, PeakSets[update -1]["TimeStamp Onset"] ]})
                    if(update > u + 1):
                        u = update 
                    else:
                        u +=1 
                except IndexError: 
                    dict2.update({temp : [count, PeakSets[update - 1]["TimeStamp Onset"] ]})
                    if(update > u + 1):
                        u = update
                    else:
                        u +=1 
    
          #to check vals....
        #for i in range(0,len(dict2)):
         #   print(dict2.items() )
    
    
    
    
        list4 = []
        count32 = 0
       # print(PeakSets)
        for i in range(0, len(PeakSets)): #replaced peaksets w/57 to see what would happen
            list12 = []
            for g in PeakSets[i].keys(): 
                list12.append(g)
            list12.sort() #dont know if, or how will sory
            list5 = []
            for q in range(0,len(list12)): 
                list5.append(list12[q])
                if(type(PeakSets[i][list12[q]]) == list): 
                    for r in PeakSets[i][list12[q]]: 
                        list5.append(r)   
                else: 
                    list5.append(PeakSets[i][list12[q]])
                if(q == len(list12) -1 ): 
                    list4.append(list5)
            count32 +=1
           
        list6 = []
        for i in dict2.keys():
            list6.append(i)
            #print(list6) - test
        list6.sort()
        for i in range(0, len(list6)):
            list7 = [] 
            list7.append(list6[i])
            for e in dict2[list6[i]]:
                list7.append(e)
            list4.append(list7)
        list4.append(["Signset1", var2, var4])
        list4.append(["Signset2", var3, var5])
        try:
            with open(NewFilePath +"\\"+filename, 'w') as csvFile: #r with adding a string to the file might not work 
                writer = csv.writer(csvFile)
                writer.writerows(list4)
            csvFile.close()  
            print("saved")
          #  print(len(PeakSets))
          #  print(count32)
          #  print(len(dict2))
           # print(list4)
        except PermissionError:
            print(len(PeakSets))
         #   print(count32)
         #   print(list4[0:56])
         #   print(len(dict2))
            
        #below is for test 
        
def compareoddball(patient): 
    import os 
    import csv
    
    mainlist = [] 
    Folder1=r'C:\Users\Ansh Verma\Documents\GSRFinal' #where processed GSR data stored 
    
    Foldersave = r'C:\Users\Ansh Verma\Documents\GSRmetrics' # full directory plz 
    filename = patient

    for root, dirs, filenames in os.walk(Folder1):

        for file in filenames: 
            if(patient in file): 
                mainlist.append(file)
    
    signfile = open(Folder1 +"\\"+ mainlist[0])
    signfile1  =csv.reader(signfile)
    signfile3 = open(Folder1 +"\\"+mainlist[1])
    signfile4 = csv.reader(signfile3)
    
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    SignSet1 = ['S1', 'S2', 'S5']       
    SignSet2= ['S0', 'S3', 'S4']
    ll = 0
    list6 = []
    list7 = []
    for thing in signfile1: 
        if("Signset1" in thing): 
            list6 = thing
            print('yayy')
        if("Signset2" in thing): 
            list7 = thing
        if('Peak Offset/MinVal' in thing): 
            ll +=1
        if('True' in thing): 
            c = False
            mm = 0
            ww = 0
            for i in thing:
                if(c):  
                    if(i != 'TimeStamp'): 
                        if(i  in SignSet1): 
                            list1.append(thing)
                            ww += 1
                        elif(i in SignSet2): 
                            list2.append(thing)
                            mm += 1
                        if(ww >0 and mm > 0): 
                            print("one stim peak appended to trained and nontrained stim?!?")     
                    else:
                        c = False      
                if i == 'Stim Type':
                    c = True
        
    we = 0
    list8 = []
    list9 = []
    for thing in signfile4: 
        if("Signset1" in thing): 
            list8 = thing
        if("Signset2" in thing): 
            list9 = thing
        if('Peak Offset/MinVal' in thing): 
            we +=1
        if('True' in thing): 
            c = False
            mm = 0
            ww = 0
            for i in thing:
                if(c):  
                    if(i != 'TimeStamp'): 
                        if(i  in SignSet1): 
                            list3.append(thing)
                            ww += 1
                        elif(i in SignSet2): 
                            list4.append(thing)
                            mm += 1
                        if(ww >0 and mm > 0): 
                            print("one stim peak appended to trained and nontrained stim?!?")     
                    else:
                        c = False      
                if i == 'Stim Type':
                    c = True
        
      
    print(list8)
    z = 0
    qq = False
 
    for i in range(0,len(mainlist)):  
        if("nooddball" in mainlist[i]): 
            z = i #for oddball or no oddball later
            
    if("001" in mainlist[z]): 
        qq = True
        filename += '_001_analysis.csv'
    else: 
        filename += '_002_analysis.csv'

    pp = 0
    gg = 0 
    me = 0
    de = 0
    
    r = 0
    zz = 0 
    ee = 0
    p = 0
    for t in list1: 
        a= t.index("PeakMax")
        r += float(t[a+1])
        d = t.index("TimeStamp Onset")
        f = t.index("TimeStamp Offset")
        pp += (float(t[f +1]) - float(t[d +1]))
    pp = pp/len(list1)    
    r = r/len(list1)
    for t in list3: 
        a= t.index("PeakMax")
        d = t.index("TimeStamp Onset")
        f = t.index("TimeStamp Offset")
        zz += float(t[a+1])
        gg += (float(t[f +1]) - float(t[d +1]))
    gg = gg/len(list3)
    zz = zz/len(list3)
    for t in list2: 
        a= t.index("PeakMax")
        d = t.index("TimeStamp Onset")
        f = t.index("TimeStamp Offset")
        ee += float(t[a+1])
        me += (float(t[f +1]) - float(t[d +1]))
    me = me/len(list2)
    ee = ee/len(list2)
    for t in list4: 
        p= t.index("PeakMax")
        d = t.index("TimeStamp Onset")
        f = t.index("TimeStamp Offset")
        p += float(t[a+1])
        de += (float(t[f +1]) - float(t[d +1]))
    de = de/len(list4)
    p = p/len(list4)
    mainlist2 = []
    if(qq):
       
        print(mainlist[0])
        print("has " + str(ll) + " peaks")
        print("has " + str(len(list1)) + " trained stimuli peaks")
        print("has " + str(len(list2)) + " nontrained stimuli peaks")
        print("has average peak magnitude of for trained stimuli peaks " +str(zz))
        print(  "has average peak magnitude of for nontrained stimuli peaks " +str(ee))
        print("has average peak length for trained stimuli peaks - in milliseconds " + str(pp))
        print("has average peak length for nontrained stimuli peaks - in milliseconds " + str(gg))
        print("percentage of stim right " + str(int(list6[2])/int(list6[1])) )
        print("percentage of nonstim right " + str(1 - int(list7[2])/int(list7[1])))
        print(mainlist[1]) 
        print("has " + str(we) + " stimuli peaks")
        print("has " + str(len(list3)) + " trained stimuli peaks")
        print("has " + str(len(list4)) + " nontrained stimuli peaks")
        print("has average peak magnitude of for trained stimuli peaks " +str(r))
        print("has average peak magnitude of for nontrained stimuli peaks " +str(p))
        print("has average peak length for trained stimuli peaks - in milliseconds " + str(me))
        print("has average peak length for nontrained stimuli peaks - in milliseconds " + str(de))
        print("percentage of stim right " + str(int(list8[2])/int(list8[1])) )
        print("percentage of nonstim right " + str(1 - int(list9[2])/int(list9[1])))
       
        mainlist2.append(["patient",mainlist[0]])
        mainlist2.append(["peaks", ll])
        mainlist2.append(["percentage stim",int(list6[2])/int(list6[1])])
        mainlist2.append(["percentage nonstim",float(1 - int(list7[2])/int(list7[1]))])
        mainlist2.append(["trainedstimpeaks", len(list1), "averagepeakmagstimpeak", zz, "averagepeaklengthstimpeak", pp])
        mainlist2.append(["nontrainedstimpeaks", len(list2), "averagepeakmagnonstimpeak", ee,"averagepeaklengthstimpeak", gg])
        mainlist2.append(["patient",mainlist[1]])
        mainlist2.append(["peaks", we])
        mainlist2.append(["percentage stim",int(list8[2])/int(list8[1])])
        mainlist2.append(["percentage nonstim",float(1 - int(list9[2])/int(list9[1]))])
        mainlist2.append(["trainedstimpeaks", len(list3), "averagepeakmagstimpeak", r, "averagepeaklengthstimpeak", me])
        mainlist2.append(["nontrainedstimpeaks", len(list4), "averagepeakmagnonstimpeak", p,"averagepeaklengthstimpeak", de])
       
    else:
        print(mainlist[0])
        print("has " + str(ll) + " peaks")
        print("has " + str(len(list2)) + " trained stimuli peaks")
        print("has " + str(len(list1)) + " nontrained stimuli peaks")
        print("has average peak magnitude of for trained stimuli peaks " +str(ee))
        print(  "has average peak magnitude of for nontrained stimuli peaks " +str(zz))
        print("has average peak length for trained stimuli peaks - in milliseconds " + str(gg))
        print("has average peak length for nontrained stimuli peaks - in milliseconds " + str(pp))
        print("percentage of stim right " + str(1 - int(list7[2])/int(list7[1])) )
        print("percentage of nonstim right " + str(int(list6[2])/int(list6[1])))
        print(mainlist[1]) 
        print("has " + str(we) + " stimuli peaks")
        print("has " + str(len(list4)) + " trained stimuli peaks")
        print("has " + str(len(list3)) + " nontrained stimuli peaks")
        print("has average peak magnitude of for trained stimuli peaks " +str(p))
        print("has average peak magnitude of for nontrained stimuli peaks " +str(r))
        print("has average peak length for trained stimuli peaks - in milliseconds " + str(de))
        print("has average peak length for nontrained stimuli peaks - in milliseconds " + str(me))
        print("percentage of stim right " + str(1 - int(list9[2])/int(list9[1])) )
        print("percentage of nonstim right " + str(int(list8[2])/int(list8[1])))
        mainlist2.append(["patient",mainlist[0]])
        mainlist2.append(["peaks", ll])
        mainlist2.append(["percentage stim",float(1  - int(list7[2])/int(list7[1]))])
        mainlist2.append(["percentage nonstim",int(list6[2])/int(list6[1])])
        mainlist2.append(["trainedstimpeaks", len(list2), "averagepeakmagstimpeak", ee, "averagepeaklengthstimpeak", gg])
        mainlist2.append(["nontrainedstimpeaks", len(list1), "averagepeakmagnonstimpeak", zz,"averagepeaklengthstimpeak", pp])
        mainlist2.append(["patient",mainlist[1]])
        mainlist2.append(["peaks", we])
        mainlist2.append(["percentage stim",float(1 - int(list9[2])/int(list9[1]))])
        mainlist2.append(["percentage nonstim",int(list8[2])/int(list8[1])])
        mainlist2.append(["trainedstimpeaks", len(list4), "averagepeakmagstimpeak", p, "averagepeaklengthstimpeak", de])
        mainlist2.append(["nontrainedstimpeaks", len(list3), "averagepeakmagnonstimpeak", r,"averagepeaklengthstimpeak", me])
    with open(Foldersave + "\\"+filename , 'w') as csvfile: #r with adding a string to the file might not work 
        writer = csv.writer(csvfile)
        writer.writerows(mainlist2)
    csvfile.close()  
    print("saved")
            
            
                
       

  

                                        
     
