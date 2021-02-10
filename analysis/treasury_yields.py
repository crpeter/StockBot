import requests
import bs4

class treasury_yields():

  URL = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%202%20and%20year(NEW_DATE)%20eq%202021'
  URL = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%202021'

  def get_yields(self):
    r = requests.get(self.URL)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    yield_entry = soup.find_all('entry')

    for e in yield_entry:
      e_split = str(e.get_text()).split('.')
      
      date_data = e_split[3]
      date = date_data.split(':')[2][-13:-3]
      
      yield_data = e_split[4:-1]
      fixed_yield_data = self.format_numeric_data(yield_data)

      inversion = self.check_inversion(fixed_yield_data)
      
      print('date: ' + date)
      print('original: ' + str(yield_data))
      print(str(inversion) + ': ' + str(fixed_yield_data))
      print('\n')
  ## END get_yields

  def format_numeric_data(self, data):
    fixed_data = []
    for i in range(len(data)):
      if i == 8:
        continue
      e = data[i]
      number_split = e.split('\n')

      decimal = float('0.' + number_split[0])

      e = str(int(number_split[1]) + decimal)[0:6]
      fixed_data.append(e)

    return fixed_data
  ## END format_numeric_data

  def check_inversion(self, data):
    inversion = False
    for i in range(len(data) - 1):
      if float(data[i]) > float(data[i+1]):
        inversion = True
    return inversion
  ## END check_inversion