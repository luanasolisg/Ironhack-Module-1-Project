from Adquisition import adquisition
from cleaning_final import cleaning


def main():
    df = adquisition(df)
    df_clean = cleaning(df)
    print(df)

if __name__ == '__main__':
    main()
