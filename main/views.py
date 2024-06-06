from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings as settings
import json
import requests

telegram_channel_id = "-4264012790"

class CreatePollView(View):
    def get(self, request):
        return render(request, 'main/send_poll.html')

    def post(self, request, **kwargs):
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        poll_params = {
            "chat_id": telegram_channel_id,
            "question":"This is a poll",
            "options":json.dumps([
                    'option1',
                    'option2',
                    'option3'
                    ]),
            "is_anonymous":False,
            "allows_multiple_answers":False,
            "type":"regular",
        }
        response = requests.get(
            url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendpoll",
            params=poll_params
        )
        print(response.text)


        return HttpResponse("ok")