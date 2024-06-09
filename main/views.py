from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings as settings
import json
import requests
from .models import Poll, User
MAX_POLL_OPTIONS = 10

telegram_channel_id = "-4264012790"

class CreatePollView(View):
    def get(self, request):
        return render(request, 'main/send_poll.html')

    def post(self, request, **kwargs):
        if 'send-poll__button' in request.POST:
            poll_options = []
            for i in range(MAX_POLL_OPTIONS):
                option = request.POST.get(f'option{i+1}')
                if option != "":
                    poll_options.append(option)
            points = request.POST.get('points')
            points = int(points) if points != "" else 0
            poll_name = request.POST.get('poll_name')
            right_answer = int(request.POST.get('correct_option')) - 1
            poll_params = {
                "chat_id": telegram_channel_id,
                "question": poll_name,
                "options": json.dumps(poll_options),
                "is_anonymous": False,
                "allows_multiple_answers": False,
                "type": "quiz",
                "correct_option_id": right_answer
            }
            response = requests.get(
                url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendpoll",
                params=poll_params
            )
            
            response_info = response.json()
            print(response_info)
            
            if response.status_code == 200:
                poll_obj = Poll.objects.create(
                    poll_telegram_id = response_info['result']['poll']['id'],
                    points = points,
                    poll_name = poll_name
                )
                poll_obj.save()

            return HttpResponse("ok")
        elif 'send-leaderboard__button' in request.POST:
            response = requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getUpdates")
            updates = response.json()['result']
            for update in updates:
                print(update['poll_answer'])
                print()
            # print(updates)
            return HttpResponse("ok")
    

# class SendLeaderboard(View):
#     def get(self, request):
#         return render(request, 'main/send_leaderboard.html')
    
#     def post(self, request):
#         pass
        