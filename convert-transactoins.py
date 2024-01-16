import csv
import argparse
from collections import defaultdict
from datetime import datetime, date

def format_amount(amount):
    return '{:.8f}'.format(round(float(amount), 8))

def process_csv(input_file_path, output_file_path, start_date, end_date):
    transactions = []
    last_transaction_for_asset = {}
    ignored_transaction_types = set()
    current_date = None
    previous_datetime_str = None

    with open(input_file_path, 'r') as infile:
        csv_reader = csv.DictReader(infile)  # No need to specify a delimiter for commas; it's the default.

        for row in csv_reader:
            # Check if the current transaction datetime string is earlier than the previous one
            if previous_datetime_str and row['Date & time'] < previous_datetime_str:
                raise ValueError(f"Out-of-order transaction detected. Datetime {row_datetime_str} is earlier than previous transaction datetime {previous_datetime_str}.")

            previous_datetime_str = row['Date & time']

            # Convert the string date from the row into a date object
            row_date = date.fromisoformat(row['Date & time'].split("T")[0])

            # If a new date is encountered, flush the last transactions
            if row_date != current_date:
                for last_transaction in last_transaction_for_asset.values():
                    if last_transaction:
                        transactions.append(last_transaction)
                last_transaction_for_asset.clear()
                current_date = row_date

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
                current_asset = row['Asset Acquired']
                transaction_type = 'Buy'
            else:
                sell_asset = row['Asset Disposed (Sold, Sent, etc)']
                sell_amount = float(row['Quantity Disposed']) if row['Quantity Disposed'] else 0.0
                buy_asset = 'USD'
                buy_amount = float(row['Proceeds (excl. fees and/or spread) (USD)']) if row['Proceeds (excl. fees and/or spread) (USD)'] else 0.0
                current_asset = row['Asset Disposed (Sold, Sent, etc)']
                transaction_type = 'Sell'

            # Check if we should start a new transaction group
            last_transaction = last_transaction_for_asset.get(current_asset)
            if last_transaction and (last_transaction['Date'] != date_str or last_transaction['Type'] != transaction_type):
                transactions.append(last_transaction)
                last_transaction = None

            if not last_transaction:
                last_transaction = {'Date': date_str, 'Buy Asset': buy_asset, 'Sell Asset': sell_asset, 'Buy Amount': 0, 'Sell Amount': 0, 'Type': transaction_type}

            # Update amounts
            last_transaction['Buy Amount'] += buy_amount
            last_transaction['Sell Amount'] += sell_amount

            last_transaction_for_asset[current_asset] = last_transaction

        # Flush any remaining transactions for the last date
        for last_transaction in last_transaction_for_asset.values():
            if last_transaction:
                transactions.append(last_transaction)

    with open(output_file_path, 'w', newline='') as outfile:
        headers = ['Date', 'Buy Asset', 'Buy Amount', 'Sell Asset', 'Sell Amount']
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(headers)

        for transaction in transactions:
            csv_writer.writerow([transaction['Date'], transaction['Buy Asset'], format_amount(transaction['Buy Amount']), transaction['Sell Asset'], format_amount(transaction['Sell Amount'])])

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
