lst = [109, 101, 100, 105, 117, 109, 46, 99, 111, 109]

# Using list comprehension and join
res = ''.join(chr(i) for i in lst)

print (str(res))
