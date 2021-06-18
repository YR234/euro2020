import datetime
from bs4 import BeautifulSoup
import requests
import time
import os




while True:
    games_hour = [13, 14, 16, 17, 19, 20]
    now = datetime.datetime.now().hour
#     print(now)
    if now not in games_hour:
        time.sleep(10*60)
    else:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

        url = 'https://www.uefa.com/livescores/?date='
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        today_url = f'{url}{date}'
        req = requests.get(today_url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        my_classes = soup.findAll('div')
        #
        # for div in my_classes:
        #     if "class" in div.attrs:
        #         if 'match' in div["class"][0]:
        #             print(div)
        # my_classes = soup.find_all("a", {"class": "match-row_link"})
        #
        # print(my_classes)


        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.chrome.options import Options
        import time
        import urllib.request
        from bs4 import BeautifulSoup
        from selenium import webdriver


        def download_by_xpathes(year_path, download_path, driver):
            link = driver.find_element_by_xpath()
            time.sleep(3)
            link.click()
            time.sleep(2)
            link = driver.find_element_by_xpath()
            link.click()


        from webdriver_manager.chrome import ChromeDriverManager
        from datetime import timedelta
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#         driver.get("https://www.google.com/")
#         print(driver.page_source)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.minimize_window()
        # PATH = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        # driver = webdriver.Chrome(executable_path=PATH)
        curr_date = datetime.datetime(2021, 6, 10)
        end_date = datetime.datetime(2021, 7, 11)
        today_url = 'https://www.uefa.com/livescores/?date=2021-06-12'
        done = False
        games_scores = []
        google_sheet_id = '1N9Gq9RN0eYzQrAnQHLeBA56odAtFrOds-0Ye8fjlpHU'


        def euro_game(team):
            teams = ['Italy',
                     'Switzerland',
                     'Turkey',
                     'Wales',
                     'Belgium',
                     'Denmark',
                     'Finland',
                     'Russia',
                     'Austria',
                     'Netherlands',
                     'North Macedonia',
                     'Ukraine',
                     'Croatia',
                     'Czech Republic',
                     'England',
                     'Scotland',
                     'Poland',
                     'Slovakia',
                     'Spain',
                     'Sweden',
                     'France',
                     'Germany',
                     'Hungary',
                     'Portugal']
            if team in teams:
                return True
            return False

        def euro_game2(team1, team2):
            teams = ['Italy',
                     'Switzerland',
                     'Turkey',
                     'Wales',
                     'Belgium',
                     'Denmark',
                     'Finland',
                     'Russia',
                     'Austria',
                     'Netherlands',
                     'North Macedonia',
                     'Ukraine',
                     'Croatia',
                     'Czech Republic',
                     'England',
                     'Scotland',
                     'Poland',
                     'Slovakia',
                     'Spain',
                     'Sweden',
                     'France',
                     'Germany',
                     'Hungary',
                     'Portugal']
            if team1 not in teams or team2 not in teams:
                return False
            return True

        def get_teams(game_text):
            team1, team2 = "0", "0"
            for i in range(len(game_text)):
                if euro_game(game_text[i]):
                    if team1 == '0':
                        team1 = game_text[i]
                    else:
                        team2 = game_text[i]
            return team1, team2


        def get_scores(game_text):
            # return 2, 2
            if '-' in game_text[1]:
                return game_text[1].split("-")[0], game_text[1].split("-")[1]
            return "@", "@"


        def fix_date_to_excel(date):
            #  6/11/2021
            return f'{date.day}/{date.month}/{date.year}'


        def create_row(team1, score1, team2, score2,date):
            date = fix_date_to_excel(date)
            return {
                'team1': team1,
                'score1': score1,
                'team2': team2,
                'score2': score2,
                'date': date
            }


        def fix_sort(results):
            return results.sort_values(["date", "team1"], ascending=(True, True))



        import pandas as pd

        results = pd.DataFrame(columns=['team1', 'score1', 'team2', 'score2'])

        while not done:
            curr_date += timedelta(days=1)
            url_date = f'{curr_date.year}-{curr_date.month}-{curr_date.day}'
            # driver.minimize_window()
            driver.get(f'{url}{url_date}')
            time.sleep(3)
#             print("Date")
            games = driver.find_elements_by_class_name('match-row_link')
            for game in games:
                game_text = game.text.split("\n")
                team1, team2 = get_teams(game_text)
                if euro_game2(team1, team2):
                    score1, score2 = get_scores(game_text)
                    row = create_row(team1, score1, team2, score2, curr_date)
                    results = results.append(row, ignore_index=True)
            if curr_date > end_date:
                done = True

        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        import gspread_dataframe as gd


        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("euro.json", scope)

        client = gspread.authorize(creds)
        title = 'תוצאות'
        sheet_name1 = 'יורו 2021 [-Internal-]'
        sheet_name2 = 'יורו 2021'
        try:
            work = client.open(sheet_name2)
        except:
            work = client.open(sheet_name1)
        sheets = [sheet.title for sheet in work.worksheets()]
        if title in sheets:
            sheet = work.worksheet(title)
            sheet.clear()
        try:
            ws = client.open(sheet_name2).worksheet(title)
        except:
            ws = client.open(sheet_name1).worksheet(title)
        results = fix_sort(results)
        gd.set_with_dataframe(ws, results)
        driver.close()
