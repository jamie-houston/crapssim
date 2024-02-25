import pandas
import matplotlib.pyplot as plt

# Prepare data frame from csv
data = pandas.read_csv("data.csv")
df = pandas.DataFrame(data)

# Set a frame of reference for analyzing the data
columns = df.columns
sims = df.loc[(df["Sim Number"] == 0)]
num_sims = len(sims)
sim_names = sims["Strategy"]

# Convert data types
df["Sim Number"] = df["Sim Number"].astype(int)
df["End Bankroll"] = df["End Bankroll"].astype(float)
df["Start Bankroll"] = df["Start Bankroll"].astype(float)
df["Dice Rolls"] = df["Dice Rolls"].astype(int)
df["Difference"] = df["Difference"].astype(float)
df["Dollar/Roll"] = df["Dollar/Roll"].astype(float)

boxplot = df.boxplot(column="Difference", by="Strategy")

box2 = df.boxplot(column="Dollar/Roll", by="Strategy")

plt.show()