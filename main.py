import scraper
import file_utils
import logging
import argparse
from pathlib import Path
from time import strftime


'''
Company Info Scraper

This program takes a csv containing company's names and address
and scrapes Google search results to attempt to find the domain of the company.
Once the domain is identified, the company can be entered into Hubspot which
auto-populates information about the company.


'''

def get_args():
    """ Parse arguments from the commandline

    Returns
    -------
    Namespace A collection of key-value pairs of options. For more
        information, read the documentation of parse_args().
    """
    
    description = "A utility that processes a file containing company names and addresses \
        and retrieves the it's best guess of each company's website URL."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('Input', metavar='input', type=str, 
        help='the input csv file containing company names and addresses')
    parser.add_argument('-o', '--output', help='the output file. \
        If no file specified, writes to output_<%Y-%m-%d_%H-%M-%S>.csv  in the current working directory')
    return parser.parse_args()

if __name__ == "__main__":

    args = get_args()

    input = Path(args.Input)
    
    output = None
    if args.output:
        output = Path(args.output)
    else:
        datetime = strftime("%Y-%m-%d_%H-%M-%S")
        output = Path(f'output_{datetime}.csv')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    
    df = file_utils.init(input, output)
    df = scraper.crawl(df, output)
    df.to_csv(output)
    


    