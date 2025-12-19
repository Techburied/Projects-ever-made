import pandas as pd
a = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
# a.index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
a.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k','l'])
print(a)