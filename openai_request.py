import openai , json
from openai import OpenAI

from openai import OpenAI
key = "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"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=key,
)
import json

def generate_prompt(stats_data,perf,team,prom):
    perf = 1 if perf else 0
    
    performance = ['defending' , 'attacking']
    prompt=[]
    prompt.append(f"As a football analysis expert, share your insights on the {team} team's  {performance[perf]} in less than 280 characters . data : {stats_data} ,  with a tweet. Start with a reaction comment and provide key stats. Note: Do not use emojis or any stickers in the tweet.")
    prompt.append(f"As a football analysis expert, provide insights on the {team} team's possession in a tweet. Start with a reaction comment and include key possession stats:Highlight any notable trends or strategies. #FootballAnalysis #PossessionStatsNote. Do not use emojis or any stickers in the tweet.data : {stats_data}")
    prompt.append(f"As a football analysis expert, provide insights on the {team} team's shooting performance in a tweet. Start with a reaction comment and include key stats: {stats_data}Note: Do not use emojis or any stickers in the tweet.")
    # Use the prompt with OpenAI API to generate the tweet-like summary
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt[prom]},
        ],
    )
    
    print("Tweet seccessfully Generated " )
    print("posting ...  " )
    return str(chat_completion.choices[0].message.content)


