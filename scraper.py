from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime


class MoneyControlScraper:
    def __init__(self):
        self.url = 'https://www.moneycontrol.com'
        r = requests.get(self.url)
        html_content = r.content
        self.content = bs(html_content,'html.parser')


    def scrap_bonds(self):
        '''Scrapes Bonds and their current price for today.'''

        bxcom_class = self.content.find_all('div',class_ = "bxcom")[2]

        bonds_lst = bxcom_class.get_text().split('\n')
        bonds_str = ' '.join(bonds_lst)[:-27]
        bonds_lst = bonds_str.split('  ')[1:]
        bonds_lst.pop(0)
        bonds_lst.pop(1)
        for i in range(1,5):
            bonds_lst[i] = bonds_lst[i][1:]

        return bonds_lst
    
    def scrap_commodities(self):
        '''Scrapes Commodities and their current prices for today.'''
        bxcom_class = self.content.find_all('div',class_ = "bxcom")[0]

        commodity_lst = bxcom_class.get_text().split('\n')
        for i in commodity_lst:
            if i == '':
                commodity_lst.pop(commodity_lst.index(i))
            if i == '\xa0':
                commodity_lst.pop(commodity_lst.index(i)) 
        commodity_lst = commodity_lst[5:25]
        x = 4
        while x<=16:
            commodity_lst[x] = commodity_lst[x][28:]
            x+=4
        a = 0
        fin_lst = []
        for j in range(5):
            a+=4
            if a==20:
                fin_lst.append(commodity_lst[j*4:])
                break
            fin_lst.append(commodity_lst[j*4:a])
        return fin_lst
    
    def scrap_currencies(self):
        '''Scrapes Currencies and their current prices for today.'''

        bxcom_class = self.content.find_all('div',class_ = "bxcom")[1]

        currency_str = bxcom_class.table.get_text()
        currency_lst = currency_str.split('\n')

        currency_str = ' '.join(currency_lst)

        currency_lst = currency_str.split('                                 ')
        currency_lst[0] = currency_lst[0][3:]
        currency_lst[len(currency_lst)-1] = currency_lst[len(currency_lst)-1][:-3]
        
        return currency_lst

    def scrap_MostActiveCompanies(self):
        '''Scrapes the Most Active Companies and their current prices for today.'''
        
        most_active_companies = self.content.find('div',id = 'in_maNSE')
        company_str = most_active_companies.table.get_text()

        company_lst = company_str.split('\n')
        company_str = ' '.join(company_lst)
        company_str = company_str[72:-3]
        final_lst = company_str.split('    ')
        final_lst = [x.split('  ') for x in final_lst]
        return final_lst
    
    def scrape_TopGainers(self):
        '''Scrapes Top Gainers and their current prices for today.'''

        columns = ['Company','Price','Change','%Gain']

        top_gainers = self.content.find('div',id="in_tgNifty")

        top_gainers_text = top_gainers.table.get_text()

        top_gainers_text = top_gainers_text.replace('\n'," ")

        top_gainers_text = top_gainers_text[60:]

        tgtl = top_gainers_text.split('   ')
        top_gainers_list = [x.split('  ') for x in tgtl]

        top_gainers_list.pop(5)
        top_gainers_list.insert(0,columns)
        return top_gainers_list
    
    def scrape_TopLosers(self):
        '''Scrapes Top Losers and their current prices for today.'''

        columns = ['Company','Price','Change','%Gain']
        losers = self.content.find('div',id="in_tlNifty")

        losers_text = losers.table.get_text()
        losers_text = losers_text.replace('\n'," ")
        losers_text = losers_text[60:]
        tgtl = losers_text.split('   ')
        losers_list = [x.split('  ') for x in tgtl]
        losers_list.pop(5)
        
        losers_list.insert(0,columns)
        return losers_list
    
    def scrape_GlobalMarkets(self):
        '''Scrapes Global Markets and their current prices for today.'''


        columns = ['Indices Price Change% Chg']
        global_markets = self.content.find_all('table',class_ ="rhsglTbl")[2]

        g_market_str = global_markets.get_text()

        g_market_lst = g_market_str.split('\n')
        g_market_str = ' '.join(g_market_lst)
        final_lst = g_market_str.split('    ')
        final_lst = [x.split('  ') for x in final_lst]
        final_lst[-1].pop(2)
        final_lst[0] = columns

        return final_lst
    
    def show_most_read(self):
        '''Prints most read headlines from the website.'''

        news = self.content.find_all('div',id = 'keynwstb1')[0]
        lis = news.find_all('li')

        news_text = []
        for i in lis:
            try:
                news_text.append(' '.join(i.a.get_text()))
            except:
                news_text.append('None')

        for i in news_text:
            if i == 'None':
                news_text.pop(news_text.index(i))

        print(''.join(news_text))

    def get_news_hindi(self):
        '''
        Prints news headlines in Hindi language
        '''

        hindi_news = self.content.find('div',id="keynwstb4")
        news_lst = []

        for i in hindi_news.find_all('li'):
            news_lst.append(i.get_text())

        for i in  news_lst:
            print(i)

    
    def write_to_file(self):

        gainers = self.scrape_TopGainers()
        losers = self.scrape_TopLosers()
        commodities = self.scrap_commodities()
        currencies = self.scrap_currencies()
        global_markets = self.scrape_GlobalMarkets
        bonds = self.scrap_bonds()
        active_companies = self.scrap_MostActiveCompanies()
        
        with open('moneycontrolscraper.txt','w') as f:
            f.write(str(datetime.datetime.now())+" ")
            f.write(str({'gainers':gainers,'losers':losers,'commodities':commodities,'currencies':currencies,'global_markets':global_markets,'bonds':bonds,'MostActiveCompanies':active_companies}))
            f.close()


