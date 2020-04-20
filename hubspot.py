from hubspot3 import Hubspot3
import pprint

API_KEY = 'b62a495f-ca1b-48e8-a98e-20bac54d3bac'

client = Hubspot3(api_key=API_KEY)

all_companies = client.companies.search_domain('hubspot.com', limit = 1)

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(all_companies)