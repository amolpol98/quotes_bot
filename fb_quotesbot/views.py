from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
from django.http.response import HttpResponse
import json, pprint, requests, re, random

pp = pprint.PrettyPrinter(indent=4)

quotes = {
    'love': ["""I'm selfish, impatient and a little insecure. I make mistakes, I am out of control and at times hard to handle. But if you can't handle me at my worst, then you sure as hell don't deserve me at my best.""",
            """You know you're in love when you can't fall asleep because reality is finally better than your dreams."""],
    'inspirational':    ["""Be yourself; everyone else is already taken.""",
            """Be the change that you wish to see in the world."""],
    'life':   ["""Don't cry because it's over, smile because it happened.""",
                """You only live once, but if you do it right, once is enough."""]
         }

# Create your views here.
class QuotesBotView(generic.View):
    def get(self, request, *args, **kwargs):
        print self.request.GET
        if self.request.GET['hub.verify_token'] == '9768087465':
            print self.request.GET
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pp.pprint(message)
                    post_facebook_message(message['sender']['id'],message['message']['text'])
        return HttpResponse()

def post_facebook_message(fbid, received_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',received_message).lower().split()
    quote_text = ''
    for token in tokens:
        if token in quotes:
            quote_text = random.choice(quotes[token])
            break
    if not quote_text:
        quote_text = "I didn't understand! Send 'love', 'inspirational', 'life' for a quote!"
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAYZCkIRMZC58BADZAIS0w7GGLfC8ikS2oceczWIjkiBK4jIsL1pMzGYZCqLU9fZAFtR9qmBz2r8temLs1wHK5ZCArSXj3TMg8N5msofYxGbvocGlFnHSfRaBxJEMjoPKEBI6zIt6CeIZBYbpZC71gfO87DxG91j6SUP3uQrZCGKDBwZDZD'}
    user_details = requests.get(user_details_url, user_details_params).json()
    print user_details
    quote_text = 'Hi '+user_details['first_name']+'..! ' + quote_text
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAYZCkIRMZC58BADZAIS0w7GGLfC8ikS2oceczWIjkiBK4jIsL1pMzGYZCqLU9fZAFtR9qmBz2r8temLs1wHK5ZCArSXj3TMg8N5msofYxGbvocGlFnHSfRaBxJEMjoPKEBI6zIt6CeIZBYbpZC71gfO87DxG91j6SUP3uQrZCGKDBwZDZD'
    response_msg = json.dumps({'recipient': {'id':fbid},'message':{'text':quote_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pp.pprint(status.json())
