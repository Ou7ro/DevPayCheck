import requests


def get_response_hhru(vacant_languages):
    moskow_id = '1'
    hh_url = 'https://api.hh.ru/vacancies/'
    payload = {
        'professional_role': 96,
        'text': vacant_languages,
        'area': moskow_id,
        'period': 30,
    }

    response = requests.get(hh_url, params=payload)
    response.raise_for_status()
    return response.json()


#languages = ['Python', 'Javascript', '1c', 'ruby', 'C', 'C#', 'C++', 'PHP']

print(get_response_hhru(vacant_languages='Python'))

#vacancies = {}
