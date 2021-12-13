# Imports an Defines
from defines import *

# SETUP 
# Instance empty objects
df = pd.DataFrame()
post_list = []
post_likes = {}
engaged_users = set()
# Start timer
init_time = datetime.now()
# Instagram credentials for login
credentials = load_credentials('credentials.txt')
# Base folder to save binaries data
folder = os.getcwd() + '\\binaries'
# Profile to scrape data
profile_name = 'cervejariamojica'

# START SCRAPING
# Instance Instaloader Object
loader = instance_loader(credentials)

# Create Profile Object
profile = instance_profile(profile_name, loader)

# Store a instance of each profile who follow the User -> instaloader.structures.Profile
followers = get_followers(profile)

# Extract Post information
print(f"Fetching Posts of profile {profile.username}.")
for index, post in enumerate(profile.get_posts()):
    
    loop_start = datetime.now()

    # Store Post instance -> instaloader.structures.Post
    post_list.append(post)
    key = post.shortcode

    print(f'{c["G"]}Post #{index+1}{c["W"]} <{key}> - Extracting Likes...')
    # Store a instance of each profile who liked the Post
    # Key: int -> Post Shorcode; Value: List -> instaloader.structures.Profile
    post_likes[key] = get_post_likes(post, index)
    # Add to unique engaged_users list
    engaged_users = add_engaged_users(engaged_users, post_likes[key])
    # Create Data Frame
    df = create_dataframe(df, post, like_count=len(post_likes[key]))
    # Random timer to avoid Bad Request
    time.sleep(float(np.random.choice(np.arange(0.5,2,0.1), 1)))
    tdelta = datetime.now() - loop_start
    print(f'time: {tdelta.seconds//60}min {tdelta.seconds%60}secs') 
    print('Fetching next post...')

# Analyse Users profiles
followers_profile = analyse_profile(followers, engaged_users)

# Prepare to save data
folder += '\\' + profile_name
os.makedirs(folder, exist_ok=True)
print(f'Saving data in folder:\n {folder}')

# Post List
with open(folder + '\\' + profile_name + '_' + 'post_list' + '.pkl','wb') as pickle_file:
        pickle.dump(post_list, pickle_file)
# Post Likes
with open(folder + '\\' + profile_name + '_' + 'post_likes' + '.pkl','wb') as pickle_file:
        pickle.dump(post_likes, pickle_file)
# Followers profile
with open(folder + '\\' + profile_name + '_' + 'followers_profile' + '.pkl','wb') as pickle_file:
        pickle.dump(followers_profile, pickle_file)
# Data Frame
with open(folder + '\\' + profile_name + '_' + 'df' + '.pkl','wb') as pickle_file:
        pickle.dump(df, pickle_file)

final_time = datetime.now() - init_time

print('Scrap complete!')
print(f'Total time: {final_time.seconds//3600}:{final_time.seconds//60}:{final_time.seconds%60}')
