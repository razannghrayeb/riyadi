from Main.models import Player
from django.core.management.base import BaseCommand
import os


"""
READDDDD THISSS!!!!!!!!
THIS IS A SCRIPT TO POPULATE PLAYERS DATABASE PLEASE DO NOT RUN THIS UNLESS THE DATABASE NEEDS POPULATION
"""
class Command (BaseCommand):

    help = 'Populates the Player model with data from the file.'

    def handle(self, *args, **kwargs):

        file_path = "C:\\Users\\96176\\Desktop\\C++\\populatePlayersDb.txt" #make sure to update this to your own path !!!!!!!!!!!!!!!!!

        if not os.path.isfile(file_path):
            return -1
        
        file = open(file_path,"r")


        for line in file:
            
            line = line.strip() 
            if not line:
                continue
            else:

                line = line.split(",")
                
                player = Player.objects.create(Name=line[0],image=line[1],TshirtNumber=line[2],role=line[3])
                self.stdout.write(self.style.SUCCESS("Player '{}' created.".format(player.Name))) 
                

    

