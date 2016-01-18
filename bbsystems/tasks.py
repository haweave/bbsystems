from __future__ import absolute_import

import datetime
import re
import requests
import xml.etree.ElementTree as ET

from celery import shared_task

from bbsystems.models import Team, Game, Atbat, Pitch

def get_games_for_range(start_date, end_date):
    """
    Get a list of all game links in an inclusive date range
    """

    games_list = []
    current_date = start_date

    while current_date < end_date and current_date < datetime.date.today():
        games_list = games_list + get_games_for_day(current_date)
        current_date = current_date + datetime.timedelta(days=1)

    return games_list

def get_games_for_day(date=datetime.date.today() - datetime.timedelta(days=1)):
    """
    Get a list of game links for a certain day
    """

    url = 'http://gd2.mlb.com/components/game/mlb/year_' + str(date.year) + '/month_'
    if date.month < 10:
        url += '0'
    url += str(date.month) + '/day_'
    if date.day < 10:
        url += '0'
    url += str(date.day)
    r = requests.get(url)
    games = re.findall(r'href="(gid_\d{4}_\d{2}_\d{2}_[^_]{6}_[^_]{6}_\d)', r.text)
    game_links = [url + '/' + x for x in games]
    return game_links

def process_games(game_links, parallel=False):
    """
    Import data from multiple games given their links
    """

    for game_link in game_links:
        if parallel:
            process_game.delay(game_link)
        else:
            process_game(game_link)

def process_pitch(pitch_elem, atbat, balls, strikes):
    """
    Create a pitch object from an xml node

    Returns (pitch_object, is_new) where pitch_object is the Pitch object
            and is_new is a boolean that is True only if a new pitch
            needs to be created for this object
    """

    kwargs = pitch_elem.attrib

    # had to rename invalid column names in model.
    for reserved_word in Pitch.reserved_fixes.keys():
        kwargs[Pitch.reserved_fixes[reserved_word]] = kwargs[reserved_word]
        del(kwargs[reserved_word])

    kwargs['balls'] = balls
    kwargs['strikes'] = strikes
    kwargs['atbat_num'] = atbat.num
    kwargs['game_id'] = atbat.game.id

    pitch = Pitch(**kwargs)
    return pitch

def process_atbat(atbat_elem, top_bottom, inning, game):
    """
    Create an atbat object from an xml node.
    Call process_pitch for every pitch in that atbat
    """
    kwargs = atbat_elem.attrib
    kwargs['inning'] = inning
    kwargs['top_bottom'] = top_bottom
    kwargs['game'] = game

    for delete_blank in Atbat.delete_blanks:
        if delete_blank in kwargs and kwargs[delete_blank] == '':
            del(kwargs[delete_blank])

    atbat = Atbat(**kwargs)

    balls = 0
    strikes = 0

    pitches = []

    for pitch_elem in atbat_elem:
        if pitch_elem.tag == 'pitch':
            pitch = process_pitch(pitch_elem, atbat, balls, strikes)
            pitches.append(pitch)
            if pitch.pitch_type == 'B':
                balls += 1
            else:
                if strikes < 2:
                    strikes += 1

    return (atbat, pitches,)

@shared_task
def process_game(game_link):
        """
        Create a Game object. Query the mlbam gameday xml files for that game.
        Call process_atbat for each atbat in that game
        """

        inning_url = game_link + '/inning/inning_all.xml'
        inning_r = requests.get(inning_url)
        if inning_r.status_code != 200:
            return
            # raise Exception('Could not find game_link: ' + game_link)
        root = ET.fromstring(inning_r.text.replace(u'\xed','').encode('utf-8').strip())

        match = re.search(r'(gid_(\d{4})_(\d{2})_(\d{2})_[^_]{6}_[^_]{6}_\d)', game_link)
        gid = match.group(1)
        date = datetime.date(int(match.group(2)), int(match.group(3)), int(match.group(4)))

        teams = re.findall(r'_([^_]{3})[^_]{3}',gid)

        away_team = Team.objects.get(short = teams[0])
        home_team = Team.objects.get(short = teams[1])

        Game.objects.filter(gid = gid).delete()

        game = Game(
            gid = gid,
            date = date,
            home_team = home_team,
            away_team = away_team,
        )
        game.save()

        atbats = []
        pitches = []

        # Innings and top/bottom are tedious and meaningless relationships.
        # We're just going to pin them in to the at bats.
        for inning_elem in root:
            inning = inning_elem.attrib['num']
            for top_bottom_elem in inning_elem:
                top_bottom = 1
                if top_bottom_elem.tag == 'bottom':
                    top_bottom = 0
                for atbat_elem in top_bottom_elem:
                    if atbat_elem.tag == 'atbat':
                        (ab, ps) = process_atbat(atbat_elem, top_bottom, inning, game)
                        atbats.append(ab)
                        pitches.extend(ps)

        Atbat.objects.bulk_create(atbats)
        Pitch.objects.bulk_create(pitches)
