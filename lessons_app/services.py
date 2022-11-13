import requests
import json

from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor

from .models import Lesson, User, UserDetail, TimeBlock


python_any_where_domen = 'http://anyany123.pythonanywhere.com/'
user_url = 'api/add_user'
lesson_url = 'api/add_lesson'
block_url = 'api/add_block'


def check():
    print("it's working")
    users = get_users()

    i = 0
    for user in users:
        print('User: ', user)
        print('User dict: ', user.__dict__)
        # print('Telegram: ', user.details.telegram)
        print('Last login: ', user.last_login)
        # js = json.dumps(user.details.telegram)
        # print(js)
        js = json.dumps(user.last_login.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        print(js)
        # get_lessons_by_user(user=user.id)

        lessons = get_lessons_by_user(user.id)
        # if lessons:
        for lesson in lessons:
            print('LESSON:', lesson.__dict__)
            break

        i += 1
        if i >= 1:  # out of 51 (16.10.2022)
            break

    get_blocks()


def check1():
    print(User.objects.using('heroku_db').filter(id__gt=79)[:1][0].id)

    user1 = User.objects.using('heroku_db').get(id=1)
    # lessons = Lesson.objects.using('heroku_db').filter(student=user1)
    print('User1: ', user1.__dict__, end='\n\n')
    print('User1 dir: ', user1.__dir__(), end='\n\n')
    try:
        user1.details
    except BaseException:
        print('except')
    else:
        print(user1.details)
    # print('Lessons1: ', lessons.__dict__, end='\n\n')

    # users = User.objects.using('heroku_db').all()
    # for user in users:
    #     print(user.__dict__)
    #     print(user.__dir__())
    #     print(user.details)


# test
def get_users():
    users = User.objects.using('heroku_db').all().select_related('details')
    print('Users: ', users)
    print('Amount users: ', len(users))
    return users


# test
def get_lessons_by_user(user):
    user_lessons = Lesson.objects.using('heroku_db').filter(student=user)
    print('User lessons: ', user_lessons)
    print('Amount user lessons: ', len(user_lessons))
    return user_lessons


# test
def get_blocks():
    blocks = TimeBlock.objects.using('heroku_db').all()
    print('Blocks: ', blocks)
    print('Amount blocks: ', len(blocks))


def send_users_and_lessons():
    """ Send all users and them lessons """

    users = User.objects.using('heroku_db').all().select_related('details')
    for user in users:
        try:
            user.details
        except BaseException:
            # data = {
            #     'username': user.username,
            #     'first_name': user.first_name,
            #     'password': user.password,
            #     'phone': '',
            #     'telegram': '',
            #     'last_login': user.last_login.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            #     'date_joined': user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            # }
            continue
        else:
            data = {
                'username': user.username,
                'first_name': user.first_name,
                'password': user.password,
                'phone': user.details.phone,
                'telegram': user.details.telegram,
                'last_login': user.last_login.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'date_joined': user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }

        user_response = send(
            domen=python_any_where_domen,
            path=user_url,
            data=data
        )
        # print(user.details.phone)
        # print(type(user.details.phone))
        print(user_response)
        user_lessons = Lesson.objects.using('heroku_db').filter(student=user)
        for lesson in user_lessons:
            data = {
                'student': user_response['id'],
                'salary': lesson.salary,
                'time': lesson.time.strftime('%H:%M:%S.%f'),
                'date': lesson.date.strftime('%Y-%m-%d')
            }
            response = send(
                domen=python_any_where_domen,
                path=lesson_url,
                data=data
            )


def send_blocks():
    """ Send all blocks """

    blocks = TimeBlock.objects.using('heroku_db').all()
    for block in blocks:
        data = {
            'date': block.date.strftime('%Y-%m-%d'),
            'start_time': block.start_time.strftime('%H:%M:%S.%f'),
            'end_time': block.end_time.strftime('%H:%M:%S.%f')
        }
        response = send(
            domen=python_any_where_domen,
            path=block_url,
            data=data
        )


def send(domen, path, data):
    url = domen + path
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    return json.loads(response.content)


def main():
    send_users_and_lessons()
    send_blocks()
