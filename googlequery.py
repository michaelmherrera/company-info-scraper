from googleapiclient.discovery import build

def google_query(query, api_key, cse_id, **kwargs):
    """Returns a list of web links from a Google search

    Parameters:
        query (str) - The search query
        api_key (str) - Your personal custom search API key
        cse_id (str) - Your person custom search engine (cse) ID
        **kwargs - Use "num" kwarg to denote number of results you want

    Returns:
        links (list) - A list of web links
    """
    query_service = build("customsearch", "v1", developerKey=api_key)  
    query_results = query_service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    # Results is a list. Each element is a search result formatted as a dict
    results = query_results['items']
    links = []
    for result in results:
        links.append(result['link'])
    return links

print(google_query("potato", "AIzaSyBKCyZ2o0kL9bukbBh-4P7sjIEAsh6ud7M", "014736235146535078122:2tyml511uzu", num=1))


