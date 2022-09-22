# imports
import json
import urllib.request
import os

# lambda event
def lambda_handler(event, context):
    
    # api details
    url = os.environ["API_URL"]
    
    headers = {
    	"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    	"X-RapidAPI-Host": os.environ["RAPIDAPI_HOST"]
    }
    
    slack_hdrs = {'Content-Type': 'application/json'}    
    
    # make api request
    req_rapid = urllib.request.Request(url, headers = headers)
    res_rapid = urllib.request.urlopen(req_rapid)
    res_data = res_rapid.read()
    
    # parse returned stories
    stories = json.loads(res_data)
    story = str(stories[0])

    for item in stories:
        link = item["link"]
        title = item["title"]
        img = item["img"]
        date_time = item["dateTime"]

    # parse a story
    response_body = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":newspaper: New Story published on 9to5 Mac"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*<https://{0}|{1}>*\n".format(link, title)
                },
                "accessory": {
                    "type": "image",
                    "image_url": img,
                    "alt_text": "tech"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Article posted: {0}".format(date_time)
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    }
    
    # debug
    print(story)
    
    # send to slack
    req_slack = urllib.request.Request(os.environ["WEBHOOK_URL"], json.dumps(response_body).encode('utf-8'), headers = slack_hdrs)
    res_slack = urllib.request.urlopen(req_slack)
    response = res_slack.read()
    print(response)
