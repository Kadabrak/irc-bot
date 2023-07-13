import wikipedia
def wiki(*arg):
    if arg != (None,):
        wikipedia.set_lang("en")
        result = wikipedia.search(' '.join(arg))

        if result == []:
            message = 'no result'

        else:
            result = result[0].split(' ')
            message = "https://wikipedia.org/wiki/"+"_".join(result)

    else:
        message = "You don't have specify a page to search"

    return message

    
