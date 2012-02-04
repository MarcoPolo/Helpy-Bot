import random
insult_file = open('insults2.txt')
comp_file = open('comp.txt')
insults = insult_file.read().split('\n')
compliments = comp_file.read().split('\n')

def insult(text):
    user = text[0]
    tweet = ''
    while (tweet == '' or len(tweet) > 140):
        insult = insults[random.randint(0,96)]
        tweet = '@'+user+' ' + insult
    #api.update_status(tweet)
    print tweet

def compliment(text):
    user = text[0]
    tweet = ''
    while (tweet == '' or len(tweet) > 140):
        compliment = compliments[random.randint(0,45)]
        tweet = '@'+user+' ' + compliment
    #api.update_status(tweet)
    print tweet

insult(['dr_choc'])
compliment(['dr_choc'])
