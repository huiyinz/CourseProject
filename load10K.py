# Please install the package if you haven't already
# You must have pip>=19.3 to install pandas from PyPI

# pip install sec-edgar-downloader
# pip install pandas

def load10K(excel_adrs = '/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/Energy_Sector.xlsx',
            dir = "/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/",
            n_file = 1,
            end_date = '2022-01-01'):

    from sec_edgar_downloader import Downloader
    import pandas as pd
    import process10K

    # Please copy and paste your interested companies from
    # https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_energy&o=-marketcap
    # You can change to a different economic sector
    # Please save in an excel file and specify the directory for download

    excel_file_adrs = excel_adrs
    download_adrs = dir

    # Do not change the code below
    companies = pd.read_excel(excel_file_adrs, engine='openpyxl')
    dl = Downloader(download_adrs)
    tickers = list(companies['Ticker'])

    for ticker in tickers:
        ticker = str(ticker)
        # Feel free to change the parameters, check documentations here:
        # https://pypi.org/project/sec-edgar-downloader/
        dl.get("10-K", ticker, amount = n_file, before = end_date)
