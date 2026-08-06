import pandas as pd

df = pd.read_csv("Chocolate_Sales.csv")

df["Amount"] = df["Amount"].replace(r"[\$,]", "", regex=True).astype(float)
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

top5 = df.groupby("Product").agg(
    liczba_produktow=("Product", "count"),
    srednia_wartosc_zamowienia=("Amount", "mean")
).sort_values("liczba_produktow", ascending=False).head(5)

miesieczne_sumy = df.groupby(df["Date"].dt.to_period("M")).agg(
    suma=("Amount", "sum")
)

top5.to_csv("raport.csv")

