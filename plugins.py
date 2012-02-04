def insult(text):
    text = text[text.find('#'):]
    text = text[:find(' ')+1]
    text = text.strip(' ')
    api.update_status('@'+text+' hey ugly!')
