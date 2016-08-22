import openpyxl
from TweetFunction import Tweet

data = openpyxl.load_workbook('RawTwitterData.xlsx')
sheet = data.active

for n in range(2,20):                           #change range to include all rows
    Tweet(sheet['P{0}'.format(n)].value, sheet['N{0}'.format(n)].value,
          'https://pbs.twimg.com/profile_images/344513261578483836/0ebebbe0e353d79c61e7225ba9047250.png',
          sheet['B{0}'.format(n)].value, sheet['C{0}'.format(n)].value)
    