import GetSong
from ActionPerformer import ActionPerform as Action
import datetime as dt

# Setting variable from setup.txt here
# TOKEN = 'BQCXlVUBUtzcyOpndk3lG2gMczg4SQ7ImRUFXzrITHyVc_qWNl30RlnSYW0J3vdUj7TjcYPnawgJ8SPzcXTsqXvodCBEDFW_ZP_PShfvwRuehOtIjqSHJr4X7zez9_wukPER5rCpq8lwiPLz9Gsu7g24uz6z-SQiueqDR5w2msTgs4ybpu0R9r5KUw", "token_type": "Bearer", "expires_in": 3600, "refresh_token": "AQB637j2pDU6-KVW91OoMKjzTvr8SuwpDzMwbR_rvUxA19Ie4tCeRjj0dv2aALwfA7sRGGErCJnXFqIBEb6D52sZplRU08d9WXHImE9RbafYc4BqjULfSZrXURRdHder-UA' 
# headers = {
#     "Accept" : "application/json",
#     "Content-Type" : "application/json",
#     "Authorization" : "Bearer {token}".format(token=TOKEN)
# }


def wishMe(action):
    hour = int(dt.datetime.now().hour)
    if (hour >= 0) and (hour < 12):
        action.speak("Good Morning")
    elif (hour >= 12) and hour < 18:
        action.speak("Good Afternoon")
    else:
        action.speak("Good Evening")
    action.speak("This is Jarvis. Please tell me something to do")


if __name__ == "__main__":
    action = Action()
    wishMe(action)
    action.perform()
    
