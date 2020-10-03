# Imported the module for the testing
import speedtest

st = speedtest.Speedtest()

'''
I got the download speed (in bytes thats why it divided by 1000) and made it into kb wih 2 decimal places
I got the upload speed (in bytes thats why it divided by 1000) and made it into kb wih 2 decimal places
'''

download = round(st.download() / 1000,2)
upload = round(st.upload() / 1000,2)

print("Your internet speeds are: ")
print(f"Download: {download} kb/s")
print(f"Upload: {upload} kb/s")