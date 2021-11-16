import requests

def get_acc_feed():
    """Gets the info about the last post"""
    url = "https://instagram40.p.rapidapi.com/account-feed"

    querystring = {"username":"student_council_nis_kst"}

    headers = {
        'x-rapidapi-host': "instagram40.p.rapidapi.com",
        'x-rapidapi-key': "75a080a24bmsh79caf9b2328fd8dp167288jsn32cf0cdfd80d"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


while(True):

    acc_feed = get_acc_feed()

    prev = []
    next = []

    for i in range(12):
        prev.append(acc_feed[i]['node']["shortcode"])

    
    
    text = last_post['node']['edge_media_to_caption']['edges'][0]['node']['text']
    shortcode = last_post['node']["shortcode"]

    text + "\nСсылка на инстаграм пост: https://www.instagram.com/p/" + shortcode