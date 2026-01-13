import csv

def u():
    with open("/home/morsdesuper/Documents/joseh/Joseh/update_t_data.csv", newline="") as f: 
        return list(csv.DictReader(f))

rows = u()
for row in rows:
    print(row.keys())
    break
