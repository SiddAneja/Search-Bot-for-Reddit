#! python3
import praw
import numpy
import pandas as pd
import datetime as dt
import getpass

reddit_username = input('Enter your Reddit username: ')
reddit_password = getpass.getpass('Enter your password: ')

reddit = praw.Reddit(client_id='BVXeVtgnBLrxIw', \
					client_secret='oZ3o62ldMh8jAn4oR1ysHVXAfPs', \
					user_agent='chatBotScraper', \
					username= reddit_username, \
					password= reddit_password)

all = reddit.subreddit('all')

thread_dict = { "Title":[], \
				"Score":[], \
				"ID":[], \
				"URL":[], \
				"Comms_Num":[], \
				"Created":[], \
				"Body":[]}
	#creating a dictionary to store the data from the subreddit
def get_date(Created):
 	return dt.datetime.fromtimestamp(Created) #Reddit uses UNIX timestamps to format date and time
 												#we can easily write up a function in Python to convert the entries to readable format

search = input('What can I help you with?\n')

for submission in all.search(search, limit=5):
	thread_dict["Title"].append(submission.title)
	thread_dict["Score"].append(submission.score)
	thread_dict["ID"].append(submission.id)
	thread_dict["URL"].append(submission.url)
	thread_dict["Comms_Num"].append(submission.num_comments)
	thread_dict["Created"].append(submission.created)
	thread_dict["Body"].append(submission.selftext)

thread_data = pd.DataFrame(thread_dict) #pandas library to put all the data into a spreadsheet called dataframe


timestampNew = (thread_data["Created"]).apply(get_date)
thread_data = thread_data.assign(timestamp = timestampNew)

thread_data.to_csv(r'C:\Users\Siddharth\Projects\RedditChatbot\browseReddit.csv', index=False)

# titles = thread_data['Title']
# print(titles[0:4])
# choice = input('Select the ')