import fileUtils
import scraper
import file_utils

if __name__ == "__main__":
    input_file, save_dir, output_file = fileUtils.get_file_selections()
    df = file_utils.init(input_file, save_dir)
    df = scraper.crawl(df, output_file, save_dir)
    file_utils.save(df, save_dir, output_file)
    


    