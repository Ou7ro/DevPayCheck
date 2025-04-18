import requests
from itertools import count
import time
from environs import env
from terminaltables import AsciiTable


def get_response_hhru(prog_language, page):
    hh_url = 'https://api.hh.ru/vacancies/'
    mosсow_id = 1
    payload = {
        'text': prog_language,
        'professional_role': 96,
        'area': mosсow_id,
        'period': 30,
        'page': page,
    }

    response = requests.get(hh_url, params=payload)
    response.raise_for_status()
    return response.json()


def get_response_superjob(prog_language, secret_key, sj_token, page):
    city = 'Москва'
    headers = {
        'X-Api-App-Id': secret_key,
        'Authorization': f'Bearer {sj_token}'
    }
    url_superjob = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'page': page,
        'town': city,
        'keyword': prog_language,
    }
    response = requests.get(url_superjob, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_statistics_hhru(popular_languages):
    vacancies_stats = {}
    for prog_language in popular_languages:
        try:
            all_salaries = []
            max_pages = 20
            for page in count(start=0):
                if page > 0:
                    time.sleep(0.5)

                full_response = get_response_hhru(prog_language, page)

                total_vacancies = full_response['found']
                actual_pages = min(full_response['pages'], max_pages)

                for vacancy in full_response['items']:
                    salary = predict_rub_salary_for_hh(vacancy['salary'])
                    if salary is not None:
                        all_salaries.append(salary)

                if page >= actual_pages - 1:
                    break

            avg_salary = sum(all_salaries) / len(all_salaries) if all_salaries else 0
            vacancies_stats[prog_language] = {
                'Вакансий найдено': int(total_vacancies),
                'Вакансий обработано': len(all_salaries),
                'Средняя зарплата': int(avg_salary),
            }
        except Exception as e:
            print(f'Ошибка обработки вакансий через HeadHunter для {prog_language}: {e}')
    return vacancies_stats


def get_statistics_sj(popular_languages, secret_key, sj_token):
    vacancies_stats = {}
    for prog_language in popular_languages:
        try:
            all_salaries = []
            for page in count(start=0):
                if page > 0:
                    time.sleep(0.2)
                full_response = get_response_superjob(prog_language, secret_key, sj_token, page)
                if not page:
                    total_vacancies = full_response['total']

                for vacancy in full_response['objects']:
                    salary = predict_rub_salary_for_superjob(vacancy)
                    if salary is not None:
                        all_salaries.append(salary)
                if not full_response['more']:
                    break

            avg_salary = sum(all_salaries) / len(all_salaries) if all_salaries else 0
            vacancies_stats[prog_language] = {
                'Вакансий найдено': int(total_vacancies),
                'Вакансий обработано': len(all_salaries),
                'Средняя зарплата': int(avg_salary),
            }
        except Exception as e:
            print(f'Ошибка обработки вакансий через SuperJob для {prog_language}: {e}')
    return vacancies_stats


def predict_rub_salary_for_hh(salary):
    if not salary:
        return None
    salary_from = salary['from']
    salary_to = salary['to']
    return calculate_average_salary(salary_from, salary_to)


def predict_rub_salary_for_superjob(salary):
    if not salary or salary['currency'] != 'rub':
        return None
    salary_from = salary['payment_from']
    salary_to = salary['payment_to']
    return calculate_average_salary(salary_from, salary_to)


def calculate_average_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    elif salary_from:
        return int(salary_from * 1.2)
    elif salary_to:
        return int(salary_to * 0.8)
    return None


def create_table_with_vacancies(vacancy_statistics, title):
    headers = ['Язык программирования'] + list(next(iter(vacancy_statistics.values())).keys())
    table_data = [headers]
    for prog_lang, statistic in vacancy_statistics.items():
        row = [prog_lang] + list(statistic.values())
        table_data.append(row)
    table = AsciiTable(table_data, title)
    return table.table


def main():
    try:
        env.read_env()
        secret_key = env.str('SECRET_KEY')
        sj_token = env.str('ACCESS_TOKEN')

        if not secret_key or not sj_token:
            raise ValueError("Не задан SECRET_KEY или ACCESS_TOKEN")

        title_hhru = 'HeadHunter Moscow'
        title_sj = 'SuperJob Moscow'
        popular_languages = [
            'Python',
            'Javascript',
            '1c',
            'ruby',
            'C',
            'C#',
            'C++',
            'PHP'
        ]

        print(create_table_with_vacancies(
            get_statistics_sj(popular_languages, secret_key, sj_token),
            title_sj))
        print(create_table_with_vacancies(
            get_statistics_hhru(popular_languages),
            title_hhru))
    except Exception as e:
        print(f'\nОшибка: {e}')


if __name__ == '__main__':
    main()
