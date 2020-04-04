from urllib.parse import urlparse
from googlesearch import search
import util
import pandas as pd
import file_utils

ERROR_TOLERANCE = 10
SAVE_FREQUENCY = 100 #How many entries to crawl before incremental save

def get_urls(query, result_index):
    """For a given query, retrieves Google Search result corresponding to result_index
    
        Returns: A list of one url
    
    """
    results = search(query, tld="com", num=1, start=result_index, stop=result_index+1, pause=2)
    return list(results)


def get_domain(query, index, bad_queries):
    """Given a query, returns the domain of the first Google search result

    Tracks number of bad queries in a row for fault tolerance purposes.
    """
    #get_urls with num = 1 returns a list 1 link, we so use [0] to get the link
    links = []
    link = ''
    try:
        links = get_urls(query, 0)
        link = links[0]
        domain = urlparse(link)[1]
        if 'www' in domain:
            domain = domain[4:]
        print("{} Query: {} | Domain: {}".format(index, query, domain))
    except:
        print("BAD QUERY: " + query)
        bad_queries += 1
        return bad_queries, "BADQUERY"
    bad_queries = 0
    return bad_queries, domain


def bad_queries_fail(df, save_dir, i):
    """Prompts user on how to respond to 

    """
    proceed = util.get_yes_no("Crawler encountered {} bad queries in a row. Proceed?".format(ERROR_TOLERANCE))
    if proceed:
        return
    else:
        file_name = "FAILED_BAD_QUERIES.csv"
        file_utils.save(df, save_dir, file_name)
        print("Exiting...")
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

def crawl(df, output_file, save_dir):
    """Crawls the dataframe and generates domains from names and addresses.
    
    Given a dataframe df and  output_file and save_dir for incremental saves,
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
            bad_queries_fail(df, save_dir, i)
        if i%SAVE_FREQUENCY == 0:
            file_utils.incremental_save(df, save_dir, output_file, i,)
    return df