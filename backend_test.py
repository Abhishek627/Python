import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope= [ 'https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('backend_secret.json',scope)
client= gspread.authorize(creds)

sheet = client.open("RPC").sheet1
rpc =sheet.get_all_records()
print rpc