from requests import get
from bs4 import BeautifulSoup
import pandas as pd

#아래부터 찾고 싶은데로 바꿔!
REGION = "원주시--강원도"
CHECKIN = "2023-04-01"
CHECKOUT = "2023-04-02"
FIRST_URL = f'https://www.airbnb.co.kr/s/{REGION}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=1&channel=EXPLORE&date_picker_type=calendar&checkin={CHECKIN}&checkout={CHECKOUT}&source=structured_search_input_header&search_type=search_query&zoom_level=8&adults=3&query=%EA%B2%BD%EC%83%81%EB%B6%81%EB%8F%84&place_id=ChIJvRgZer-kYDURI9xMx5ppVsY&federated_search_session_id=9a8eeae2-35fc-40af-a82a-27180d726ca8&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjowLCJ2ZXJzaW9uIjoxfQ%3D%3D'
URL= ""
data = []

def AirbnbCrawler(url):
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('div', {'class': 'c4mnd7m dir dir-ltr'})
    next_button = soup.find('a',{'class':'l1j9v1wn c1ytbx3a dir dir-ltr'}).get('href')
    next_url = 'https://www.airbnb.co.kr'+ next_button

    for listing in listings:
        name = listing.find('span', {'data-testid': 'listing-card-name'}).text
        price = listing.find('span', {'class': '_14y1gc'}).find('span').text
        url = 'https://www.airbnb.co.kr'+listing.find('a', {'class': 'rfexzly dir dir-ltr'}).get('href')
        data.append([name, price, url])

    return next_url

for i in range(14):
    print(data) #TODO:굉장해 엄청나
    if i == 0 :
        URL = AirbnbCrawler(FIRST_URL)
    else:
        URL = AirbnbCrawler(URL)

df = pd.DataFrame(data, columns=['Name', 'Price','Url'])
df.to_excel('airbnb.xlsx', index=False)
