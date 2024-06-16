from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings as settings
import json
import requests
from .models import Poll, User, PollAnswer
from .utils import get_updates, read_updates
MAX_POLL_OPTIONS = 10


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
                "chat_id": settings.TELEGRAM_GROUP_ID,
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
                Poll.objects.create(
                    poll_telegram_id = response.json()["result"]["poll"]["id"],
                    question=poll_name,
                    points=points,
                    correct_option_id=right_answer
                ).save()

            return HttpResponse("ok")
        elif 'send-leaderboard__button' in request.POST:
            get_updates()
            read_updates()
            users = User.objects.order_by("-total_points")
            message_text = "Таблица лидеров:\n"
            for i, user in enumerate(users):
                message_text += f"{i+1}: {user.username} - {user.total_points}\n"
            leaderboard_params = {
                "chat_id": settings.TELEGRAM_GROUP_ID,
                "text": message_text
            }
            response = requests.get(
                url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
                params=leaderboard_params
            )
            print(response.json())
            return HttpResponse("Таблици лидеров отправлена в группу")
    

# class SendLeaderboard(View):
#     def get(self, request):
#         return render(request, 'main/send_leaderboard.html')
    
#     def post(self, request):
#         pass
        