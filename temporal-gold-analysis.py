# IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
from pydantic import BaseModel, Field
from datetime import date
import os


# SCHEMAS
class AssetData(BaseModel):
    ticker: str
    timestamp: date
    price_usd: float = Field(gt=0)
    volume: float = Field(default=0.0)


# FUNCTIONS
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "Data Analytics", "gold_prices_10y.csv")

df = pd.read_csv(file_path)

print(list(df.columns))
length = print(len(df))

df.head()

# Have to convert to datetime form so Python reads as date not string
df["Date"] = pd.to_datetime(df["Date"])


# What was the highest and lowest prices of each year?
# Creating a class to assign the same method to multiple columns


# MAIN LOGIC
class LowestHighestPrice:

    def __init__(self, df, year_col="Year", low_col="Low", high_col="High"):
        self.df = df
        self.year_col = year_col
        self.low_col = low_col
        self.high_col = high_col

    # Dependency injection
    def df_ref(self):
        df_copy = self.df.copy()
        df_copy["Date"] = df_copy["Date"].dt.year
        self.df = df_copy

    def ann_low_high(self):
        low = (
            self.df.groupby("Year")[[self.low_col, self.high_col]]
            .agg(low=(self.low_col, "min"), high=(self.high_col, "max"))
            .reset_index()
        )
        for _, row in low.iterrows():
            print(f"Year {row['Year']}: Lowest price = {row['low']:.2f}")
            print(f"Year {row['Year']}: Highest price = {row['high']:.2f}")
        return low

    def sum_low_high(self):
        avg_low = self.df[self.low_col].mean()
        avg_high = self.df[self.high_col].mean()
        print(
            f"The average low is {avg_low:.2f} and the average high is {avg_high:.2f}"
        )


lpy = LowestHighestPrice(df)
lpy.df_ref()
lpy.ann_low_high()
lpy.sum_low_high()

# Plotting line graph
years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
highs = [
    131.15,
    128.32,
    129.51,
    146.82,
    194.45,
    183.21,
    193.30,
    193.18,
    257.71,
    418.45,
    458.75,
]
lows = [
    106.26,
    109.37,
    111.06,
    119.54,
    136.12,
    157.13,
    150.57,
    168.19,
    183.78,
    242.05,
    396.25,
]

plt.plot(years, highs, label="High Prices", marker="D")
plt.plot(years, lows, label="Low Prices", marker="D")
plt.xlabel("Year")
plt.ylabel("Price")
plt.title("Gold Yearly Highs and Lows")
plt.legend(loc="lower center", bbox_to_anchor=(1.5, -0.2), ncol=2)
plt.show()


# Plotting bar chart
years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
highs = [
    131.15,
    128.32,
    129.51,
    146.82,
    194.45,
    183.21,
    193.30,
    193.18,
    257.71,
    418.45,
    458.75,
]
lows = [
    106.26,
    109.37,
    111.06,
    119.54,
    136.12,
    157.13,
    150.57,
    168.19,
    183.78,
    242.05,
    396.25,
]

width = 0.35  # width of the bars

# Create bars side by side
plt.bar(
    [y - width / 2 for y in years],
    highs,
    width=width,
    label="High Prices",
    color="skyblue",
)
plt.bar(
    [y + width / 2 for y in years], lows, width=width, label="Low Prices", color="blue"
)

# Add mean lines
plt.axhline(sum(highs) / len(highs), color="blue", linestyle="--", label="Mean High")
plt.axhline(sum(lows) / len(lows), color="gray", linestyle="--", label="Mean Low")

plt.xlabel("Year")
plt.ylabel("Price")
plt.title("Gold Yearly Highs and Lows")
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=4)
plt.show()
