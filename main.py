import scraper
import file_utils
import logging


'''
Company Info Scraper

This program takes a csv containing company's names and address
and scrapes Google search results to attempt to find the domain of the company.
Once the domain is identified, the company can be entered into Hubspot which
auto-populates information about the company.


'''

if __name__ == "__main__":
    input_file, output_file, log_file = file_utils.get_file_selections()
    print(input_file, output_file, log_file)
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='logfile.txt')
    # df = file_utils.init(input_file, save_dir)
    # df = scraper.crawl(df, output_file, save_dir)
    # file_utils.save(df, save_dir, output_file)
    


    