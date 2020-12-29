from bs4 import BeautifulSoup as BS
import csv
import math
import re
import pprint
import os.path
from Browser import Browser
import time

pp = pprint.PrettyPrinter(indent=4)

def read_bookid_csv(fn):
    bookid_list = []
    with open(fn, newline='', encoding='utf-8-sig') as csvfile:
        bookid_reader = csv.reader(csvfile, delimiter=',')
        for row in bookid_reader:
            bookid_list.append(row[0])
    return bookid_list

def read_reviews(file):

    bookids = read_bookid_csv(file)
    products = []
    browser = Browser()

    if len(bookids) > 0:
        for bookid in bookids:
            review_dict = {bookid: {'reviewer': [], 'review_timestamp': [], 'rating': [], 'review_text': [], 'review_link': [], }}

            base_url = 'https://www.goodreads.com'
            url = base_url + '/book/show/' + bookid

            browser.get(url)
            source = browser.page_source
            soup = BS(source, 'lxml') # soup = soup.encode('utf-8')

            total_reviews = int(soup.find('meta', {'itemprop': 'reviewCount'}).attrs['content'])
            page_count = int(math.ceil(total_reviews/30))

            # grab the title
            if soup.find('h1', {'id': 'bookTitle'}, {'class': 'gr-h1 gr-h1--serif'}):
                product_title = soup.find('h1', {'id': 'bookTitle'}, {'class': 'gr-h1 gr-h1--serif'})
                if product_title.text:
                    product_title = str(product_title.text.replace('\n',''))
                else:
                    product_title = 'No title found'
            else:
                product_title = 'No title found'
                        
            # Start grabing page by page
            if page_count > 0:
                print(f'Page count: {str(page_count)}')
                last_page_source = ''

                for i in range(page_count):

                    page_changed = False
                    attempts = 0
                    while(not page_changed):
                        if last_page_source != browser.page_source:
                            page_changed = True
                        else:
                            if attempts > 5: # Decide on some point when you want to give up.
                                break
                            else:
                                time.sleep(3) # Give time to load new page. Interval could be shorter.
                                attempts += 1

                    page = i + 1
                    page = str(page)
                    print(f'Fetching page {page}')
                    
                    paged_soup = BS(browser.page_source, 'lxml')

                    # review_info
                    review_info = paged_soup.find_all('div',{'class': 'friendReviews elementListBrown'})

                    for r in review_info:

                        # review_timestamp
                        rt = r.find_all('a', {'class': 'reviewDate createdAt right'}, href = True)[0]
                        review_dict[bookid]['review_timestamp'].append(rt.text)

                        # review_link
                        review_dict[bookid]['review_link'].append(base_url + '%s' % rt['href'])

                        # reviewer
                        reviewer = r.find_all('span',{'itemprop': 'author'},{'itemscope itemtype': 'http://schema.org/Person'})[0].text
                        review_dict[bookid]['reviewer'].append(reviewer.replace('\n',''))

                        # rating
                        try:
                            rating = r.find_all('span', {'class': 'staticStars notranslate'}, title = True)[0].text
                        except IndexError:
                            rating = None
                        review_dict[bookid]['rating'].append(rating)
                        
                        # review_text
                        review_text = r.find_all('div', {'class': "reviewText stacked"})[0].text
                        review_dict[bookid]['review_text'].append(review_text.replace('\U0001f44d', '').replace('\U0001f4a9', '')) 
                    
                    last_page_source = browser.page_source
                    browser.goto_next_page()

            data_tuples = []
            for rr in range(len(review_dict[bookid]['reviewer'])):
                data_tuples.append((review_dict[bookid]['reviewer'][rr], review_dict[bookid]['review_timestamp'][rr],
                                    review_dict[bookid]['rating'][rr], review_dict[bookid]['review_text'][rr], review_dict[bookid]['review_link'][rr]))

            products.append({'bookid': bookid, 'title': product_title, 'data': data_tuples})

        browser.close()
        # should return an object with all info here (or write out to csv)
        return products

