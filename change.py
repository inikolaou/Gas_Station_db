import pandas as pd
df = pd.read_csv("Datasets/purchase.csv")
li = []
for date in df['Purchase_Date']:
    numbers = date.split('/')
    if (len(numbers[0]) == 1):
        if (len(numbers[1]) == 1):
            day = '0' + numbers[0]
            month = '0' + numbers[1]
        else:
            day = '0' + numbers[0]
            month = numbers[1]
    else:
        if (len(numbers[1]) == 1):
            day = numbers[0]
            month = '0' + numbers[1]
        else:
            day = numbers[0]
            month = numbers[1]
    correct_date = '/'.join([day, month, numbers[2]])
    li.append(correct_date)
df['Purchase_Date'] = li
df.to_csv("Datasets/purchase.csv", index=False)