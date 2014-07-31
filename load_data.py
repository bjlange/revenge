"""
Creates a nice tidy pickle file of the data in the data/ directory.
"""

import os
import csv
from collections import defaultdict

class Position:
    """
    A position for fantasy football.
    """
    def __init__(self, title, players=[]):
        if title in [QB, RB, WR, TE, DEF, ST, K]:
            self.title = title
        else:
            raise Exception("Position name not valid: %s" % name)

        # a dictionary keyed on player name for quick lookups
        self.players = {}
        for player in players:
            self.players[player.name] = player



class Player:
    """A player/squad"""
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.stat_categories = []
        self.seasons = defaultdict(dict)

    # stats is a dictionary keyed on the name of the stat, with a
    # value that can be converted to a float
    def add_season(self, year, stats):
        if self.stat_categories == []:
            for key in stats.iterkeys():
                key = self.clean_stat_name(key)
                if key:
                    self.stat_categories.append(key)

        for key, val in stats.iteritems():
            key = self.clean_stat_name(key)
            if key and self.stat_categories and key not in self.stat_categories:
                raise Exception("Stat '%s' not in existing categories: %s" % \
                                (key ,str(self.stat_categories)))
            try:
                val = float(val)
            except:
                pass # if we can't float it, it's probably text or something


            self.seasons[year][key] = val

    def clean_stat_name(self, stat_name):
        """ for dealing with unruly headers """
        stat_name = stat_name.strip()
        mapping = {'Rec Tgt':'Targets',
                   'Tgt':'Targets',
                   'KR Lng': 'KR Long',
        }

        if self.position == 'QB':
            mapping['YdsL'] = 'Sack Yds'

        for key, val in mapping.iteritems():
            if stat_name == key:
                stat_name = val

        if stat_name:
            return stat_name
        else:
            return False

if __name__ == "__main__":

    data_root = "./data/"

    for subdir, dirs, files in os.walk(data_root):
        if not dirs:
            year = subdir.split('/')[-1]
            for filename in files:
                if filename.split('.')[-1].lower() == 'csv':
                    position = filename.split('.')[0].upper()
                    with open(os.path.join(subdir,filename),'rU+') as csvfile:
                        reader=csv.DictReader(csvfile)
                        for obj in reader:
                            try:
                                p = Player(obj["Name"], position)
                                p.add_season(year, obj)
                            except KeyError:
                                p = Player(obj["Team"], position)
                                p.add_season(year, obj)
                            a, b = p.position, p.stat_categories
                            b.sort()
                            print a, b
