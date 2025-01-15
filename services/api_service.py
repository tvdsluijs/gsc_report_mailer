from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_search_console_data(site_url, start_date, end_date, config):
    credentials = service_account.Credentials.from_service_account_file(
        config["SERVICE_ACCOUNT_FILE"], scopes=config["SCOPES"]
    )
    service = build('searchconsole', 'v1', credentials=credentials)
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query', 'page'],
        'rowLimit': 1000
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    return response.get('rows', [])
