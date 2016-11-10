from __future__ import division

import codecs
import os
import re

from nltk.tag import StanfordNERTagger as nerTagger
from nltk.tokenize import sent_tokenize as st
from nltk.tokenize import word_tokenize as wt


jar = '../stanford-ner-2015-12-09/stanford-ner.jar'
model = '../stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz'
ner = nerTagger(model, jar)

raw_text_path = '../data/AA'
output_path = '../data/AA_tag'


def pre_process():
    filenames = os.listdir(raw_text_path)

    for f in filenames:
        with open(os.path.join(raw_text_path, f), 'r') as doc:
            texts = re.split('</?doc.*>\n+', doc.read())

            for page in texts:
                if page == '':
                    continue
                paragraphs = re.split('\n+', page)
                title = paragraphs[0]
                doc_path = os.path.join(output_path, title)

                if not os.path.exists(doc_path):
                    os.makedirs(doc_path)

                print "processing %s" % title

                for i in range(1, len(paragraphs)):
                    out = os.path.join(doc_path, "%d.txt" % i)
                    if os.path.exists(out):
                        continue
                    writer = codecs.open(out, 'w', 'utf-8')
                    sentences = st(paragraphs[i].decode('utf-8'))

                    for s in sentences:
                        tags = ner.tag(wt(s))

                        for t in tags:
                            writer.write('%s\t%s\n' % (t[0], t[1]))

                        writer.write('\n')

                    writer.flush()
                    writer.close()

if __name__ == '__main__':
    pre_process()
