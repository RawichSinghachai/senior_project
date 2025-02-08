import pandas as pd
import os
from datetime import datetime

# Sample dictionary
data = [{'UserId': 'd12ef752-d1aa-4902-8e7e-19cef5ccfa98', 'FirstName': 'yami', 'LastName': 'tryt', 'Department': 'fgh', 'Gender': 'Male', 'Email': 'tytf', 'BirthDate': '06/09/2026'}, {'UserId': 'f06f0ac5-4c0e-467c-8f63-6e3f50d39d73', 'FirstName': 'Amin', 'LastName': '', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '06/09/2024'}, {'UserId': '60439ca8-e739-4c86-91e1-e67c2d46853f', 'FirstName': 'Jame', 'LastName': 'djfljsdf', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '06/09/2024'}, {'UserId': '50f44040-711e-4eac-bcb2-8a8e4d3263d3', 'FirstName': '', 'LastName': '', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '06/09/2024'}, {'UserId': 'd0727827-5b6a-4fac-9627-e8db86c81b87', 'FirstName': '', 'LastName': '', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '10/09/2024'}, {'UserId': '6bf5af62-0180-4f6c-af93-83745c2cc789', 'FirstName': '', 'LastName': '', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '06/09/2020'}, {'UserId': 'cee66332-c376-47fb-807e-c5b063cf8986', 'FirstName': 'add', 'LastName': 'add', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '06/09/2024'}, {'UserId': '6080813d-c4c2-40c6-8621-c82f442fde24', 'FirstName': 'edd', 'LastName': 'edd', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '07/09/2024'}, {'UserId': '7c007c3d-97b1-4386-b4ed-551564f21c72', 'FirstName': '555', 'LastName': '', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '07/09/2024'}, {'UserId': '5ab9d56d-9bfa-4dcf-89cc-7585ffa7201b', 'FirstName': '111', 'LastName': '', 'Department': '', 'Gender': '', 'Email': '', 'BirthDate': '07/09/2024'}]

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Define the file name
file_name = 'output.xlsx'

# Check if the file exists
if os.path.exists(file_name):
    # Generate a new file name with a timestamp to prevent overwriting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"output_{timestamp}.xlsx"

# Export the DataFrame to an Excel file
df.to_excel(file_name, index=False)
print(f"File saved as: {file_name}")