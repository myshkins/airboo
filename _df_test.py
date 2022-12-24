import pandas as pd

df1 = pd.DataFrame(
    {
        "name": ["bob", "alice", "joe", "jane"],
        "p1": [12, 14, 15, 10],
        "q1": [2, 4, 5, 8],
    }
)

df2 = pd.DataFrame(
    {
        "name": ["bob", "alice", "joe"],
        "p2": [13, 15, 16],
        "q1": [2, 4, 5],
    }
)

print(df1)
print("")
print(df2)
print("")
merged = pd.merge(df1, df2, how="outer", on=["name", "q1"])
print(merged)