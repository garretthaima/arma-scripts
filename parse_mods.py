from bs4 import BeautifulSoup
import re

def modlist(html_file):
    # html_file = "/home/garrett/code/Arma3Server/src/arma_mods.html"
    # html_text = requests.get(html_file).text
    soup = BeautifulSoup(open(html_file), 'html.parser')

    table = soup.find_all('table')[0]

    output_rows = []
    for row in table.findAll('tr'):
        col = row.findAll('td')
        # print(col)
        output_row = []
        for c in col:
            str = c.text.split("=")
            if len(str) > 1:
                output_row.append(re.sub("[^0-9a-zA-Z]+", "_", str[1].rstrip().lower()))
            if not (re.search("Steam", str[0])) and len(str) == 1:
                output_row.append(re.sub("[^0-9a-zA-Z@]+", "_", '@' + str[0].rstrip().lower()))
        output_rows.append(output_row)
    return output_rows
