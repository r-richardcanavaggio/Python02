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
    """Program that plots gdp against life expectancy for a given year"""
    life_expec_df = load("life_expectancy_years.csv")
    income_df = load(
        "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    )
    if life_expec_df is None or income_df is None:
        return

    try:
        annee = '1900'
        df_life_1900 = life_expec_df[['country', annee]]
        df_income_1900 = income_df[['country', annee]]

        df_final = pd.merge(df_life_1900, df_income_1900,
                            on='country', suffixes=('_life_expec', '_income'))
        column_gdp = f'{annee}_income'
        df_final[column_gdp] = df_final[column_gdp].apply(convert_pop)
        df_final = df_final.dropna()

        fig, ax = plt.subplots()

        df_final.plot(
            ax=ax,
            kind='scatter',
            x=column_gdp,
            y=f'{annee}_life_expec',
            title='1900'
        )
        plt.xlabel('Gross domestic product')
        plt.ylabel('Life expectancy')
        ax.set_xscale('log')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_kmb))

        plt.show()

    except KeyError:
        print("Error: column 'country' or '1900' not found in CSV file.")
    except Exception as e:
        print(f"Unexepected error : {e}")


if __name__ == "__main__":
    main()
