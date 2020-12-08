import json
import pandas as pd
f = pd.read_csv("US_Top200_10-10-2020.csv")
print(f.columns)
"""
for i in range(1,201):
    try:
        print(str(i) + ": ", end='')
        print(dictionary[str(i)]['name'], end='')
        print(" by ", end='')
        print(dictionary[str(i)]['artist'])
    except KeyError:
        print(str(i) + " Error")
"""
#print(f)
def xy(csv):
    x = f["Artist"]
    plot =f.groupby("Streams")["Artist"].sum().plot(kind = "pie", figsize=(5, 5), cmap="rainbow_r")
    print(x)
xy(f)