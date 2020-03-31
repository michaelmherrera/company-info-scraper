from googlesearch import search 
from urllib.parse import urlparse
from googlequery import google_query
import pandas as pd
import os, time, random

#TODO: Change for GitHub upload
#Get api_key and cse_id for Google search
from secrets import API_KEY, CSE_ID

file_name = 'dummy.csv' #'texas_firms_roster.csv'
new_file = 'dummy_output.csv' #'texas_firms_roster_with_domain.csv'

#Here's a comment

#TODO: Remove this once done testing
def delete_old_output(new_file):
    import os
    if os.path.exists(new_file):
        os.remove(new_file)
    else:
        print("The file does not exist") 


def get_domain(query):
    """Given a query, returns the domain of the first Google search result

    """
    #Google query with num = 1 returns a list 1 link, we so use [0] to get the link
    links = []
    try:
        links = google_query(query, API_KEY, CSE_ID, num=1)
    except:
        print("BAD QUERY: " + query)
        return "BADQUERY"
    link = links[0]
    domain = urlparse(link)[1]
    if 'www' in domain:
        domain = domain[4:]
    return domain

def set_up_dataframe(file_name):
    """Given the path to a csv file, sets up a dataframe from the file and adds the fields 'www' and 'domain' at the end

    """  
    df = pd.read_csv(file_name)
    index = len(df.columns)
    df.insert(index, 'www', 'www.')
    df.insert(index+1, 'domain', None)
    return df

def name_address_search(df):
    num_rows = df.shape[0]
    domain_index = list(df.columns).index('domain')
    for i in range(num_rows):
        name = df.iloc[i,0]
        address = ""
        for j in range(1,6):
            frag = str(df.iloc[i,j])
            if frag != "nan":
                address = address + frag + ' '
        domain = get_domain(name + ' ' + address, )
        df.iat[i, domain_index] = domain
    return df


delete_old_output(new_file)
df = set_up_dataframe(file_name)
df = name_address_search(df)
print(df)
df.to_csv(new_file)
    





'''Old Search Strat'''
# def query_request(query, result_index):
#     results = search(query, tld="com", num=1, start=result_index, stop=result_index+1, pause=2)
#     result = list(results)[0]
#     domain = urlparse(result)[1]
#     if 'www' in domain:
#         domain = domain[4:]
#     print("Query: {} | Domain: {}".format(query, domain))
#     return domain

# def get_good_domain(company_name, company_address):
#     query = company_name + ' ' + company_address
#     result_index = 0
#     domain = query_request(query, result_index)
#     return domain