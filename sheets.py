import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RZncOT2E9K2uA9VR2shGB-EdEucbCb3ED6WGnrA4-iY/edit?gid=1276249909#gid=1276249909"

# Worksheet/tab name
WORKSHEET_NAME = "BackendData"


def load_data():

    workbook = client.open_by_url(SHEET_URL)

    sheet = workbook.worksheet(WORKSHEET_NAME)

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    # =========================
    # Convert Numeric Columns
    # =========================

    numeric_columns = [
        "Order Qty",
        "CutWt",
        "TotalWeight",
        "Per Item Price",
        "Produced Qty"
    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df
