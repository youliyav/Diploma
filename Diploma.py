import urllib3
import json
from user import User
from config import TOKEN
from pprint import pprint


def groups_format(groups):
    res = []
    for group in groups:
        res.append({'name': group['name'],
                    'gid': group['id'],
                    'members_count': group['members_count']})
    return res


def save_file(data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # source_uid = 171691064
    source_uid = input('Введите идентификатор пользователя: ')
    usr = User(TOKEN, source_uid)
    groups = usr.get_unique_groups()
    groups_result = groups_format(groups)
    save_file(groups_result, 'groups.json')
    pprint(groups_result)
