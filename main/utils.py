from .models import Poll, User, PollAnswer
import requests
from django.conf import settings as settings
import ast


def get_updates():
    response = requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getUpdates")
    updates = response.json()['result']
    file = open('updates_file.txt', 'w')
    file.write(str(updates))
    file.close()


def read_updates():
    file = open('updates_file.txt', 'r')
    updates = ast.literal_eval(file.read())
    poll_answer_updates = [update["poll_answer"] for update in updates if "poll_answer" in update]
    # print(poll_answer_updates)

    for answer_update in poll_answer_updates:
        # Проверка наличия Telegram пользователя в базе
        try:
            user = User.objects.get(user_telegram_id=answer_update["user"]["id"])
        except:
            user = User.objects.create(
                user_telegram_id=answer_update["user"]["id"],
                username=answer_update["user"]["username"],
                total_points=0
            )
            user.save()
        # Проверка наличия опроса в базе
        try:
            poll = Poll.objects.get(poll_telegram_id=answer_update["poll_id"])
        except:
            continue
        # Проверка, был ли уже обработан голос пользователя
        try:
            poll_answer = PollAnswer.objects.get(user=user, poll=poll)
            if poll_answer:
                continue
        except:
            if answer_update["option_ids"][0] == poll.correct_option_id:
                user.total_points += poll.points
                user.save()
            PollAnswer.objects.create(
                user=user,
                poll=poll
            ).save()