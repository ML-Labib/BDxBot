import requests
import csv

def get_csv_form_sheet(gsheet_url: str):

    url: str  = gsheet_url.split("/edit")[0] + "/export?format=csv"

    try:
        response: requests.Response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch CSV data. Status code: {response.status_code, response.reason}")
        reader = csv.DictReader(response.content.decode('utf-8').splitlines())
        print("CSV data fetched successfully.")
        return (response.status_code, reader)

    except Exception as e:
        return (None, f"Error fetching CSV data: {e}")


if __name__ == "__main__":
    # gsheet_url = "https://docs.google.com/spreadsheets/d/1h6f61MqmR8N0YuPbf1hgfe2vR_LjoI6WereUupiD7Qk/edit?gid=0#gid=0"
    ghsheet_url = "https://docs.google.com/spreadsheets/d/1X1bX4kCk3b2v9v5Z8F6jH9K0L7Q2Y3Z4A5B6C7D8E9F"
    get_csv_form_sheet(ghsheet_url)