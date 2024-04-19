import pandas as pd
import requests
import fake_useragent
from bs4 import BeautifulSoup


def get_diary(login: str, password: str, logging_str='') -> pd.DataFrame:
    link = "https://elschool.ru/Logon/Index"
    session = requests.Session()

    if logging_str:
        print(f"{logging_str}: обработка запроса")

    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    data = {
        'from_sent': '1',
        'login': login,
        'password': password
    }
    response = session.post(link, data=data, headers=header)
    st1 = response.url
    if logging_str:
        print(f"{logging_str}: выполнен вход")
    if st1 != f"https://elschool.ru/users/privateoffice":
        raise ValueError
    response = response.text
    current_url = (session.get("https://elschool.ru/users/diaries")).url
    current_url = current_url.replace("details", "grades")
    page = session.get(current_url).text
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', {'class': 'GradesTable'})
    html_string = table.prettify()
    df = pd.read_html(html_string)[0]
    return df


part_name_by_count = {
    6: 'полугодие',
    8: 'триместр',
    10: 'четверть'
}


def _normalise(grade: str) -> str:
    norm_gr = grade[0] + '.'
    for digit in grade[1:]:
        if digit == '.':
            break
        norm_gr += digit
    if len(norm_gr) == 2:
        norm_gr += '0'
    return norm_gr


def get_emoji(grade: str) -> str:
    if grade[0] == '5' or (grade[0] == '4' and grade[2] in '56789'):
        return '🟢'
    if grade[0] == '4' or (grade[0] == '3' and grade[2] in '56789'):
        return '🔵'
    if grade[0] == '3' or (grade[0] == '2' and grade[2] in '56789'):
        return '🟡'
    return '🔴'


def to_str(df: pd.DataFrame) -> str:
    table = ''

    for tpl in df.iterrows():
        for row in tpl[1::2]:
            table += f"{row['Предмет']}) {row['Предмет.1']}\n"
            for index, field in enumerate(row[2:], start=2):
                if str(field) == 'nan':
                    continue
                if type(field) == float:
                    table += f"{(index >> 1)} {part_name_by_count[len(row)]} "
                    grade = _normalise(str(field))
                    table += f"{get_emoji(grade)} {grade}"
                elif type(field) == str:
                    table += field.replace(' ', '')
                table += '\n'
            table += '\n'

    return table[:-1]
