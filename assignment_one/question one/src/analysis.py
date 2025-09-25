import pandas as pd
import numpy as np

# Read in the clean data using pandas
clean_yield_data = pd.read_csv('../data_clean/clean_yield_data.csv')

# Change binary columns type to int8
df = clean_yield_data.copy()
df["Frailty"] = df["Frailty"].astype("int8")
df["AgeGroup_<30"] = df["AgeGroup_<30"].astype("int8")
df["AgeGroup_30–45"] = df["AgeGroup_30–45"].astype("int8")
df["AgeGroup_46–60"] = df["AgeGroup_46–60"].astype("int8")
df["AgeGroup_>60"] = df["AgeGroup_>60"].astype("int8")

# Compute summary table and write it to disk
summary = df.describe(exclude=np.int8).loc[["mean", "50%", "std"]]  # Exclude int8 because we use it as binary in our case
summary.rename(index={"50%": "median"}, inplace=True)  # Rename 50% to median
summary.to_markdown("../reports/findings.md") # Write summary to disk as md file

# Compute correlation between Grip and Frailty and report it
grip_fraitly_corr=str(df["Grip strength"].corr(df["Frailty"]))

print(summary)
print("Correlation between Grip_kg and Frailty_binary is: " + str(grip_fraitly_corr))