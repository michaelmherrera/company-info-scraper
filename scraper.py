from urllib.parse import urlparse
from googlesearch import search
import pandas as pd
import os, time, random

file_name = 'dummy.csv' #'texas_firms_roster.csv'
new_file = 'dummy_output.csv' #'texas_firms_roster_with_domain.csv'

#TODO: Remove this once done testing
def delete_old_output(new_file):
    import os
    if os.path.exists(new_file):
        os.remove(new_file)
    else:
        print("The file does not exist")
    temp_name = "INCOMPLETE_" + new_file
    if os.path.exists(temp_name):
        os.remove(temp_name)
    else:
        print("The file does not exist") 

def get_urls(query, result_index):
    results = search(query, tld="com", num=1, start=result_index, stop=result_index+1, pause=2)
    return list(results)


def get_domain(query, index, bad_queries):
    """Given a query, returns the domain of the first Google search result

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
        return "BADQUERY"
    bad_queries = 0
    return domain
    
    

def set_up_dataframe(file_name):
    """Given path to a csv, sets up the dataframe
    
    Given the path to a csv file, sets up a dataframe from the 
    file and adds the fields 'www' and 'domain' at the end

    """  
    df = pd.read_csv(file_name)
    index = len(df.columns)
    df.insert(index, 'www', 'www.')
    df.insert(index+1, 'domain', None)
    return df

def get_yes_no(message):
    print(message)
    proceed = ""
    while(True):
        proceed = input("[Y/N]")
        if proceed == 'Y':
            return True
        elif proceed == 'N':
            return False

def bad_queries_fail(i):
    proceed = get_yes_no("Crawler encountered 10 bad queries in a row. Proceed?")
    if proceed:
        return
    else:
        df.to_csv("FAILED_BAD_QUERIES_0-{}.csv".format(i))
        print("Exiting...")
        exit() 

def get_name_address(i):
    name = df.iloc[i,0]
    address = ""
    for j in range(2,5):
        frag = str(df.iloc[i,j])
        if frag != "nan":
            address = address + frag + ' '
    return name, address


def crawl(df, new_file):
    bad_queries = 0
    num_rows = df.shape[0]
    domain_index = list(df.columns).index('domain')
    for i in range(num_rows):
        name, address = get_name_address(i)
        domain = get_domain(name + ' ' + address, i, bad_queries)
        df.iat[i, domain_index] = domain
        if bad_queries >= 10:
            bad_queries_fail(i)
        if i%100 == 0:
            incremental_save(df, new_file, i)
    return df


def init(file_name, new_file):
    os.chdir("C:\\Users\\micha\\Documents\\Python-Projects\\company-info-scraper")
    df = set_up_dataframe(file_name)
    return df

def incremental_save(df, new_file, index):
    temp_name = "INCREMENTAL_SAVE_0-{}_{}".format(index, new_file)
    df.to_csv(temp_name)
    print("Saved incremental progress. Next index: {}".format(index+1))

delete_old_output(new_file)
df = init(file_name, new_file)
df = crawl(df, new_file)
df.to_csv(new_file)