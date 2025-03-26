import pandas as pd
from datetime import datetime

def excelRender(table,filename = None):

    df = pd.DataFrame(table)

    if filename is None:
        filename = f"Result-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xlsx"

    # Export the DataFrame to an Excel file
    df.to_excel(filename, index=False)
        