__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from Bio import Entrez
import pandas as pd


def search(query):
    Entrez.email = 'diegompin@gmail.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'diegompin@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


if __name__ == '__main__':
    results = search('"Catchment Area (Health)"[mesh] AND "heart failure"[mesh]')
    id_list = results['IdList']
    papers = fetch_details(id_list)

    df = pd.DataFrame()

    list_articles = []
    for id,  paper in zip(id_list, papers['PubmedArticle']):
        curated_article = dict()
        curated_article['PMID'] = id
        citation = paper['MedlineCitation']
        article = citation['Article']
        curated_article['TITLE'] = article['ArticleTitle']
        abstract = 'NONE'
        if 'Abstract' in article:
            abstract = ' '.join(article['Abstract']['AbstractText'])
        curated_article['ABSTRACT'] = abstract
        date = 'NONE'
        if 'PubDate' in article['Journal']['JournalIssue']:
            date = article['Journal']['JournalIssue']['PubDate']
            if 'Year' in date:
                date = date['Year']
            elif 'MedlineDate' in date:
                date = date['MedlineDate'].split(' ')[0]
        curated_article['DATE'] = date
        journal = 'NONE'
        if 'Title' in article['Journal']:
            journal = article['Journal']['Title']
        curated_article['JOURNAL'] = journal
        # authors = 'NONE'
        authors = ', '.join([f'{i["LastName"]} i["Initials"]' for i in article['AuthorList']])
        curated_article['AUTHORS'] = authors

        list_articles.append(curated_article)
    df = pd.DataFrame(list_articles)
    # df.columns = ['PMID', 'TITLE', 'ABSTRACT']
    df.to_csv('articles.csv')
        # line = f'{id}, {title}, {abstract}'
        # print(line)
        # print("%d) %s" % (i + 1, paper['MedlineCitation']['Article'].keys()['MedlineCitation']['Article']['ArticleTitle']))
    # Pretty print the first paper in full to observe its structure
    # import json
    # print(json.dumps(papers[0], indent=2, separators=(',', ':')))
