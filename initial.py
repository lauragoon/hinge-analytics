import json
from sys import stderr

COUNT_CONNECTIONS = 0
COUNT_WE_MET = 0
COUNT_CHATS = 0
COUNT_MATCH = 0
COUNT_LIKE = 0
COUNT_BLOCK = 0

'''
data (list of dicts) - from given read json file
year (int) - year of data to be summarized, None if want all data

Summarize input data.
'''
def summarize_data(data, year=None):
    global COUNT_CONNECTIONS
    global COUNT_WE_MET
    global COUNT_CHATS
    global COUNT_MATCH
    global COUNT_LIKE
    global COUNT_BLOCK

    for connection in data:
        actions = set(connection.keys())

        # if need to filter for year
        if year is not None:
            connection_year = -1

            if 'match' in actions:
                connection_year = connection['match'][0]['timestamp'][0:4]
            elif 'like' in actions:
                connection_year = connection['like'][0]['timestamp'][0:4]
            elif 'block' in actions:
                connection_year = connection['block'][0]['timestamp'][0:4]
            else:
                stderr("ERROR: unexpected connection found to check year")

            if int(connection_year) != year:
                continue
        
        # count total num of connections
        COUNT_CONNECTIONS += 1

        # if we_met (w chats, match, [like])
        if 'we_met' in actions:
            actions.remove('we_met')
            COUNT_WE_MET += 1

        # if chats (w match, [like])
        if 'chats' in actions:
            actions.remove('chats')
            COUNT_CHATS += 1

        # if match (w [like])
        if 'match' in actions:
            actions.remove('match')
            COUNT_MATCH += 1

        # if like
        if 'like' in actions:
            actions.remove('like')
            COUNT_LIKE += 1

        # if block
        if 'block' in actions:
            actions.remove('block')
            COUNT_BLOCK += 1

        # else - ? 
        if len(actions) > 0:
            stderr("ERROR: encountered unexpected action: ", actions)

'''
filename (string)

Acquire json data from file.
'''
def get_data(filename):
    with open(filename, 'r', encoding='utf-8') as matches_file:
        matches_data = json.load(matches_file)
        return matches_data
