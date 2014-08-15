"""
Creates a nice tidy pickle file of the data in the data/ directory.
"""

import os
import requests
import csv
import pickle
from collections import defaultdict
import pprint
import string
import json
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

def load_historical_stats():
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

def get_ffc_adps():
    ffc_file = requests.get('http://fantasyfootballcalculator.com/adp_csv.php?format=standard&teams=12')
    ffc_reader = csv.reader(ffc_file.text.split('\n'))

    players = []

    # skip first 5 rows; header info
    skip_rows(ffc_reader, 5)

    for row in ffc_reader:
        if len(row) == 7:
            players.append({"name":normalize_name(row[2]),
                            "adp":row[1],
                            "pos":row[3],
                            "team":row[4],
                            "bye":row[6]})

    return players

def skip_rows(obj,num):
    for x in range(num):
        # skip first 5 rows; header info
        obj.next()

def get_fp_xls(url, position):
    players = []

    request = requests.get(url)
    r = csv.reader(request.text.split('\n'),delimiter='\t')
    skip_rows(r, 6)
    for row in r:
        row = map(string.strip, row)
        if len(row) > 1:
            players.append({"name":normalize_name(row[0]),
                            "team":row[1],
                            "pos": position,
                            "projected_pts":float(row[-2])})

    return players

def normalize_name(name):
    if name == "Christopher Ivory":
        name = "Chris Ivory"
    if name == "Ty Hilton":
        name = "TY Hilton"

    return name.replace('.','').replace("'",'')

if __name__ == "__main__":
    players = []

    players.extend(
        get_fp_xls("http://www.fantasypros.com/nfl/projections/qb.php?export=xls",
                   "QB"))

    players.extend(
        get_fp_xls("http://www.fantasypros.com/nfl/projections/rb.php?export=xls",
                   "RB"))

    players.extend(
        get_fp_xls("http://www.fantasypros.com/nfl/projections/wr.php?export=xls",
                   "WR"))

    players.extend(
        get_fp_xls("http://www.fantasypros.com/nfl/projections/te.php?export=xls",
                   "TE"))

    adps = get_ffc_adps()
    for player in adps:
        if player['pos'] in ['QB','RB','WR','TE','DEF']:
            results = [x for x in enumerate(players)
                       if x[1]['name'] == player['name']]
            if len(results) == 0:
                if player['pos'] == 'DEF':
                    players.append({'name':player['name'],
                                    'adp':player['adp'],
                                    'pos':player['pos']})
                else:
                    print 'NO MATCH:', player['name']

            elif len(results) > 1:
                print 'MULTIMATCH:', player['name'], str(results)

            else:
                players[results[0][0]]['adp'] = float(player['adp'])
                players[results[0][0]]['bye'] = player['bye']

    for i in range(12):
        players.append({'name':"Generic Kicker",
                        'adp':-1,
                        'pos':"K"})
    for i in range(4):
        players.append({'name':"Generic Defense",
                        'adp':-1,
                        'pos':"DEF"})

    with open('players.js','w+') as outfile:
        outfile.write("players = " + json.dumps(players))
