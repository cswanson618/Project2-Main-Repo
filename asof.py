import datetime

asof = input("YYYY-MM-DD")
entry = datetime.datetime.strptime(asof, "%Y-%m-%d")
print(entry)
