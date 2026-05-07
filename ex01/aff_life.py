from load_csv import load
import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = load("/Users/robincanavaggio/Documents/"
              "GitHub/Ecole/PostCC/Piscine Python/Python02/ex01/"
              "life_expectancy_years.csv")
    if df is None:
        return

    if "country" not in df.columns:
        print("Error: missing 'country' column")
        return
    country_df = df[df['country'] == 'Germany']
    if country_df.empty:
        print("Error: country not found")
        return

    row = country_df.iloc[0]
    series = row.iloc[1:]

    series = series.apply(pd.to_numeric, errors="coerce").dropna()
    if series.empty:
        print("Error: no numeric year data to plot")
        return

    series.plot(kind='line', title='Germany Life expectancy Projections')
    plt.xlabel('Year')
    plt.ylabel('Life expectancy')

    plt.show()


if __name__ == "__main__":
    main()
