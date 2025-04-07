import pandas as pd
from datetime import datetime
import os

def excelRender(table, filename=None, folder_path="excel"):

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    df = pd.DataFrame(table)

    if filename is None:
        filename = f"Result_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"

    file_path = os.path.join(folder_path, filename)

    # Export the DataFrame to an Excel file
    df.to_excel(file_path, index=False)
        