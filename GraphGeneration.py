import os
import json

ORG_TAG = 'ORGANIZATION'
PER_TAG = 'PERSON'


def graph_generate(data_path='../data'):
    org_path = os.path.join(data_path, 'org')
    per_path = os.path.join(data_path, 'per')
    per_org_dict = {}
    org_per_dict = {}

    for (path, label) in [(org_path, ORG_TAG), (per_path, PER_TAG)]:
        for title in os.listdir(path):
            if label == PER_TAG and title not in per_org_dict:
                per_org_dict[title] = set()
            elif label == ORG_TAG and title not in org_per_dict:
                org_per_dict[title] = set()
            for f in os.listdir(os.path.join(path, title)):
                with open(os.path.join(path, title, f), 'r') as doc:
                    sentences = doc.read().split('\n\n')
                    for s in sentences:
                        if s == '':
                            continue
                        tokens = [(t.split()[0], t.split()[1]) for t in s.split('\n') if len(t.split()) == 2]
                        orgs = set()
                        pers = set()
                        i = 0
                        while i < len(tokens):
                            if tokens[i][1] == PER_TAG:
                                j = 1
                                per = tokens[i][0]
                                while i + j + 1 < len(tokens) and tokens[i + j][1] == PER_TAG:
                                    per += ' ' + tokens[i + j][0]
                                    j += 1
                                if " " in per:
                                    pers.add(per)
                                i += j
                            elif tokens[i][1] == ORG_TAG:
                                j = 1
                                org = tokens[i][0]
                                while i + j + 1 < len(tokens) and tokens[i + j][1] == ORG_TAG:
                                    org += ' ' + tokens[i + j][0]
                                    j += 1
                                if " " in org:
                                    orgs.add(org)
                                i += j
                            i += 1
                        if len(orgs) != 0 and len(pers) != 0:
                            if label == ORG_TAG:
                                orgs.add(title)
                            elif label == PER_TAG:
                                pers.add(title)
                            for per in pers:
                                if per not in per_org_dict:
                                    per_org_dict[per] = set()
                                for org in orgs:
                                    if org not in org_per_dict:
                                        org_per_dict[org] = set()
                                    per_org_dict[per].add(org)
                                    org_per_dict[org].add(per)
                        elif len(orgs) != 0 and label == PER_TAG:
                            for org in orgs:
                                if org not in org_per_dict:
                                    org_per_dict[org] = set()
                                per_org_dict[title].add(org)
                                org_per_dict[org].add(title)
                        elif len(pers) != 0 and label == ORG_TAG:
                            for per in pers:
                                if per not in per_org_dict:
                                    per_org_dict[per] = set()
                                per_org_dict[per].add(title)
                                org_per_dict[title].add(per)
    return per_org_dict, org_per_dict


# helper function to decode json unicode object to string
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

if __name__ == '__main__':
    # generate per_org_dict
    per_org, org_per = graph_generate()

    per_org_writer = open('../data/per_org_dict.json', 'w')
    org_per_writer = open('../data/org_per_dict.json', 'w')

    for (k, v) in per_org.items():
        per_org[k] = list(v)
    for (k, v) in org_per.items():
        org_per[k] = list(v)

    per_org_writer.write(json.dumps(per_org))
    per_org_writer.flush()
    per_org_writer.close()

    org_per_writer.write(json.dumps(org_per))
    org_per_writer.flush()
    org_per_writer.close()

    # load per_org_dict
    """
    per_org = json.loads(open('../data/per_org_dict.json', 'r').read(), object_hook=byteify)
    for (k, v) in per_org.items():
        per_org[k] = set(v)
    org_per = json.loads(open('../data/org_per_dict.json', 'r').read(), object_hook=byteify)
    for (k, v) in org_per.items():
        org_per[k] = set(v)
    """
