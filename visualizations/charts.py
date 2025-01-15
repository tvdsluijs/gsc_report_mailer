import matplotlib.pyplot as plt

def generate_chart(comparison_data, output_path='comparison_chart.png'):
    plt.figure(figsize=(10, 5))
    queries = list(comparison_data.keys())[:10]
    current_clicks = [comparison_data[q]['current_clicks'] for q in queries]
    previous_clicks = [comparison_data[q]['previous_clicks'] for q in queries]

    plt.barh(queries, current_clicks, label='Current', alpha=0.7)
    plt.barh(queries, previous_clicks, label='Previous', alpha=0.7)
    plt.xlabel('Clicks')
    plt.ylabel('Queries')
    plt.title('Top 10 Queries: Current vs Previous Period')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
