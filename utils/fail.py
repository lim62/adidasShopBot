from lexicon import lexRU
from keyboards import (adminGetStarted,
                       moderGetStarted,
                       userGetStarted)

def failFunction(role: str) -> tuple:
    match role:
        case 'admin':
            text = lexRU['message']['failModer']
            markup = adminGetStarted()
        case 'moder':
            text = lexRU['message']['failModer']
            markup = moderGetStarted()
        case _: 
            text = lexRU['message']['failUser']
            markup = userGetStarted()
    return (text, markup)