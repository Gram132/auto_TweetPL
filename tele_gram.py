import time
from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler , MessageHandler, filters, ContextTypes
from dataAPI import check_ID, setData
from openai_request import generate_prompt
from tweet_it import post_tweet


TOKEN:Final = "6205153938:AAHDqdoG21pmsPnBVFU1AEJByYLZGRlWM_k"
BOT_USERNAME:Final="XtweetIt_bot"
Game_ID = 000000
#Commands
async def start_command(update:Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey there! you ready to tweet !")

async def new_tweet(update:Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey there! you ready to tweet !")
    await update.message.reply_text("Enter your match ID ")
    context.user_data['state'] = 'newid'





#Responses
def handle_response(text:str , context:ContextTypes.DEFAULT_TYPE  ) ->str :
    processed:str =text.lower()
    #print("User input :"+ text)
    if 'state' in context.user_data and context.user_data['state'] == 'newid':
        try:
            gameID = context.user_data['match_id']=int(text)
            context.user_data['state'] = 'WAITING_FOR_MATCH_ID'
            print('Checking ID ...')
            gameTeams = check_ID(gameID)
            if gameTeams != 0:
                context.user_data['state'] = 'id_valid'
                context.user_data['Game_ID'] =gameID
                context.user_data['awayTeam'] =gameTeams['away']
                context.user_data['homeTeam'] =gameTeams['home']
                return f" enter 1 for {context.user_data['homeTeam']} and 2 for {context.user_data['awayTeam']}"
            else:
                context.user_data['state'] = 'newid'
                return "Game ID is not valid, please try again"
        except:
            context.user_data['state'] = 'newid'
            return "Invalid Game ID, please enter a valid number."

    if 'state' in context.user_data and context.user_data['state'] in ['id_valid' ,'team_valid','perf_valid','prompt_readdy','NEXT']:
        print( context.user_data['state'])
        if context.user_data['state'] == 'id_valid':
            user_input =int(text)
            if user_input in [1,2]:
                context.user_data['state'] = 'team_valid'
                context.user_data['team_choised'] = 'home'if user_input == 1 else 'away'
                return "Now please enter 1 for attack performance and 2 for defense performance"
            else:
                context.user_data['state'] = 'id_valid'
                return f"Input out of range, enter 1 for {context.user_data['homeTeam']} and 2 for {context.user_data['awayTeam']}"
        if context.user_data['state'] == 'team_valid':
            user_input =int(text)
            if user_input in [1,2]:
                context.user_data['state'] = 'perf_valid'
                context.user_data['perf_choised'] = 1 if user_input == 1 else 0
                return "Perfect, Now what prompt model do you want to generate?\nEnter:\n1: for attack / defending performance\n2: for possession performance\n3: for shots performance"
            else:
                context.user_data['state'] = 'team_valid'
                return "Input out of range ,please enter 1 for attack performance and 2 for defense performance"
        
        if context.user_data['state'] == 'perf_valid':
            user_input =int(text)
            if user_input in [1,2,3]:
                context.user_data['state'] = 'prompt_readdy'
                context.user_data['prompt'] = user_input -1
                if context.user_data['state'] == 'prompt_readdy':
                    try:
                        data=setData(context.user_data['Game_ID'] )
                        #attack or defense
                        ad = context.user_data['perf_choised']
                        #home or away 
                        ha = context.user_data['team_choised']
                        # which prompt performance :0 , possession :1 , shoots :2 
                        prompt= context.user_data['prompt']
                        #generate tweet
                        tweet_generated = generate_prompt(data,ad,ha,prompt)
                        context.user_data['state'] = 'NEXT'
                        context.user_data['tweet_generated'] =tweet_generated
                        return f"Data has been seccessufully Scrapted .. \n\n\n{tweet_generated} \n\n\ntype\n1 : To post on Twitter (X)\n2 : To change parameters"
                    except ValueError:
                       print(ValueError)
                       context.user_data['state'] = 'perf_valid'
                       return"input out of range please, enter:\n1: for attack / defending performance\n2: for possession performance\n3: for shots performance"
                else:
                    context.user_data['state'] = 'perf_valid'
                    return"input out of range please, enter:\n1: for attack / defending performance\n2: for possession performance\n3: for shots performance"
            else:
                context.user_data['state'] = 'perf_valid'
                return"input out of range please, enter:\n1: for attack / defending performance\n2: for possession performance\n3: for shots performance"
    if 'state' in context.user_data and context.user_data['state'] == 'NEXT':
        user_input =int(text)
        if user_input in [1,2]:
            if user_input == 1 :
                try:
                    post_tweet(context.user_data['tweet_generated'] )
                    context.user_data['state'] = 'newid'
                    return "Posted Successfully "
                except:
                    context.user_data['state'] = 'newid'
                    return "Apologies, we encountered an issue while processing your request. Kindly try again later."
            else :
                try:
                    context.user_data['state'] = 'id_valid'
                    return f"Input out of range, enter 1 for {context.user_data['homeTeam']} and 2 for {context.user_data['awayTeam']}"
                except:
                    context.user_data['state'] = 'newid'
                    return "Apologies, we encountered an issue while processing your request. Kindly try again later."
        else:
            context.user_data['state'] = 'NEXT'
            return f"Input out of range \n\n\n{tweet_generated} \n\n\nplease type\n1 : To post on Twitter (X)\n2 : To change parameters"
    else:
        print( context.user_data['state'])
        return 'Soory i am not a modul language , Ask again !'


async def handle_message(update:Update , context:ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text:str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type =='group':
        if BOT_USERNAME in text :
            new_text:str = text.replace(BOT_USERNAME,'').strip()
            response:str = handle_response(new_text)
        else:
            response:str =handle_response(text ,context)

    else:
        response: str = handle_response(text ,context)
    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update:Update , context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app =Application.builder().token(TOKEN).build()

   # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('new_tweet', new_tweet))

    #Message
    app.add_handler(MessageHandler(filters.TEXT , handle_message))

    #Errors
    app.add_error_handler(error)

    #Pool the bot
    print('Polling ...')
    app.run_polling(poll_interval=3)