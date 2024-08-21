# 自民党HPの議員略歴
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# memberURL.csv ファイルを適切なエンコーディングで読み込む
df = pd.read_csv('memberURL.csv', encoding='cp932')

# 取得したデータを格納するリスト
output_data = []

# 各URLに対してループを回す
for index, row in df.iterrows():
    url = row['url']
    giin = row['giin']
    num = row['num']

    # ページの内容を取得
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # データを抽出
    # 議員の役職（例: 参議院議員）
    position = soup.find("a", class_="btn is-g").text.strip() if soup.find("a", class_="btn is-g") else ""

    # 名前とルビ
    name_parts = soup.find_all("span", class_="ruby is-t")
    ruby_1 = name_parts[0]['data-ruby'] + " " + name_parts[0].text.strip() if len(name_parts) > 0 else ""
    ruby_2 = name_parts[1]['data-ruby'] + " " + name_parts[1].text.strip() if len(name_parts) > 1 else ""

    # 選挙区
    election_district = soup.find("th", text="選挙区").find_next_sibling("td").text.strip() if soup.find("th", text="選挙区") else ""

    # 当選回数
    election_times = soup.find("th", text="当選回数").find_next_sibling("td").text.strip() if soup.find("th", text="当選回数") else ""

    # 生年月日
    birth_date = soup.find("th", text="生年月日").find_next_sibling("td").text.strip() if soup.find("th", text="生年月日") else ""

    # 経歴
    career_html = soup.find("h2", class_="t-6 t-bg bgc-g mb").find_next("p").decode_contents() if soup.find("h2", class_="t-6 t-bg bgc-g mb") else ""
    career = career_html.replace("<br />", "\n").strip() if career_html else ""

    # 取得したデータを辞書に格納
    data = {
        "num": num,
        "giin": giin,
        "position": position,
        "name_ruby_1": ruby_1,
        "name_ruby_2": ruby_2,
        "election_district": election_district,
        "election_times": election_times,
        "birth_date": birth_date,
        "career": career
    }

    # 出力データに追加
    output_data.append(data)

    # 3秒待機
    time.sleep(3)

# データフレームに変換してCSVに保存
output_df = pd.DataFrame(output_data)
output_df.to_csv('output_data_html.csv', index=False, encoding='cp932', quoting=1)

print("データの取得と保存が完了しました。")
