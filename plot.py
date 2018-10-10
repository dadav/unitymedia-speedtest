#!/usr/bin/env python                                                                                                                             
                                                                                                                                                  
import csv                                                                                                                                        
import argparse                                                                                                                                   
import datetime as dt                                                                                                                             
import matplotlib.pyplot as plt                                                                                                                   
import matplotlib.dates as mdates                                                                                                                 
plt.style.use('seaborn-deep')                                                                                                                     
                                                                                                                                                  
                                                                                                                                                  
def main():                                                                                                                                       
    parser = argparse.ArgumentParser()                                                                                                            
    parser.add_argument('-i', '--input', action='store',                                                                                          
                        dest='input', default='tests/tests.csv')                                                                                  
    parser.add_argument('-o', '--output', action='store',                                                                                         
                        dest='output', default='tests/diagram.png')                                                                               
    args = parser.parse_args()                                                                                                                    
                                                                                                                                                  
    dates = []                                                                                                                                    
    dlrates = []                                                                                                                                  
    uprates = []                                                                                                                                  
    ping = []                                                                                                                                     
                                                                                                                                                  
    with open(args.input) as csvfile:                                                                                                             
        reader = csv.reader(csvfile, delimiter=";", quotechar='"')                                                                                
        for row in reader:                                                                                                                        
            dates.append(row[1])                                                                                                                  
            dlrates.append(row[3])                                                                                                                
            uprates.append(row[4])                                                                                                                
            ping.append(row[5])                                                                                                                   
                                                                                                                                                  
    x = [dt.datetime.strptime(d, '%d.%m.%Y %H:%M Uhr').date() for d in dates]                                                                     
                                                                                                                                                  
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))                                                                         
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())                                                                                        
            
    ax1 = plt.subplot(311)                                                                                                                        
    ax1.set_title("Download")                                                                                                                     
    plt.plot(x, dlrates, "C1")                                                                                                                    
    plt.ylabel("Mbit/s")                                                                                                                          
    plt.setp(ax1.get_xticklabels(), visible=False)                                                                                                
                                                                                                                                                  
    ax2 = plt.subplot(312, sharex=ax1)                                                                                                            
    ax2.set_title("Upload")                                                                                                                       
    plt.plot(x, uprates, "C2")                                                                                                                    
    plt.ylabel("Mbit/s")                                                                                                                          
    plt.setp(ax2.get_xticklabels(), visible=False)                                                                                                
                                                                                                                                                  
    ax3 = plt.subplot(313, sharex=ax1)                                                                                                            
    ax3.set_title("Ping")                                                                                                                         
    plt.plot(x, ping, "C3")                                                                                                                       
    plt.ylabel("ms")                                                                                                                              
    plt.gcf().autofmt_xdate()                                                                                                                     
                                                                                                                                                  
    plt.savefig(args.output)                                                                                                                      
    plt.show()                                                                                                                                    
                                                                                                                                                  
                                                                                                                                                  
if __name__ == "__main__":                                                                                                                        
    SystemExit(main())
