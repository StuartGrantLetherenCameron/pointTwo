import math
import requests
from bs4 import BeautifulSoup
import pygsheets
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from building import Building


def main():


    baseUrl = 'https://www.point2homes.com'

    searchUrl = 'https://www.point2homes.com/CA/Real-Estate-Listings.html?location=Ontario&PropertyType=MultiFamily&search_mode=location&ListingDate=yesterday&page=1&SelectedView=listings&LocationGeoId=205411&location_changed=&ajax=1'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    r = requests.get(searchUrl)
    soup = BeautifulSoup(r.content, features="html.parser")

    productList = soup.find_all('div', class_='item-cnt')

    resultsElement = soup.find('div', class_='results-no').text.split()

    numberOfPages = 1


    if len(resultsElement) > 2:
        numberOfPages = math.ceil(int(resultsElement[len(resultsElement) - 2]) / 24.0)

    homeLinks = []


    def find_good_link(evalute):
        if 'https' in evalute:
            return False
        if 'javascript' in evalute:
            return False

        return True


    for item in productList:
        for link in item.find_all('a', href=True):
            if link['href'] not in homeLinks and find_good_link(link['href']):
                homeLinks.append(link['href'])

    building_list = []

    for link in homeLinks:
        r = requests.get(baseUrl + link, headers=headers)

        soup = BeautifulSoup(r.content, features="html.parser")

        address = soup.find('div', class_='address-container').text.strip()

        adress_list = address.split(',')

        address = adress_list[0]

        city = adress_list[1]

        province = adress_list[2]

        price = soup.find('div', class_='price').text.strip()

        property_summery_list = soup.find('div', class_='details-charcs').text.strip().split()

        try:
            building_type = property_summery_list[property_summery_list.index('Building')+2]
        except:
            building_type = "none"

        try:
            year_built = property_summery_list[property_summery_list.index('Built')+1]
        except:
            year_built = 0

        try:
            floors = property_summery_list[property_summery_list.index('Stories')+1]
        except:
            floors = -1

        try:
            postal_code = property_summery_list[property_summery_list.index('Code')+1]
        except:
            postal_code = "ur dads house"
        try:
            mls_number = property_summery_list[property_summery_list.index('Number')+1]
        except:
            mls_number = "Not given"

        try:
            description = soup.find('div', class_='description-text clearfix').text.strip()
        except:
            description = "not given"

        building = Building(price=price, address=address, building_type=building_type, year_built=year_built, floors=floors,
                            postal_code=postal_code, mls_number=mls_number, description=description, city=city, province=province)

        building_list.append(building)

    return building_list


def export():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("BIG_DAYTA/big_dayta").sheet1

    print(sheet)

    dataas = sheet.get_all_records()

    print(dataas)

if __name__ == '__main__':
    #building_list = main()
    export()



