"""
Creates a nice tidy pickle file of the data in the data/ directory.
"""

import os
import inspect
import csv
import pickle
from collections import defaultdict
import pprint
pp = pprint.PrettyPrinter()

class Player:
    """A player/squad that fills a position"""
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
            # if key and self.stat_categories and key not in self.stat_categories:
            #     raise Exception("Stat '%s' not in existing categories: %s" % \
            #                     (key ,str(self.stat_categories)))
            try:
                val = float(val)
            except:
                pass  # if we can't float it, it's probably text or something


            self.seasons[int(year)][key] = val

    def clean_stat_name(self, stat_name):
        """ for dealing with unruly headers """
        stat_name = stat_name.strip()
        mapping = {'Rec Tgt':'Targets',
                   'Tgt':'Targets',
                   'KR Lng': 'KR Long'}

        if self.position == 'QB':
            mapping['YdsL'] = 'Sack Yds'

        for key, val in mapping.iteritems():
            if stat_name == key:
                stat_name = val

        if stat_name:
            return stat_name
        else:
            return False

    def get_season(self, year):
        season = self.seasons[year]
        return season

    def get_points(self, year):
        season = self.seasons[year]
        score = 0.0
        if self.position == "QB":
            if 'Pass Yds' in season.keys():
                score += season['Pass Yds']/25.0
            if 'TD' in season.keys():
                score += season['TD']*4.0
            if 'Int' in season.keys():
                score -= season['Int']*2

        if 'Rush Yds' in season.keys():
            score += season['Rush Yds']/10.0
        if 'Rush TD' in season.keys():
            score += season['Rush TD']*6

        if 'Rec Yds' in season.keys():
            score += season['Rec Yds']/10.0
        if 'Rec TD' in season.keys():
            score += season['Rec TD']*6

        if 'FumL' in season.keys():
            score -= season['FumL']*2

        return score


    def print_stat_categories(self):
        self.stat_categories.sort()
        print self.position, self.stat_categories

if __name__ == "__main__":

    data_root = "./data/"
    positions = defaultdict(dict)
    for subdir, dirs, files in os.walk(data_root):
        if not dirs:
            year = subdir.split('/')[-1]
            for filename in files:
                if filename.split('.')[-1].lower() == 'csv':
                    position_name = filename.split('.')[0].upper()
                    position_dict = positions[position_name]

                    with open(os.path.join(subdir,filename),'rU+') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for obj in reader:
                            try:
                                name = obj["Name"]
                            except KeyError:
                                name = obj["Team"]

                            name = name.strip()

                            if name in position_dict.keys():
                                p = position_dict[name]
                            else:
                                p = Player(name, position_name)

                            p.add_season(year, obj)

                            if name not in position_dict.keys():
                                position_dict[name] = p
    pickle.dump(positions, open('stats.pkl','w+'))
