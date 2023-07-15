import wikipedia
def wiki(arg =[]):
    description = None
    arg = arg.split(' ')
    try:
        nbr_sentences = int(arg[0])
        del arg[0]
    except ValueError:
        nbr_sentences = None
    if arg != []:
        wikipedia.set_lang("en")
        term_to_search = ' '.join(arg)
        all_results = wikipedia.search(term_to_search)


        if all_results == []:
            message = 'no result'

        else:
            result = all_results[0]
            message = "https://en.wikipedia.org/wiki/"+result.replace(' ','_')
            try:
                result_page = wikipedia.page(result)
                if nbr_sentences != None:
                    description = wikipedia.summary(result_page.title, sentences=nbr_sentences)
            except:
                description = "sry i can't get the description"

    else:
        message = "pas de page spécifié"

    return message,description



