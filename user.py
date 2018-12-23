import requests
import time
from pprint import pprint


class User:

    def __init__(self, token, source_uid):
        self.token = token
        self.source_uid = self.resolve_uid(source_uid)

    def resolve_uid(self, user_id):
        """
        Дано uid или строка, задача понять число или строка.
        Использую метод класса строка isnumeric
        Если это число, возвращаю user_id
        Если вернуло False, то делаем 'https://api.vk.com/method/users.get'
        и оттуда вычленяем user_id

        """
        if user_id.isnumeric():
            return user_id
        params = {'access_token': self.token,
                  'user_ids': user_id,
                  'v': '5.85'}
        response = requests.get('https://api.vk.com/method/users.get', params, verify=False, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data['response'][0]['id']

    def get_friends(self):
        params = {'access_token': self.token,
                  'user_id': self.source_uid,
                  'fields': 'nickname',
                  'v': '5.85'}
        response = requests.get('https://api.vk.com/method/friends.get', params, verify=False)
        data = response.json()
        pprint(data)
        return data['response']

    def get_groups(self, user_id=None):
        if user_id is None:
            user_id = self.source_uid
        try:
            params = {'access_token': self.token,
                      'user_id': user_id,
                      'extended': 1,
                      'fields': 'members_count',
                      'v': '5.85'}
            response = requests.get('https://api.vk.com/method/groups.get', params, verify=False, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            print(exc.__doc__)
            raise
        else:
            result = response.json()
            if 'error' in result:
                if result['error']['error_code'] == 6:  # Too many requests per second
                    time.sleep(0.5)
                    return self.get_groups(user_id)
                else:
                    return {'items': []}
            else:
                return result['response']

    def get_unique_groups(self):
        gr_response = self.get_groups(self.source_uid)
        groups = gr_response['items']
        fr_response = self.get_friends()
        friends = fr_response['items']
        gr_list = [i['id'] for i in groups]
        group_friends_count = dict.fromkeys(gr_list, 0)
        res = []
        for friend in friends:
            print(friend)
            friend_groups_response = self.get_groups(friend['id'])
            friend_groups = friend_groups_response['items']
            for group in friend_groups:
                if group['id'] in group_friends_count.keys():
                    group_friends_count[group['id']] += 1
        for group in groups:
            if group_friends_count[group['id']] == 0:
                res.append(group)
        return res
