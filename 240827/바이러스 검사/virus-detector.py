import math

n = int(input())

cust = list(map(int, input().split()))
leader, member = map(int, input().split())

cust.sort(reverse=True)

result = 0
for i, c in enumerate(cust):
    c -= leader
    result += 1
    result += math.ceil(c / member)

print(result)