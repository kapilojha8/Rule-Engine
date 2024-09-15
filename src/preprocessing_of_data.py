import pandas as pd
from datetime import datetime
import os
import json

class PreprocessingOfData:
    def __init__(self,ClientData={}, csv_file_path="../data/Data_from_Client.csv", ClientDataDict = True) -> None:
        """
        Initializes the PreprocessingOfData class by loading data and setting up necessary fields.
        
        Parameters:
        csv_file_path (str): The file path of the CSV file containing client data. Defaults to "../data/Data_from_Client.csv".
        """
        if ClientDataDict and isinstance(ClientDataDict, dict):
            print("Dict_data")
        else:
            self.csv_file_path = csv_file_path
            self.Client_data = self.load_data()

        # Initialize Data_of_Rule_test to None
        self.Data_of_Rule_test = None
        # Create ABN and GST dates, calculate Asset age
        if self.Client_data is not None:
            if ClientDataDict:
                self.create_abn_gst_dates()
            else:
                if len(self.Client_data.columns) and  all(item in self.Client_data.columns for item in ['Asset_age','GST_in_Months','ABN_in_Months']):
                    ValueError("The Columns were not in Dataframe")
            self.create_asset_classification()
            self.create_Deposit_Amount_Percentage()

    def create_asset_classification(self):
        with open('../data/Preprocessing_Data.json', 'r') as file:
                self.asset_classes = json.load(file)

        def classify_asset(asset):
            asset_upper = asset.upper()
            if asset_upper in self.asset_classes["Motor_Vehicles"]:
                return "Motor_Vehicles"
            elif asset_upper in self.asset_classes["Primary_Assets"]:
                return "Primary_Assets"
            else:
                return "Unknown"

        self.Client_data['Asset_classification'] = self.Client_data['asset_type'].apply(classify_asset)
        
    
    def create_Deposit_Amount_Percentage(self):

        self.Client_data["Deposit_Amount_percentage"] = (self.Client_data['deposit_amount'].fillna(0) / self.Client_data['amount_financed'])  



    def load_data(self):
        """
        Loads client data from a CSV file.

        Returns:
        pd.DataFrame: The loaded client data as a pandas DataFrame.
        """
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {self.csv_file_path}. Please check the file path.")
        
        try:
            data = pd.read_csv(self.csv_file_path)
            if data.empty:
                raise ValueError("The CSV file is empty. Please provide a valid CSV file with data.")
            return data
        except pd.errors.EmptyDataError:
            raise ValueError("The CSV file is empty. Please provide a valid CSV file with data.")
        except pd.errors.ParserError:
            raise ValueError("Error parsing the CSV file. Please check the file format.")
        except Exception as e:
            raise Exception(f"An error occurred while loading the data: {str(e)}")

    def create_abn_gst_dates(self, current_year=datetime.now().year, current_date=pd.to_datetime(datetime.now().strftime('%d-%m-%Y'))):
        """
        Calculates asset age and the number of months for GST and ABN registration.

        Parameters:
        current_year (int): The current year to calculate the asset age. Defaults to the current year.
        current_date (pd.Timestamp): The current date to calculate the number of months for GST and ABN registration. Defaults to today's date.
        """
        if current_year is None:
            current_year = datetime.now().year
        if current_date is None:
            current_date = pd.to_datetime(datetime.now().strftime('%d-%m-%Y'))

        try:
            # Calculate the asset age based on the current year and asset manufacture year
            self.Client_data['Asset_age'] = current_year - self.Client_data['asset_manufacture_year']

            # Convert GST and ABN registration dates from string to datetime format
            self.Client_data['gst_registered_date'] = pd.to_datetime(self.Client_data['gst_registered_date'], format='%d-%m-%Y')
            self.Client_data['abn_registered_date'] = pd.to_datetime(self.Client_data['abn_registered_date'], format='%d-%m-%Y')

            # Calculate the number of months since GST registration
            self.Client_data['GST_in_Months'] = (current_date.year - self.Client_data['gst_registered_date'].dt.year) * 12 + (current_date.month - self.Client_data['gst_registered_date'].dt.month)

            # Calculate the number of months since ABN registration
            self.Client_data['ABN_in_Months'] = (current_date.year - self.Client_data['abn_registered_date'].dt.year) * 12 + (current_date.month - self.Client_data['abn_registered_date'].dt.month)

            # Create a new column 'Loan_Amount' as a copy of the 'amount_financed' column
            self.Client_data['Loan_Amount'] = self.Client_data['amount_financed'].copy()
        except KeyError as e:
            raise KeyError(f"Missing column in data: {str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while creating ABN and GST dates: {str(e)}")


    def dropping_columns(self, column_names=[]):
        """
        Drops irrelevant columns from the dataset.

        Parameters:
        column_names (list): A list of column names to drop from the DataFrame.
        """
        if not isinstance(column_names, list):
            raise TypeError("Column names must be provided as a list.")
        
        if any([not isinstance(col, str) for col in column_names]):
            raise ValueError("All column names must be strings.")
        
        missing_columns = [col for col in column_names if col not in self.Client_data.columns]
        if missing_columns:
            raise KeyError(f"The following columns are not in the DataFrame: {missing_columns}")
        
        try:
            self.Client_data.drop(column_names, axis=1, inplace=True)
        except Exception as e:
            raise Exception(f"An error occurred while dropping columns: {str(e)}")

    def extracting_few_records(self, n_records):
        """
        Extracts the first N records from the dataset.

        Parameters:
        n_records (int): The number of records to extract.

        Returns:
        pd.DataFrame: A DataFrame containing the first N records.
        """
        if not isinstance(n_records, int) or n_records <= 0:
            raise ValueError("n_records must be a positive integer.")
        
        try:
            return self.Client_data.head(n_records).copy()
        except Exception as e:
            raise Exception(f"An error occurred while extracting records: {str(e)}")
    
    def converting_df_to_dict(self):
        """
        Converts the DataFrame to a list of dictionaries.
        """
        try:
            self.Data_of_Rule_test = self.Client_data.to_dict(orient="records")
        except Exception as e:
            raise Exception(f"An error occurred while converting the DataFrame to a dictionary: {str(e)}")