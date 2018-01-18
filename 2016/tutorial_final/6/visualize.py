import matplotlib
import matplotlib.pyplot as plt
import seaborn # or alternatively plt.style.use('ggplot') for a similar look
import numpy as np
import math
from textwrap import fill
from espncricinfo.player import Player
import matplotlib

major_countries = set(["Australia", "Sri Lanka", "West Indies", "Zimbabwe", "New Zealand",
                       "India", "Pakistan", "Bangladesh", "South Africa", "England"])

#get which team a player belongs to
def get_team(player):
    for team in player.major_teams:
        for country in major_countries:
            if country in team:
                return country
    return player.major_teams[0]

#get average of batsmen for relevant format of game
def get_bat_average(player):
    avg = 0
    debut = True
    try: #account for API error
        for data in player.batting_fielding_averages:
            #get appropriate average if non-debutee
            if match_class in data.keys()[0]:
                debut = False
                for level, average in data.iteritems():
                    avg=float(average[5][1]) #average is in the 6th index
                    return avg
            #get estimate of other performances if debutee     
            if debut:
                count = 0
                for data in b.batting_fielding_averages:
                    for level, average in data.iteritems():
                        avg+=float(average[5][1]) #average is in the 6th index
                        count+=1
                avg/= count if count > 0 else 1
                return avg
    except:
        return 0
        
#get average of bowlers for relevant format of game
def get_bowl_average(player):
    avg = 0
    debut = True
    try: #account for API error
        for data in player.bowling_averages:
            #get appropriate average if non-debutee
            if match_class in data.keys()[0]:
                debut = False
                for level, average in data.iteritems():
                    avg=float(average[7][1]) #average is in the 8th index
                    return avg

            #get estimate of other performances if debutee     
            if debut:
                count = 0
                for data in player.bowling_averages:
                    for level, average in data.iteritems():
                        avg+=float(average[7][1]) #average is in the 8th index
                        count+=1
                avg/= count if count > 0 else 1
                return avg
    except:
        return 0

#get strike rate of bowlers for relevant format of game
def get_bowl_sr(player):
    sr = 0
    debut = True
    try: #account for API error
        for data in player.bowling_averages:
            #get appropriate average if non-debutee
            if match_class in data.keys()[0]:
                debut = False
                for level, average in data.iteritems():
                    sr=float(average[9][1]) #average is in the 8th index
                    return sr

            #get estimate of other performances if debutee     
            if debut:
                count = 0
                for data in player.bowling_averages:
                    for level, average in data.iteritems():
                        sr+=float(average[9][1]) #average is in the 8th index
                        count+=1
                sr/= count if count > 0 else 1
                return sr
    except:
        return 0

    
#displays top 5 players from both teams in bar chart
def display_top(bat, bowl, all_round, match_info):
    bat_avgs = []
    bowl_avgs = []
    all_avgs = []
    width = 0.25
    d = dict()
    
    #get batting info
    for b in bat:
        bat_avg = get_bat_average(b)
        d[bat_avg] = b
        bat_avgs.append(bat_avg)
    bat_avgs = [avg for avg in bat_avgs if avg!=None]
    
    #get top in match
    num = min(len(bat_avgs),5)
    top_bat_avg = sorted(bat_avgs)[-num:]
    top_bat = [d[avg].name + " (" + get_team(d[avg]) + ")" for avg in top_bat_avg]
    top_bat = [s.replace(" ", "\n") for s in top_bat]
    
    #visualize
    f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20,20))
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=1)
    ax1.bar(range(len(top_bat_avg)), top_bat_avg)
    pos = np.arange(len(top_bat))
    ax3.set_xlim(min(pos)-width, max(pos)+width*4)
    ax1.set_xticks([x + 1.5*width for x in pos])
    ax1.set_xticklabels(top_bat)
    ax1.set_ylabel("Average")
    ax1.set_xlabel("Batsmen (Higher averages are ranked higher)")
    ax1.set_title(fill("Top Batsmen in " + match_info + "\n", 30))
    
    #get bowling info
    for b in bowl:
        bowl_avg = get_bowl_average(b)
        d[bowl_avg] = b
        bowl_avgs.append(bowl_avg)
        
    bowl_avgs = [avg for avg in bowl_avgs if avg!=None]
    #get top in match
    num = min(len(bowl_avgs),5)
    top_bowl_avg = (sorted(bowl_avgs)[:num])
    top_bowl_avg.reverse()
    top_bowl = [d[avg].name + " (" + get_team(d[avg]) + ")" for avg in top_bowl_avg]
    top_bowl = [s.replace(" ", "\n") for s in top_bowl]
    
    #visualize
    ax2.bar(range(len(top_bowl_avg)), top_bowl_avg)
    pos = np.arange(len(top_bowl))
    ax3.set_xlim(min(pos)-width, max(pos)+width*4)
    ax2.set_xticks([x + 1.5*width for x in pos])
    ax2.set_xticklabels(top_bowl)
    ax2.set_ylabel("Average")
    ax2.set_xlabel("Bowlers (Lower averages are ranked higher)")
    ax2.set_title(fill("Top Bowlers in " + match_info + "\n",30))
    
    #get all_round info
    for a in all_round:
        all_avg = get_bat_average(a) - get_bowl_average(a)
        d[all_avg] = a
        all_avgs.append(all_avg)
            
    #get top in match
    num = min(len(all_avgs),5)
    top_all_avg = (sorted(all_avgs)[-num:])
    top_all = [d[avg].name + " (" + get_team(d[avg]) + ")" for avg in top_all_avg]
    top_all = [s.replace(" ", "\n") for s in top_all]
    
    #visualize
    ax3.bar(range(len(top_all_avg)), top_all_avg)
    pos = np.arange(len(top_all))
    ax3.set_xlim(min(pos)-4*width, max(pos)+width*8)
    ax3.set_xticks([x + 1.5*width for x in pos])
    ax3.set_xticklabels(top_all)
    ax3.set_ylabel("Average")
    ax3.set_xlabel("Allrounders (Higher averages are ranked higher)")
    ax3.set_title(fill("Top Allrounders in " + match_info + "\n",30))
