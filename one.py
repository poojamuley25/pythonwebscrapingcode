from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from matplotlib import pyplot as plt
from csv import writer
from os import path

all_codes = ["6007","6270","6160","6004","6794","6755","6276","6278","2020","2127","2131","2132","3148","3190","3194",
             "6156","6759","2130","2133","1120","1125","3189"]
data = []
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.strip()
  return cleantext

def savedata():
  if(path.exists('college_info.csv')):
    df = pd.DataFrame(data)
    df = df[df.isnull().sum(axis=1) < 5]
    df.to_csv("college_info.csv", mode='a', header=False)
  else:
    df = pd.DataFrame(data, columns=['code', 'College Name', 'Address', 'Email', 'District', 'Principal Name',
                                   'Office Number', 'Personal Number', 'Register Number', 'Website'])
    df = df[df.isnull().sum(axis=1) < 5]
    df.to_csv("college_info.csv",index=False)

def visualize():
  df = pd.read_csv('college_info.csv')
  unique_regions = list(set(df['District']))
  region_count = []
  for i in unique_regions:
    region_count.append(list(df['District']).count(i))
  plt.bar(unique_regions, region_count)
  plt.xlabel('regions')
  plt.ylabel('No of clg per region')
  plt.show()

for code in range(3000,3200):
  url = f"http://dtemaharashtra.gov.in/frmInstituteSummary.aspx?InstituteCode={code}"
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  clg_name_id = "ctl00_ContentPlaceHolder1_lblInstituteNameEnglish"
  clg_address_id = "ctl00_ContentPlaceHolder1_lblAddressEnglish"
  email_address_id = "ctl00_ContentPlaceHolder1_lblEMailAddress"
  District_id = "ctl00_ContentPlaceHolder1_lblDistrict"
  principal_id = "ctl00_ContentPlaceHolder1_lblPrincipalNameEnglish"
  Office_no = "ctl00_ContentPlaceHolder1_lblOfficePhoneNo"
  personal_id = "ctl00_ContentPlaceHolder1_lblPersonalPhoneNo"
  register_id = "ctl00_ContentPlaceHolder1_lblRegistrarNameEnglish"
  website_link_id = "ctl00_ContentPlaceHolder1_lblWebAddress"

  clg_name = cleanhtml((soup.find(id=clg_name_id)).prettify())
  clg_address = cleanhtml((soup.find(id=clg_address_id)).prettify())
  email_address = cleanhtml((soup.find(id=email_address_id)).prettify())
  District = cleanhtml((soup.find(id=District_id)).prettify())
  principal_name = cleanhtml((soup.find(id=principal_id)).prettify())
  Office_no = cleanhtml((soup.find(id=Office_no)).prettify())
  personal_no = cleanhtml((soup.find(id=personal_id)).prettify())
  register_name = cleanhtml((soup.find(id=register_id)).prettify())
  website_link = cleanhtml((soup.find(id=website_link_id)).prettify())

  data.append([code, clg_name, clg_address, email_address, District, principal_name, Office_no, personal_no,
               register_name, website_link ])
savedata()
visualize()







