from urllib.parse import urlparse
from googlesearch import search
import util
import pandas as pd
import file_utils
import logging
import time

ERROR_TOLERANCE = 10
SAVE_FREQUENCY = 100 #How many entries to crawl before incremental save

def get_url(query):
    """For a given query, retrieves Google Search result corresponding to result_index
    
        Returns: A single url
    
    """
    result = search(query, num_results=1)[0]
    time.sleep(2)
    return result


def get_domain(query, index, bad_queries):
    """Given a query, returns the domain of the first Google search result

    Tracks number of bad queries in a row for fault tolerance purposes.
    """
    #get_urls with num = 1 returns a list 1 link, we so use [0] to get the link
    try:
        link = get_url(query)
        domain = urlparse(link)[1]
        if 'www' in domain:
            domain = domain[4:]
        logging.info("{} Query: {} | Domain: {}".format(index, query, domain))
    except:
        logging.error("BAD QUERY: " + query)
        bad_queries += 1
        return bad_queries, "BADQUERY"
    bad_queries = 0
    return bad_queries, domain


def bad_queries_fail(df, output_file, i, bad_queries):
    """Prompts user on how to respond to a failed query

    """
    #TODO: Reimplement with new saving strategy
    proceed = util.get_yes_no(f'Crawler encountered {bad_queries} bad queries in a row. Proceed?')
    if proceed:
        return
    else:
        df.to_csv(output_file)
        logging.fatal(f'Program exited due to crawler encountering {bad_queries} bad queries in a row')
        exit() 

def get_name_address(df, i):
    """Given the index i of dataframe df, extracts the name and address

    """
    name = df.iloc[i,0]
    address = ""
    for j in range(2,5):
        frag = str(df.iloc[i,j])
        if frag != "nan":
            address = address + frag + ' '
    return name, address

def crawl(df, output_file):
    """Crawls the dataframe and generates domains from names and addresses.
    
    Given a dataframe df and output_file
    crawls the dataframe and generates domains from names and addresses.
    Incrementally saves progress and has fault tolerance for Google blocking
    or TODO internet disconnecting.
    """
    bad_queries = 0
    num_rows = df.shape[0]
    domain_index = list(df.columns).index('domain')
    for i in range(num_rows):
        name, address = get_name_address(df, i)
        bad_queries, domain = get_domain(name + ' ' + address, i, bad_queries)
        df.iat[i, domain_index] = domain
        if bad_queries >= ERROR_TOLERANCE:
            bad_queries_fail(df, output_file, i, bad_queries)
        if i%SAVE_FREQUENCY == 0:
            file_utils.incremental_save(df, output_file, i)
    return df