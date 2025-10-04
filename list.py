L1 = [1, 2, 2, 3, 2, 3, 4, 5]

most_repetitive = L1[0]
max_count = 0

for item in L1:
    count = L1.count(item)
    if count > max_count:
        max_count = count
        most_repetitive = item

print("The most repetitive element is:", most_repetitive)