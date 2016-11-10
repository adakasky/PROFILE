import os
import json

ORG_TAG = 'ORGANIZATION'
PER_TAG = 'PERSON'


def graph_generate(data_path='../data'):
    org_path = os.path.join(data_path, 'org')
    per_path = os.path.join(data_path, 'per')
    graph = {}

    for (path, label) in [(org_path, ORG_TAG), (per_path, PER_TAG)]:
        for title in os.listdir(path):
            if label == PER_TAG and title not in graph:
                graph[title] = set()
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
                                pers.add(per)
                                i += j
                            elif tokens[i][1] == ORG_TAG:
                                j = 1
                                org = tokens[i][0]
                                while i + j + 1 < len(tokens) and tokens[i + j][1] == ORG_TAG:
                                    org += ' ' + tokens[i + j][0]
                                    j += 1
                                orgs.add(org)
                                i += j
                            i += 1
                        if len(orgs) != 0 and len(pers) != 0:
                            if label == ORG_TAG:
                                orgs.add(title)
                            elif label == PER_TAG:
                                pers.add(title)
                            for per in pers:
                                if per not in graph:
                                    graph[per] = set()
                                for org in orgs:
                                    graph[per].add(org)
                        elif len(orgs) != 0 and label == PER_TAG:
                            for org in orgs:
                                graph[title].add(org)
                        elif len(pers) != 0 and label == ORG_TAG:
                            for per in pers:
                                if per not in graph:
                                    graph[per] = set()
                                graph[per].add(title)
    return graph


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
    # generate graph
    G = graph_generate()

    writer = open('../data/graph.json', 'w')
    for (k, v) in G.items():
        G[k] = list(v)
    writer.write(json.dumps(G))
    writer.flush()
    writer.close()

    # load graph
    """
    G = json.loads(open('../data/graph.json', 'r').read(), object_hook=byteify)
    for (k, v) in G.items():
        G[k] = set(v)
    """
