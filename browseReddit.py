import praw
import numpy
import pandas as pd
import datetime as dt
import getpass
import webbrowser as web
# import pickle
# import codecs

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

for submission in all.search(search, limit=10):
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

#saves the data from reddit onto a .csv file
thread_data.to_csv(r'C:\Users\Siddharth\Projects\RedditChatbot\browseReddit.csv', index=False)
print('File saved')

titles = thread_data['Title'] #saves all the titles from the dataframe 
print(titles[0:5]) #prints the first 5 titles to display them to the user
print("\n")
#Start of discussion with the user
print('Enter "l" to load more, or ')
while True:
	print("Enter 'q' to Quit, or ")
	choice = input('Enter the index of the article you like to get more information about: ')
	#if the choice is a number enter this branch
	if(choice.isdigit()):
		#store the information from the dataframe at the index entered in a variable called info
		info = thread_data.iloc[int(choice)]
		print(info)
		#prompt the user if they want to read the article on a browser
		choice = input('Want to open this on your browser? Enter Yes or No: ')
		if(choice.lower() == 'yes'):
			web.open(info.get('URL'))
			#the following code saves the entire reddit post in a txt file
			reddit.config.decode_html_entities = True
			submission = reddit.submission(id=info.get('ID')) #extracts the submission using the id of the post
			submission.comments.replace_more(limit=None) #uses the replace_more method to get rid of the morecomments and load all of them
			#creates a file called comments.txt and saves the post to it
			f = open('comments.txt', 'w+')
			f.write(info.get('Title') + "\n")
			f.write(info.get('Body') + "\n")
			for comment in submission.comments.list():
				f.write(str(comment.body.encode("utf-8")))

		elif(choice.lower() == 'no'):
			continue
		else:
			print("Invalid Input")
	#this branch checks if the user wants to load more data or quit
	else:
		if(choice == 'l' or choice == 'L'):
			print(titles[5:])
			print("\n")
		elif(choice == 'q' or choice == 'Q'):
			break
		else:
			print('Invalid input.')

print("Thanks for using the Reddit Search Bot")