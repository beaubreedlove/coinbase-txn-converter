# Coinbase Transaction Converter for Capital Gains Tax

This script is designed to streamline the transaction activity data that Coinbase produces, optimizing it for capital gains tax calculation software. By converting the detailed `Raw transaction activity report (CSV)` into a more concise format, users can save on costs, especially if the software charges per transaction or row of input data.

## 🚫 Disclaimers

1. **Taxation**: This script and its outputs should not constitute tax advice. Always consult with a tax professional or CPA before determining how to report your taxes.

2. **Financial Advice**: This tool is not intended to provide financial advice. Cryptocurrency investments carry high risks. Only invest what you can afford to lose. Before making any financial decisions, it's essential to consult with a financial advisor or professional.

3. **Securities Warning**: The U.S. Securities and Exchange Commission (SEC) has opined that most cryptocurrencies, with the notable exception of Bitcoin, may be regarded as securities. The SEC has even approached Coinbase directly to halt trading of all crypto assets except Bitcoin. Always exercise due diligence and research before making investment decisions.

4. **Exchange and Trading Risks**: Keeping your coins on exchanges can carry high risks, including but not limited to hacking, mismanagement, and regulatory interventions. Trading cryptocurrencies also introduces its own set of risks due to market volatility. Consider using private wallets and employ security best practices when storing and trading your cryptocurrencies.

5. **Decentralization & Ownership**: Cold storage Bitcoin is the most decentralized crypto asset, but to truly ensure you own your asset, you must run your own node. For more information on the importance of nodes and how to get started, visit [bitcoin.org](https://bitcoin.org).

## Why Use This Converter

When exporting transaction details from Coinbase, the raw data can be both detailed and extensive. For users looking to calculate capital gains tax, much of this data might be redundant or unnecessary. This script simplifies and aggregates the data into a clearer format, making it friendlier for tax software.

## How to Use

1. **Download the Raw Transaction Report from Coinbase**:
    - Go to [Coinbase's tax documents page](https://accounts.coinbase.com/taxes/documents).
    - Select "Custom Reports".
    - Download the `Raw transaction activity report (CSV)`.

2. **Execute the Script**:
```
   python convert-transactoins.py input_file.csv output_file.csv
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

Beau Breedlove - beaubreedlove@gmail.com

Repository: [https://github.com/beaubreedlove/coinbase-txn-converter](https://github.com/beaubreedlove/coinbase-txn-converter)
