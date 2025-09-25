import pandas as pd

pd.options.display.max_columns = None
pd.options.display.expand_frame_repr =False

# Read in the raw data using pandas

raw_yield_data = pd.read_csv('../data_raw/raw_yield_data.csv')

# Unit standardization
df=raw_yield_data.assign(
    Height = raw_yield_data["Height"] * 0.0254,  # Convert height from in to m Height_m = Height_in * 0.0254
    Weight = raw_yield_data["Weight"] * 0.45359237,  # Convert weight from lb to kg Weight_kg = Weight_lb * 0.45359237
    Frailty = raw_yield_data["Frailty"].map({"Y": 1, "N": 0}).astype("int8"), # Convert Frailty from object to int8
)

# Calculate BMI and add it to the dataframe
df["BMI"]=(df["Weight"] / (df["Height"] ** 2)).round(2)

# Categories age 
df["Age Group"] = pd.cut(df["Age"], bins=[0,30,45,60,float("inf")], labels=["<30","30–45","46–60",">60"], right=False)

# One‑hot encode AgeGroup
df = pd.get_dummies(df, columns=["Age Group"], prefix="AgeGroup", dtype="int8")

# Write clean dataframe to disk
df.to_csv('../data_clean/clean_yield_data.csv',index=False)

print(df.head(10))

