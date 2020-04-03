from urllib.parse import urlparse
from googlesearch import search
import pandas as pd
import os, time, random

file_name = 'dummy.csv' #'texas_firms_roster.csv'
new_file = 'dummy_output.csv' #'texas_firms_roster_with_domain.csv'
_counter = 0

#TODO: Remove this once done testing
def delete_old_output(new_file):
    import os
    if os.path.exists(new_file):
        os.remove(new_file)
    else:
        print("The file does not exist") 

def get_urls(query, result_index):
    results = search(query, tld="com", num=1, start=result_index, stop=result_index+1, pause=2)
    return list(results)


def get_domain(query):
    global _counter
    """Given a query, returns the domain of the first Google search result

    """
    #get_urls with num = 1 returns a list 1 link, we so use [0] to get the link
    # try:
    links = get_urls(query, 0)
    link = links[0]
    domain = urlparse(link)[1]
    if 'www' in domain:
        domain = domain[4:]
    print("{} Query: {} | Domain: {}".format(_counter, query, domain))
    _counter+=1
    return domain
    # except:
    #     print("BAD QUERY: " + query)
    #     return "BADQUERY"
    

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

def name_city_state_search(df):
    num_rows = df.shape[0]
    domain_index = list(df.columns).index('domain')
    for i in range(num_rows):
        name = df.iloc[i,0]
        address = ""
        for j in range(2,5):
            frag = str(df.iloc[i,j])
            if frag != "nan":
                address = address + frag + ' '
        domain = get_domain(name + ' ' + address)
        df.iat[i, domain_index] = domain
    return df


delete_old_output(new_file)
df = set_up_dataframe(file_name)
df = name_city_state_search(df)
print()
print(df)
df.to_csv(new_file)