Data files
**********
1. raw_transactions.csv -- Raw Transactions
2. cleaned_transactions.csv -- Cleaned Transcations
3. engineered_features.csv -- Engineered Features

Python Files:
1. main.py -- Main file calling all the other programs
2. data_gen.py -- Data Generation file
3. cleaning.py -- Cleaning file
4. features.py -- Feature File
5. utils.py -- Utility File
6. eda.py -- EDA file( Perform exploratory data analysis)


EDA Summary:

        transaction_id  customer_id  ... discount_rate payment_type
count      1000.000000  1000.000000  ...    982.000000         1000
unique             NaN          NaN  ...           NaN            4
top                NaN          NaN  ...           NaN         card
freq               NaN          NaN  ...           NaN          597
mean        500.500000  1993.021000  ...      0.138902          NaN
std         288.819436   583.095962  ...      0.087610          NaN
min           1.000000  1002.000000  ...      0.002727          NaN
25%         250.750000  1491.750000  ...      0.069519          NaN
50%         500.500000  1986.500000  ...      0.122527          NaN
75%         750.250000  2503.750000  ...      0.192849          NaN
max        1000.000000  2997.000000  ...      0.474320          NaN

[11 rows x 10 columns]
