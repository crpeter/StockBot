"""
stockbot.py
Author: Ross Kromminga
----------------------


Instructions:

$quote [TICKER] - Returns current stock price
$bestworst - Returns best and worst performing stock of the day
$trump - Returns random Trump quote
$what is it - Too easy
$summary [TICKER] - Returns variety of different attributes
$market cap [TICKER] - Returns current market cap of stock
$dad joke - Returns a random dad joke
"""

import discord
import requests
import bs4
from datetime import date, datetime
import json
import time


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        msg = message.content.lower()

        if msg == '$what is it':
            print(f'{message.author} - {datetime.now()} - WhatIsIt request')
            await message.channel.send('Too easy')

        if msg.startswith('$quote'):
            # Scraping current stock price from Yahoo Finance
            ticker = msg.split("$quote ", 1)[1].upper()
            URL = str(f'https://finance.yahoo.com/quote/{ticker}')
            r = requests.get(URL)
            soup = bs4.BeautifulSoup(r.text, "lxml")
            try:
                price = soup.find_all('div',{'class':'D(ib) Va(m) Maw(65%) Ov(h)'})[0].find_all('span')[0].text
            except:
                await message.channel.send("Couldn't find ticker")
                print(f"{message.author} - {datetime.now()} - Quote request - ERROR: Couldn't find ticker")
                return
            company_name = soup.find_all('div',{'class':'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
            change = soup.find_all('div',{'class':'D(ib) Va(m) Maw(65%) Ov(h)'})[0].find_all('span')[1].text
            print(f'{message.author} - {datetime.now()} - Quote request - ({company_name})')
            await message.channel.send(f'{company_name}  |  ${price}  |  {change}')

        if msg.startswith('$market cap'):
            ticker = msg.split("$market cap ", 1)[1].upper()
            url = "https://seeking-alpha.p.rapidapi.com/symbols/get-valuation"

            querystring = {"symbols": ticker}

            headers = {
                'x-rapidapi-key': "9d87e7f66fmsh4811e031be17560p160537jsn8c2bab09d381",
                'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            databack = response.json()
            marketCap = databack['data'][0]['attributes']['marketCap']
            formated_float = "${:,.2f}".format(marketCap)
            print(f'{message.author} - {datetime.now()} - MarketCap request - ({ticker})')
            await message.channel.send(f'{ticker}  |  Market Cap: {formated_float}')

        if msg.startswith('$summary'):
            ticker = msg.split("$summary ", 1)[1].upper()

            url = "https://seeking-alpha.p.rapidapi.com/symbols/get-summary"

            querystring = {"symbols": ticker}

            headers = {
                'x-rapidapi-key': "9d87e7f66fmsh4811e031be17560p160537jsn8c2bab09d381",
                'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            databack = response.json()
            yearHigh = databack['data'][0]['attributes']['high52']
            yearLow = databack['data'][0]['attributes']['low52']
            priceEarnings = databack['data'][0]['attributes']['lastClosePriceEarningsRatio']
            divRate = databack['data'][0]['attributes']['divRate']
            divYield = databack['data'][0]['attributes']['divYield']
            marketCap = databack['data'][0]['attributes']['marketCap']
            formated_float = "${:,.2f}".format(marketCap)
            print(f'{message.author} - {datetime.now()} - Summary request - ({ticker})')
            await message.channel.send(f'{ticker}\nYear High: ${yearHigh}\nYear Low: ${yearLow}\nPrice Earnings Ratio: {priceEarnings}\nDividend Rate: {divRate}\nDividend Yield: {divYield}\nMarket Cap: {formated_float}')


        if msg == '$bestworst':
            # Scraping worst performing stock of the day's info from Yahoo Finance
            URL = str(f'https://finance.yahoo.com/losers/')
            r = requests.get(URL)
            soup = bs4.BeautifulSoup(r.text, "lxml")
            worst_stock = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[0].text
            worst_stock_company = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[1].text
            worst_stock_price = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[2].text
            worst_stock_change = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[3].text
            worst_stock_percentage = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[4].text

            #Scraping best performing stock of the day's info from Yahoo Finance
            URL = 'https://finance.yahoo.com/gainers/'
            r = requests.get(URL)
            soup = bs4.BeautifulSoup(r.text, "lxml")
            best_stock = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[0].text
            best_stock_company = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[1].text
            best_stock_price = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[2].text
            best_stock_change = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[3].text
            best_stock_percentage = soup.find('tbody', {'data-reactid': '72'}).find_all('td')[4].text

            print(f'{message.author} - {datetime.now()} - Best/Worst request')
            await message.channel.send(f'Best performing stock today:   {best_stock} | {best_stock_company} | ${best_stock_price} | {best_stock_change} ({best_stock_percentage})\nWorst performing stock today:   {worst_stock} | {worst_stock_company} | ${worst_stock_price} | {worst_stock_change} ({worst_stock_percentage})')


        if msg.startswith('$trump'):
            # Sends random trump quote in chat
            url = "https://matchilling-tronald-dump-v1.p.rapidapi.com/random/quote"

            headers = {
                'accept': "application/hal+json",
                'x-rapidapi-key': "9d87e7f66fmsh4811e031be17560p160537jsn8c2bab09d381",
                'x-rapidapi-host': "matchilling-tronald-dump-v1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers)

            data = response.json()
            trump_quote = data['value']
            print(f'{message.author} - {datetime.now()} - TrumpQuote request')
            await message.channel.send(trump_quote)

        if msg.startswith('$dad joke'):
            url = "https://dad-jokes.p.rapidapi.com/random/joke"

            headers = {
                'x-rapidapi-key': "9d87e7f66fmsh4811e031be17560p160537jsn8c2bab09d381",
                'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers)

            databack = response.json()
            setup = databack['body'][0]['setup']
            punchline = databack['body'][0]['punchline']
            print(f'{message.author} - {datetime.now()} - DadJoke request')
            await message.channel.send(setup)
            time.sleep(5)
            await message.channel.send(punchline)
            
        if msg.startswith('$wsb'):
            posts = int(msg.split("$wsb ", 1)[1])

            d = enchant.Dict("en_US")

            client_id = 'CLIENT_ID'
            client_secret = 'CLIENT_SECRET'
            user_agent = 'APP_NAME'
            username = 'REDDIT_USER'
            password = 'REDDIT_PASSWORD'

            reddit = praw.Reddit(client_id=client_id,
                                 client_secret=client_secret,
                                 username=username,
                                 password=password,
                                 user_agent=user_agent)

            subreddit = reddit.subreddit('wallstreetbets')

            top_subreddit = subreddit.new(limit=posts)

            words_collection = []
            for submission in top_subreddit:
                title = submission.title
                title_words = title.split()
                words_collection.append(title_words)

            all_tickers = []
            non_ticker = ['PSA','WSB','DIY']
            for i in words_collection:
                for word in i:
                    reword = re.compile('[^a-zA-Z]')
                    word = reword.sub('', word)
                    if word.isupper() and 5 > len(word) > 1 and d.check(word) == False and word not in non_ticker:
                        all_tickers.append(word)
            new_tickers = []
            for i in all_tickers:
                if i not in new_tickers:
                    new_tickers.append(i)
            print(f'{message.author} - {datetime.now()} - WSB Top Posts({posts}) request')
            await message.channel.send(new_tickers) 




if __name__ == '__main__':
    today = date.today()
    today_date = today.strftime("%m/%d/%y")

    client = MyClient()
    client.run('DISCORD_TOKEN')
