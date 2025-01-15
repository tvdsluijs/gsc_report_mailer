import datetime
from configs.config import CONFIG
from configs.websites_config import WEBSITES
from services.api_service import get_search_console_data
from services.email_service import send_email
from visualizations.charts import generate_chart
from jinja2 import Environment, FileSystemLoader

# Datuminstellingen
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)
previous_start_date = start_date - datetime.timedelta(days=30)
previous_end_date = start_date - datetime.timedelta(days=1)

# Jinja2-initialisatie
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('email_template.html')

# Rapport genereren voor elke website
for website in WEBSITES:
    current_data = get_search_console_data(website["site_url"], str(start_date), str(end_date), CONFIG)
    previous_data = get_search_console_data(website["site_url"], str(previous_start_date), str(previous_end_date), CONFIG)

    # Analyse en grafiek
    comparison_data = {q['keys'][0]: {
        'current_clicks': q['clicks'],
        'previous_clicks': next((p['clicks'] for p in previous_data if p['keys'][0] == q['keys'][0]), 0),
        'change': q['clicks'] - next((p['clicks'] for p in previous_data if p['keys'][0] == q['keys'][0]), 0)
    } for q in current_data}

    chart_path = f"visualizations/{website['site_url'].replace('https://', '').replace('/', '_')}_chart.png"
    generate_chart(comparison_data, chart_path)

    html_content = template.render(comparison_data=comparison_data, start_date=start_date, end_date=end_date)

    # E-mail verzenden
    send_email(html_content, chart_path, CONFIG, website["receiver_email"])

print("Rapporten verzonden!")
