import csv
import argparse
from collections import defaultdict
from datetime import datetime

def process_csv(input_file_path, output_file_path):
    transactions = defaultdict(lambda: defaultdict(float))
    ignored_transaction_types = set()

    with open(input_file_path, 'r') as infile:
        csv_reader = csv.DictReader(infile)  # No need to specify a delimiter for commas; it's the default.

        for row in csv_reader:
            transaction_type = row['Transaction Type']
            valid_types = ["Advanced trade trade", "Buy", "Converted from", "Sell"]

            if transaction_type not in valid_types:
                ignored_transaction_types.add(transaction_type)
                continue

            date_time_str = row['Date & time'].rstrip('Z')
            date_time_obj = datetime.fromisoformat(date_time_str)
            date_str = date_time_obj.date().isoformat()

            if row['Asset Acquired']:
                buy_asset = row['Asset Acquired']
                buy_amount = float(row['Quantity Acquired (Bought, Received, etc)']) if row['Quantity Acquired (Bought, Received, etc)'] else 0.0
                sell_asset = 'USD'
                sell_amount = float(row['Cost Basis (incl. fees and/or spread) (USD)']) if row['Cost Basis (incl. fees and/or spread) (USD)'] else 0.0
            else:
                sell_asset = row['Asset Disposed (Sold, Sent, etc)']
                sell_amount = float(row['Quantity Disposed']) if row['Quantity Disposed'] else 0.0
                buy_asset = 'USD'
                buy_amount = float(row['Proceeds (excl. fees and/or spread) (USD)']) if row['Proceeds (excl. fees and/or spread) (USD)'] else 0.0

            key = (date_str, buy_asset, sell_asset)
            transactions[key]['Buy Amount'] += buy_amount
            transactions[key]['Sell Amount'] += sell_amount

    with open(output_file_path, 'w', newline='') as outfile:
        headers = ['Date', 'Buy Asset', 'Buy Amount', 'Sell Asset', 'Sell Amount']
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(headers)

        for key, amounts in transactions.items():
            csv_writer.writerow([key[0], key[1], amounts['Buy Amount'], key[2], amounts['Sell Amount']])

    if ignored_transaction_types:
        print(f"Ignored Transaction Types: {', '.join(ignored_transaction_types)}")

def main():
    parser = argparse.ArgumentParser(description="Process a CSV file.")
    parser.add_argument('input', help="Path to the input CSV file.")
    parser.add_argument('output', help="Path to the output file.")

    args = parser.parse_args()

    process_csv(args.input, args.output)

if __name__ == "__main__":
    main()
