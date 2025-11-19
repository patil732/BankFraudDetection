import pandas as pd

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mall_customers.csv"
df = pd.read_csv(url)
df.to_csv("mall_customers.csv", index=False)  # saves file locally
print("Dataset downloaded and saved as mall_customers.csv")
df.head()
