from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import pickle
import pandas as pd

''' Initialize chatbot with unique name. '''
bot = ChatBot('JahkRAI',
              logical_adapters=[{
                  'import_path': 'chatterbot.logic.BestMatch',
                  'default_response': 'Wow, this is dope!',
                  'maximum_similarity_threshold': 0.90
              }])
trainer = ListTrainer(bot)

''' Load Dataset from pickle file '''
dataset_IG = open('./InstagramComments_.p', 'rb')
comments = pickle.load(dataset_IG)
dataset_IG.close()

commentDS = pd.read_csv('a.csv', encoding='utf-8-sig').to_dict()
commentDS = list(commentDS['comments'].values())

addComments = open('b.csv', 'a')
''' Train bot with given comments from dataset. 
for comment in comments:
    trainer.train(comment)
    addComments.write(f'{comment},\n')
addComments.close()

for comment in commentDS:
    trainer.train(comment)
    '''
''' Test bot '''
while True:
    request = input("You: ")
    response = bot.get_response(request)
    
    print(f'JahkRAI: {response}')