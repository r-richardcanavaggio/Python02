from load_csv import load
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


def convert_pop(value)-> float:
    """Converts a string rep into a float"""
    if pd.isna(value):
        return None
    
    value = str(value).upper().strip()

    if 'M' in value:
        return float(value.replace('M', '')) * 10**6
    elif 'B' in value:
        return float(value.replace('B', '')) * 10**9
    elif 'k' in value:
        return float(value.replace('K', '')) * 10**3
    else:
        return float(value)


def format_kmb(x, pos):
    if x >= 1e9:
        return f'{x*1e-9:g}B'
    elif x >= 1e6:
        return f'{x*1e-6:g}M'
    elif x >= 1e3:
        return f'{x*1e-3:g}K'
    else:
        return float(x)


def main():
    df = load("population_total.csv")
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
    print(type(row))
    series = row.iloc[1:252]
    series = series.apply(convert_pop)
    print(row)

    print(series)
    series = series.apply(pd.to_numeric, errors="coerce").dropna()
    if series.empty:
        print("Error: no numeric year data to plot")
        return

    series.plot(kind='line', title='Germany Population Projections')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_kmb))
    plt.xlabel('Year')
    plt.ylabel('Population')

    plt.show()


if __name__ == "__main__":
    main()
