import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
import random
from save_photo import main_photos

CREDENTIALS_FILE = 'avito-xml-333413-1834999ce57d.json'
SHEET_ID = '1tEiFzT8WSnUN6Kc4K_4dOSPOUM5KlR0yt20irtlXl9Q'

def session():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    return service

def create_objects_list(array):
    objects = []

    for ad in array:
        Ad = dict()
        
        if ad[0]:
            Ad['Id'] = ad[0]
            Ad['DateBegin'] = f"{ad[20].split()[0].split('.')[2]}-{ad[20].split()[0].split('.')[1]}-{ad[20].split()[0].split('.')[0]}T{ad[20].split()[1]}:00+03:00"
            Ad['AdStatus'] = "Free"
            Ad['ContactMethod'] = "По телефону и в сообщениях"
            Ad['ManagerName'] = ad[19]
            Ad['ContactPhone'] = ad[18]

            address = f"{ad[12]}, {ad[13]}, {ad[14]}, {ad[15]}, {ad[16]}, {ad[17]}"
            if not ad[13]:
                address = f"{ad[12]}, {ad[14]}, {ad[15]}, {ad[16]}, {ad[17]}"
            if not ad[15]:
                address = f"{ad[12]}, {ad[14]}, {ad[16]}, {ad[17]}"
            if not ad[17]:
                address = f"{ad[12]}, {ad[14]}, {ad[16]}"

            Ad['Address'] = address
            Ad['Category'] = ad[1]
            Ad['GoodsType'] = ad[2]
            Ad['Condition'] = ad[4]
            Ad['AdType'] = ad[3]
            if ad[5]:
                Ad['Apparel'] = ad[5]
            Ad['Title'] = ad[6]
            Ad['Description'] = ad[7]
            Ad['Price'] = ad[8]

            photo_arr = main_photos(ad[9])
            if photo_arr:
                Ad['Images'] = photo_arr
            else:
                continue

            if ad[11]:
                Ad['VideoURL'] = ad[11]

            objects.append(Ad)
    return objects


def main():
    return create_objects_list(session().spreadsheets().values().get(spreadsheetId=SHEET_ID, range="Основная!A2:Y9999").execute()['values'])
    


if __name__ == "__main__":
    array = session().spreadsheets().values().get(spreadsheetId=SHEET_ID, range="Основная!A2:Y9999").execute()['values']
    print(create_objects_list(array))
