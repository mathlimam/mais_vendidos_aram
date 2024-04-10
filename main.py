import pandas as pd


dataframe = pd.read_excel("database.xlsx")

new_df = dataframe.groupby("PRODUTO")['QUANTIDADE'].sum()

new_df = pd.merge(new_df, dataframe, on="PRODUTO")
new_df = new_df.drop_duplicates(subset="PRODUTO")
new_df = new_df.drop("QUANTIDADE_y", axis=1)
new_df["FATURAMENTO TOTAL"] = new_df["QUANTIDADE_x"] * new_df["PREÇO"]

new_df.to_excel("sales_db.xlsx")