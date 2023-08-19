# Coinbase Transaction Converter for Capital Gains Tax

This script is designed to streamline the transaction activity data that Coinbase produces, optimizing it for capital gains tax calculation software. By converting the detailed `Raw transaction activity report (CSV)` into a more concise format, users can save on costs, especially if the software charges per transaction or row of input data.

## Why Use This Converter

When exporting transaction details from Coinbase, the raw data can be both detailed and extensive. For users looking to calculate capital gains tax, much of this data might be redundant or unnecessary. This script simplifies and aggregates the data into a clearer format, making it friendlier for tax software.

## How to Use

1. **Download the Raw Transaction Report from Coinbase**:
    - Go to [Coinbase's tax documents page](https://accounts.coinbase.com/taxes/documents).
    - Select "Custom Reports".
    - Download the `Raw transaction activity report (CSV)`.

2. **Execute the Script**:
```
   python script_name.py input_file.csv output_file.csv
```

3. **Review the Processed Data**: The `output_file.csv` will contain the optimized data ready for your capital gains tax software.

## Output Data Structure

The resulting CSV file will have the following columns:

- `Date`: Date of the transaction.
- `Buy Asset`: Asset that was purchased.
- `Buy Amount`: Quantity of the asset that was acquired.
- `Sell Asset`: Asset that was sold.
- `Sell Amount`: Quantity of the asset that was disposed of.

## Prerequisites

- Python 3.x
- CSV module (comes built-in with Python)

## Contributions

Feel free to submit pull requests, report bugs, or suggest new features!

## License

This tool is [MIT](https://choosealicense.com/licenses/mit/) licensed, meaning you're free to use, modify, and distribute it as you see fit.

## Contact

Your Name - your.email@example.com

Repository: [https://github.com/beaubreedlove/coinbase-txn-converter](https://github.com/beaubreedlove/coinbase-txn-converter)
