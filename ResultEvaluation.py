import codecs

from BeautifulSoup import BeautifulSoup as bs
import requests
import unicodedata
import time

url = 'https://www.google.com/search?q='


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


if __name__ == '__main__':
    pairs = [(p.split('\t')[0], p.split('\t')[1]) for p in
             codecs.open('../data/pairs.tsv', 'r', 'utf-8').read().split('\n') if p != '']
    writer = codecs.open('../data/pairs_eval.tsv', 'w', 'utf-8')

    for pair in pairs:
        per = strip_accents(pair[0])
        org = strip_accents(pair[1])
        query = url + '%22' + per.replace(' ', '+') + '%22+%22"' + org.replace(' ', '+') + '%22'
        request = requests.get(query)
        html = bs(request.text)

        results = [r.text for r in html.findAll('span', attrs={'class': 'st'})]
        count = 0.0
        for result in results:
            if per in result and org in result:
                count += 1.0
        writer.write("%s\t%s\t%f\n" % (per, org, count / len(results)))
        time.sleep(5)

    writer.flush()
    writer.close()
