
# defines funcionts
import pickle
import time, os
from instaloader.exceptions import BadCredentialsException
import pandas as pd
import numpy as np
import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile, islice
from varname import nameof
from math import ceil, floor

# LOAD CREDENTIALS
def load_credentials(file_name):

    try:
        with open('data/' + file_name, 'r') as file:
            creds = [line for line in file.read().splitlines()]

    except FileNotFoundError:
        print('Credentials file not found!')

    return {
        'user' : creds[0],
        'password' : creds[1]
    }

# CREATE LOADER AND PROFILE
def instance_loader(credentials):

    print('Instancing loader...')
    try:
        # Instance Instaloader Object
        loader = instaloader.Instaloader()
        # Start Session
        loader.login(credentials['user'], credentials['password'])
    except BadCredentialsException:
        print('Username or Password not valid!')

    return loader

# CREATE PROFILE OBJECT
def instance_profile(profile_name, loader):

    print('Creating Profile Object...')

    # Create Profile Object
    profile = instaloader.Profile.from_username(loader.context, profile_name)

    return profile

# GET FOLLOWERS FROM A PROFILE
def get_followers(profile):

    print('Fetching followers...', end=' ')
    before = datetime.now()
    followers = set(profile.get_followers())
    tdelta = datetime.now() - before
    print(f'done! {tdelta.seconds} seconds')

    return followers

# GET POST LIKES
def get_post_likes(post, index=0):

    print(f'Extracting Likes for Post #{index+1} - {post.shortcode}', end=' ')
    before = datetime.now()
    post_likes = [user for user in post.get_likes()]
    tdelta = datetime.now() - before
    print(f'done! {tdelta.seconds} seconds')

    return post_likes

# ADD ENGAGED USER LIST
def add_engaged_users(user_list, post_likes):

    print(f'Add to engaged_users list... ', end=' ')
    before = datetime.now()
    engaged_users = user_list | set([user.username for user in post_likes])
    tdelta = datetime.now() - before
    print(f'done in {tdelta.seconds} s')

    return engaged_users

# CREATE POST INFO DATA FRAME
def create_dataframe(df, post, like_count):

    print(f'Creating Data Frame... ', end=' ')
    before = datetime.now()
    df = pd.concat([df,
                    pd.DataFrame({
                        'shortcode' : post.shortcode,
                        'url' : post.url,
                        'date' : post.date,
                        'media_id' : post.mediaid,
                        'media_count' : post.mediacount,
                        'likes' : like_count,
                        'comments' : post.comments,
                        'is_video' : post.is_video,
                        'video_duration' : post.video_duration,
                        'viewer_has_liked' : post.viewer_has_liked,
                        'caption' : post.caption,
                        'caption_hashtags' : ','.join(post.caption_hashtags)
                    }, index=[0])
                    ])
    tdelta = datetime.now() - before
    print(f'done in {tdelta.seconds} s')

    return df

# 
def analyse_profile(followers, engaged_users, log=True):
    
    ghosts_followers = followers - engaged_users
    unsubscribed = engaged_users - followers
    true_followers = engaged_users - unsubscribed

    if log:
        print(f'Total followers: {len(followers)}')
        print(f'Total of engaged users: {len(engaged_users)}')
        print(f'Ghost followers: {len(ghosts_followers)}')
        print(f'Unsubscribed followers: {len(unsubscribed)}')
        print(f'True followers: {len(true_followers)}')
    
    return {
        'followers' : followers,
        'true_followers' : true_followers,
        'ghosts_followers' : ghosts_followers,
        'unsubscribed' : unsubscribed,
    }


