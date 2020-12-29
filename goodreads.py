from helpers import read_reviews
import csv
import io

inputFile = "booklist.csv"

data = read_reviews(inputFile)

field_names = ['bookid', 'product_title', 'reviewer', 'review_timestamp', 'rating', 'review_text', 'review_link']

expanded_reviews = []

for product_reviews in data:
    _bookid = product_reviews['bookid']
    _title = product_reviews['title']
    _data = product_reviews['data']

    for _d in _data:
        expanded_reviews.append([_bookid, _title, _d[0], _d[1], _d[2], _d[3], _d[4]])

with io.open('output.csv', 'w', encoding="utf-8-sig", newline='') as dataFile:
    writer = csv.writer(dataFile, delimiter=',')

    writer.writerow(field_names)
    for e in expanded_reviews:
        writer.writerow(e)

    print(f'Output written to "output.csv"')




