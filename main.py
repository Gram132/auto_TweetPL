from dataAPI import setData
from dataAPI import check_ID
from openai_request import generate_prompt
from tweet_it import post_tweet 
#get data
ID =11352356
data=setData(ID)
check_ID(ID)
#attack or deffence
ad = 0
#home or away 
ha = 'home'
# which prompt performance :0 , possession :1 , shoots :2 
prompt= 1
#generate tweet
text = generate_prompt(data,ad,"away",1)

#post tweet
print(text) 
user_response = input("Are you sure you want to post it? (yes/y/Y for yes): ")

if user_response.lower() in ["yes", "y"]:
    # Execute your script here
    print("Posting...")
    post_tweet(text)
else:
    print("Not posting.")