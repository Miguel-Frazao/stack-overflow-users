from bs4 import BeautifulSoup
import requests

pags = 1 # num de pags a fazer requests
params = {'tab': 'Reputation', 'filter': 'all'}
score, users, badges = [], [], []

for pag in range(1, pags+1):
    print('parsing page {}'.format(pag))
    params['page'] = pag
    req = requests.get('http://stackoverflow.com/users', params=params)
    soup = BeautifulSoup(req.text, 'html.parser')
    users_html = soup.select('.user-info div.user-details a')
    users.extend(i.text for i in users_html)
    badges_html = soup.select('.user-info .badgecount')
    badges_text = [int(i.text) for i in badges_html]
    badges.extend(badges_text[i:i+3] for i in range(0, len(badges_text), 3))
    score_html = soup.select('.user-info span.reputation-score')
    for i in score_html:
        try:
            score.append(int(i['title'].split()[-1].replace(',', '')))
        except:
            score.append(int(i.text.split()[-1].replace(',', '')))
#print(badges, '\n\n')
data = list(zip(users, score, badges))
#print(data)

print('\nRANKING STACK OVERFLOW PT:\n')
maxi = len(max(users, key=len)) # O maior nome que temos para que se formate a tabela de acordo
text = '{: <4} | {: <{}} | {} | {} | {} | {} \n'.format('RANK', 'USER', maxi, 'GOLD', 'PLATE', 'BRONZE', 'SCORE') # table head
row_separator = '-'*len(text)
text += '{}\n'.format(row_separator)
for k, v in enumerate(sorted(data, key=lambda user_score: user_score[1], reverse=True), 1): # ordenar pelos pontos
    user, score, badges = v    
    text += '{: <4} | {: <{}} | {: <4} | {: <5} | {: <6} | {}\n{}\n'.format(k, user, maxi, badges[0], badges[1], badges[2], score, row_separator)
print(text)
print('Parabéns ao {}, o utilizador com mais reputação do SOEN\n'.format(users[0]))
