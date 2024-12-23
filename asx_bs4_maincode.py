""" 
Developer Name: MARUTHACHALAM S
Project Title: Australian Stock Exchange Company Announcements
Date: 23.12.2024
Version 1

 """ 



from bs4 import BeautifulSoup
import requests
import re

output_sheet = "Sl.No\tASX Code\tDate\tHeadline\tPDF URL\tStatus\n"
with open("Output_Sheet.txt", 'w') as SM:
    SM.write(output_sheet)

with open("Cookie.txt", 'r') as SM:
    cookie_data = SM.read()

search_date = input("Enter Search Date: ")
month = input("Enter Search Month: ")
year = input("Enter Search Year: ")

# Construct the URL: https://www.asx.com.au/asx/v2/statistics/announcements.do?by=asxCode&asxCode=&timeframe=R&dateReleased=20%2F12%2F2024
 
main_url = f"https://www.asx.com.au/asx/v2/statistics/announcements.do?by=asxCode&asxCode=&timeframe=R&dateReleased={search_date}%2F{month}%2F{year}"

headers = {
    "authority": "www.asx.com.au",
    "method": "GET",
    "path": f"/asx/v2/statistics/announcements.do?by=asxCode&asxCode=&timeframe=R&dateReleased={search_date}%2F{month}%2F{year}",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "cookie": str(cookie_data),
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

response = requests.get(main_url, headers=headers)
content = response.text

with open("Content.html", 'w', encoding="utf-8") as SM:
    SM.write(content)

soup = BeautifulSoup(content, 'html.parser')

blocks = soup.find_all('tr', class_=re.compile(r'(altrow|\s*)'))

si_no = 0
esi_no = 0
total_pdf_count = len(blocks)

def clean_filename(filename): return re.sub(r'[\\/*?:"<>|]', "", filename).replace("\n", " ").strip()

for block in blocks:
    si_no += 1
    try:
        asx_code = block.find_all('td')[0].text.strip()
        date = block.find_all('td')[1].text.strip()
        headline = block.find('a').text.strip()
        if headline:
            headline = re.sub('\n',' ',str(headline))
            headline = re.sub('\s+',' ',str(headline))
        pdf_link = block.find('a')['href']
        
        if pdf_link:
            pdf_link = re.sub('&amp;', '&', pdf_link)
            pdf_link_full = "https://www.asx.com.au" + pdf_link

       
        pdf_headers = {
            "authority": "www.asx.com.au",
            "method": "GET",
            "path": pdf_link,
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cookie": str(cookie_data),
            "priority": "u=0, i",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        pdf_resp = requests.get(pdf_link_full, headers=pdf_headers)
        pdf_resp_code = pdf_resp.status_code
        
        if pdf_resp_code == 200:
            file_name = f"{si_no}_{clean_filename(headline)}.pdf"
            with open(file_name, 'wb') as SM:
                SM.write(pdf_resp.content)
            status = "Downloaded"
            print(f"PDF downloaded: {file_name}")
        else:
            esi_no += 1
            status = "Not Downloaded"
            print(f"Failed to download PDF: {pdf_link_full}")

        output_sheet = f"{si_no}\t{asx_code}\t{date}\t{headline}\t{pdf_link_full}\t{status}\n"
        with open("Output_Sheet.txt", 'a', encoding="utf-8") as SM:
            SM.write(output_sheet)
        
    except Exception as e:
        esi_no += 1
        print(f"Error processing block {si_no}: {e}")

print("Total PDF Count:", total_pdf_count)
print("Data Extraction Completed")
