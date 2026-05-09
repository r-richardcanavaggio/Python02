from load_csv import load
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


def convert_pop(value) -> float:
    """Converts a string rep into a float"""
    if pd.isna(value):
        return None

    value = str(value).upper().strip()

    try:
        if 'M' in value:
            return float(value.replace('M', '')) * 10**6
        elif 'B' in value:
            return float(value.replace('B', '')) * 10**9
        elif 'K' in value:
            return float(value.replace('K', '')) * 10**3
        else:
            return float(value)
    except ValueError:
        print(f"Error: corrupted value at {value}")
        return None


def format_kmb(x, pos):
    """Matplotlib custom function Formatter,
    takes a value and returns a string representation with K for thousands,
    M for millions, and B for billions"""
    if x >= 1e9:
        return f'{x*1e-9:g}B'
    elif x >= 1e6:
        return f'{x*1e-6:g}M'
    elif x >= 1e3:
        return f'{x*1e-3:g}K'
    else:
        return float(x)


def main():
    """Program that takes a population_total.csv file,
    and compares the values for China and Germany against each other"""
    df = load("population_total.csv")
    if df is None:
        return

    try:
        germany_df = df[df['country'] == 'Germany']
        china_df = df[df['country'] == 'China']

        china_row = china_df.iloc[0]
        ger_row = germany_df.iloc[0]

        china_series = china_row.iloc[1:251].apply(convert_pop)
        ger_series = ger_row.iloc[1:251].apply(convert_pop)

        new_df = pd.DataFrame({
            'China': china_series,
            'Germany': ger_series
        })

        new_df.index = new_df.index.astype(int)
        fig, ax = plt.subplots()

        new_df.plot(ax=ax, kind='line', title='Population Projections')

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_kmb))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(40))
        # ax.tick_params(axis='x', rotation=45)

        plt.xlabel('Year')
        plt.ylabel('Population')

        plt.show()

    except KeyError:
        print("Error: column 'country' not found in CSV file.")
    except IndexError:
        print("Error: China or Germany not found in array")
    except Exception as e:
        print(f"Unexepected error : {e}")


if __name__ == "__main__":
    main()
