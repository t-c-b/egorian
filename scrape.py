import pandas
import urllib.request

base_url = r'https://rlee.hosted.uark.edu/midi/'

tables = pandas.read_html(
  base_url,
  extract_links="all"
)

for idx, row in tables[0].iterrows():
  print(row[0], row[1])
  file = row[0][1]
  mode = row[1][0].replace(' ', '')
  urllib.request.urlretrieve(base_url+file, "../chants/"+mode+"/"+file)
