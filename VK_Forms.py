import requests
import json
import pandas as pd
import webbrowser
import re

app_id = "12345678"  # идентификатор Standalone-приложения
scope = "groups"  # права доступа на группу

# формируем URL для получения access_token и открываем URL в браузере
url = f"https://oauth.vk.com/authorize?client_id={app_id}&redirect_uri=https://oauth.vk.com/blank.html&display=page&scope={scope}&response_type=token&v=5.131"
webbrowser.open(url)

# ждём авторизацию и подтверждение доступа и извлекаем access_token из URL-адреса
access_token_url = input("Введите URL из адресной строки после подтверждения доступа: ")
access_token = re.search(r"access_token=([^&]*)", access_token_url).group(1)

# проверяем, что access_token действительный, можно в целом удалить, но пусть будет на всякий случай
response = requests.get(f"https://api.vk.com/method/account.getProfileInfo?access_token={access_token}&v=5.131")

if response.status_code == 200:
    print("Access token получен!")
else:
    print("Не удалось получить access token")

# Данные по группе и форме, а также ссылка для запросов
group_id = 123456789
form_id = 1
url_stats = 'https://api.vk.com/method/leadForms.getLeads?group_id={}&form_id={}&access_token={}&v=5.131'.format(group_id, form_id, access_token)

response_stats = requests.get(url_stats)

if response_stats.status_code == 200:
    data = json.loads(response_stats.text)
    leads = data['response']['leads']

    # Создаем список словарей, где каждый словарь представляет отдельный лид с его ответами
    leads_data = []
    for lead in leads:
        lead_data = {'lead_id': lead['lead_id'], 'user_id': lead['user_id'], 'date': lead['date']}
        for answer in lead['answers']:
            lead_data[answer['key']] = answer['answer']['value']
        leads_data.append(lead_data)

    # Создаем датафрейм из списка словарей
    df = pd.DataFrame(leads_data)
else:
    print('Произошла ошибка при запросе к API VK')

df.head()