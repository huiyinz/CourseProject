if __name__ == '__main__':
    import os
    import pandas as pd
    import load10K
    import process10K

    global outputLocation, companyFolders
    #excel_adrs, dir, n_file, end_date = sys.argv
    excel_adrs = '/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/Energy_Sector.xlsx'
    dir = "/Users/huiyinz/Desktop/UIUC/CS410/CourseProject/"
    n_file = 3
    end_date = '2022-01-01'

    companyFolders = os.path.join(dir, "sec-edgar-filings")
    outputLocation = os.path.join(dir, "ProcessedFiles")

    load10K.load10K(excel_adrs, dir, n_file, end_date)
    process10K.processFiles(outputLocation, companyFolders)

    company_names = []
    company_records = []
    company_dates = []
    for folder in [os.path.join(outputLocation, x) for x in os.listdir(outputLocation)]:
        company = os.path.basename(folder)
        if company == '.DS_Store': continue
        if not os.path.isdir(folder): continue
        folder_10K = os.path.join(folder, '10-K_Risk_Factors')
        for txts in [os.path.join(folder_10K, x) for x in os.listdir(folder_10K)]:
            risk_factors = open(txts,"r")
            risk_factors_string =  risk_factors.read()
            company_names.append(company)
            company_records.append(" ".join(risk_factors_string.split()) + '\n')
            company_dates.append(os.path.basename(txts)[:-4])

    company_filings = {}
    company_filings['Company'] = company_names
    company_filings['Dates'] = company_dates
    company_filings["Filings"] = company_records

    df = pd.DataFrame.from_dict(company_filings)
    filepath = os.path.join(outputLocation, 'Filings.csv')
    df.to_csv(filepath)  

    f = open(os.path.join(outputLocation, 'Filings_Text.txt'), 'w')
    f.writelines(company_records)
    f.close()