#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import twitter
import sys
import os
import pickle
from os.path import abspath, dirname, join, exists
import argparse
from random import random, randint

script_dir = abspath(dirname(__file__))
sys.path.append(script_dir)

from statuses import render_random_status

CONSUMER_KEY='Upy5Rq4COQZNtijXS5w'
CONSUMER_SECRET='iRS0orX3AnXFSZECdQEr3rgFbc3zsfBSQek4TGS17M'

# Minimum amount of status updates for an account to be processed
MIN_STATUSES = 6000

# ASCII art from http://strawp.net/
FAILWHALE = """
Twitter is over capacity.

W     W      W        
W        W  W     W    
              '.  W      
  .-""-._     \ \.--|  
 /       "-..__) .-'   
|     _         /      
\'-.__,   .__.,'       
 `'----'._\--'      
VVVVVVVVVVVVVVVVVVVVV
"""

class TimeTweeter(object):
    def __init__(self, oauth_token, oauth_secret, consumer_key, consumer_secret, history_filename):
        self.auth=twitter.OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret)

        self.api = twitter.Twitter(auth=self.auth,
            secure=True,
            api_version='1',
            domain='api.twitter.com')

        self.history_filename = history_filename

    def run(self):
        # Get past victims from pickled file
        if exists(self.history_filename):
            self.history = pickle.load(open(self.history_filename, 'r'))
        else:
            self.history = {}

        print('History: %d users' % len(self.history))

        try:
            # Get data from Twitter API
            friends = self.api.statuses.friends()
            print("I have %d friends" % len(friends))
            followers = self.api.statuses.followers()
            print("I have %d followers" % len(followers))

            picks = self.api.users.suggestions.__getattr__('staff-picks')()['users']
            print("found %d people from staff-picks list" % len(picks))
        except twitter.api.TwitterHTTPError, e:
            print("HTTP error accessing Twitter API: %d" % e.e.code)
            if 500 <= e.e.code < 600:
                print(FAILWHALE)
            elif e.e.code == 400:
                print("Rate limited by Twitter API!")
            return
        except twitter.api.TwitterError, e:
            print("Error accessing Twitter API: %s" % e)
            return

        # Filter out the user's we've already done
        new_users = [user for user in picks if user['id'] not in self.history and user['statuses_count'] > MIN_STATUSES]

        # Give up for now if we don't find any new ones
        if not new_users:
            print("No new eligible victims!")
            return

        # Sort by statuses_count descending
        sorted_users = sorted(new_users, lambda a,b: cmp(a['statuses_count'], b['statuses_count']), reverse=True)

        # Grab the first one
        selected_user = sorted_users[0]
            
        # Do terrible things to them
        self.process_user(selected_user)

        # Save history file
        pickle.dump(self.history, open(self.history_filename, 'w'))

        print("done!")

    def process_user(self, user):
        print("Processing user %(id)s/%(screen_name)s:" % user)
        print("""%(statuses_count)d statuses
follows %(friends_count)d users
%(followers_count)d followers""" % user)

        # Calculate time spent tweeting
        tst = self.num_statuses_to_hours(user['statuses_count'])
        user.update({'time_tweeting':tst})
        print("time spent tweeting: %.1f hours" % tst)

        # Build new status
        status = self.get_message_template(user)
        if len(status) > 140:
            print('Status is too long - try again when fail != True')
            return

        # Post status and add user as friend
        print("Posting status update: \"%s\"" % status)
        try:
            self.api.statuses.update(status=status)
            self.api.friendships.create(id=user['id'])
        except twitter.api.TwitterHTTPError, e:
            print("HTTP error accessing Twitter API: %d" % e.e.code)
            if 500 <= e.e.code < 600:
                print(FAILWHALE)
            return

        # Save to history file
        self.history[user['id']] = {
            'screen_name' : user['screen_name'],
            'statuses_count' : user['statuses_count'],
            'time_tweeting': tst
        }

        
    def num_statuses_to_hours(self, num_statuses):
        # Assume one minute per status
        return num_statuses / 60.0


    def get_message_template(self, user):
        return render_random_status(user)
     


def main(args=[]):
    parser = argparse.ArgumentParser(description="Time spent tweeting bot")


    # oauth file
    parser.add_argument("--oauth-file", dest="oauth_filename", help="OAuth credentials",
            default=join(script_dir, '.twitter_oauth'))
    parser.add_argument("--history-file", dest="history_filename", help="History filename",
            default=join(script_dir, '.twitter_history'))
        
    options = parser.parse_args(args)

    if not os.path.exists(options.oauth_filename):
        from twitter.oauth_dance import oauth_dance
        oauth_dance(
            "timespenttweeting", CONSUMER_KEY, CONSUMER_SECRET,
            options.oauth_filename)

    oauth_token, oauth_secret = twitter.read_token_file(options.oauth_filename)
    print 'token is %s, secret is %s' % (oauth_token, oauth_secret)

    t = TimeTweeter(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET, options.history_filename)
    t.run()

if __name__ == '__main__':
    main(sys.argv[1:])

