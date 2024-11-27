import requests
import xml.etree.ElementTree as ET
import sys
import csv
import logging


#parent ref arg 1
# refs to move.refs arg 2

logging.basicConfig(
    level=logging.ERROR,
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('errors.log', mode='a')
    ]
)


if len(sys.argv) != 3: 
    logging.error('usage: python3 accessAPI.py <parent-ref> <ref-file>')
    sys.exit(1)


parent_ref = sys.argv[1]
collection_refs = sys.argv[2]


url = "https://pitt.preservica.com/api/accesstoken/login"
data = {
    "username": "replace with username",
    "password": "replace with password",
    "tenant": "pitt"
}


response = requests.post(url, data=data)

if response.status_code == 200: json_response = response.json() 
else: 
    err_msg = f"login failed with status code {response.status_code}"
    logging.error(err_msg)
    sys.exit(1)


access_token = json_response['token']

# SO_id = 'a18e4ca8-0ea9-4923-a8cc-92f00f437fcd'
# count = 0
# max_items = 500
#endpoint_url = f"https://pitt.preservica.com/api/entity/structural-objects/{SO_id}/children?ref={SO_id}&start={count}&max={max_items}"


# structural object = folders
# information object = assets

# ref = '7f026b8c-8e8a-43c6-9f99-e66adac826f0'
# move_info_url = f"https://pitt.preservica.com/api/entity/information-objects/{ref}/parent-ref"
# move_struct_url = f"https://pitt.preservica.com/api/entity/structural-objects/{SO_id}/parent-ref"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "text/plain",
}

#z_trash folder
# newParentRef = 'a1b1a897-60df-4ebf-88df-6020554a48e8'

# ref_csv = 'refs-to-move.csv'


#open file and begin
with open(collection_refs, 'r') as file:
    for line in file:
        ref = line.strip()
        move_url = f"https://pitt.preservica.com/api/entity/information-objects/{ref}/parent-ref"
        response = requests.put(move_url, headers=headers, data=parent_ref)
        if response.status_code in {403,404,422} or response.status_code != 202: 
            err_msg = f"{ref} trouble moving with status code {response.status_code}"
            logging.error(err_msg)
        else: print(f"successfully started {ref} move to {parent_ref}")


# -------------------------------------------------------------------------------------------------------------------------- #

# response = requests.put(move_info_url, headers=headers, data='a18e4ca8-0ea9-4923-a8cc-92f00f437fcd')
# if response.status_code == 202: print(f"information object parent: {response.text}")
# else: print(f"error getting information object to another parent: {response.status_code}")

# response = requests.get(move_struct_url, headers=headers)
# if response.status_code == 200: print(f"structural object parents: {response.text}")
# else: print(f"error moving structural object parent: {response.status_code}")



# while True:
#     endpoint_url = f"https://pitt.preservica.com/api/entity/structural-objects/{SO_id}/children?ref={SO_id}&start={count}&max={max_items}"
#     print("endpoint url: " + endpoint_url)

#     headers = {
#     "Authorization": f"Bearer {access_token}",
#     }

#     response = requests.get(endpoint_url, headers=headers)

#     if response.status_code == 200:
#         print("Response Content-Type:", response.headers.get('Content-Type'))
#         try:
#             root = ET.fromstring(response.text)

#             ns = { 'default': 'http://preservica.com/EntityAPI/v7.4'}

#             print("parsed xml response: ")
            
#             for children in root.findall('default:Children', ns):
#                 with open('child_ref.csv', 'a', newline='') as file:
#                     for Child in children.findall('default:Child', ns):
#                         child_ref = Child.get('ref')
#                         child_title = Child.get('title')
#                         print(f"title: {child_title}")
#                         writer = csv.writer(file)
#                         writer.writerow([child_title, child_ref])
                        
#             print(f"count: {count}")
#             next_url = root.find('default:Paging//default:Next', ns)
#             if next_url is None:
#                 print("all data fetched")
#                 break
#             else:
#                 count += max_items
#                 print(f"fetching from {count} now")
#         except ET.ParseError as e:
#             print("error parsing xml - raw response: " + response.text)
#             break
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         break