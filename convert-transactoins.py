


print("===================== TODO: Make it so if you buy, then sell, then buy back in a given day it separates the buys into 2")

import csv
import argparse
from collections import defaultdict
from datetime import datetime, date

def format_amount(amount):
    return '{:.8f}'.format(round(float(amount), 8))

def process_csv(input_file_path, output_file_path, start_date, end_date):
    transactions = defaultdict(lambda: defaultdict(float))
    ignored_transaction_types = set()

    with open(input_file_path, 'r') as infile:
        csv_reader = csv.DictReader(infile)  # No need to specify a delimiter for commas; it's the default.

        for row in csv_reader:
            # Convert the string date from the row into a date object
            row_date = date.fromisoformat(row['Date & time'].split("T")[0])

            # If start_date or end_date is provided, filter rows based on these dates
            if start_date and row_date < start_date:
                continue
            if end_date and row_date > end_date:
                continue

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
            csv_writer.writerow([key[0], key[1], format_amount(amounts['Buy Amount']), key[2], format_amount(amounts['Sell Amount'])])

    if ignored_transaction_types:
        print(f"Ignored Transaction Types: {', '.join(ignored_transaction_types)}")

def main():
    parser = argparse.ArgumentParser(description="Process a CSV file.")
    parser.add_argument('input', type=str, help="Path to the input CSV file.")
    parser.add_argument('output', type=str, help="Path to the output file.")
    parser.add_argument('--start_date', type=str, help='Starting date for filtering in YYYY-MM-DD format.', default=None)
    parser.add_argument('--end_date', type=str, help='Ending date for filtering in YYYY-MM-DD format.', default=None)

    args = parser.parse_args()

    start_date = date.fromisoformat(args.start_date) if args.start_date else None
    end_date = date.fromisoformat(args.end_date) if args.end_date else None

    process_csv(args.input, args.output, start_date, end_date)

if __name__ == "__main__":
    main()
