# 國泰銀行要慶祝六十周年，需要買字母貼紙來布置活動空間，
# 文字為"Hello welcome to Cathay 60th year anniversary"，
# 請寫一個程式計算每個字母(大小寫視為同個字母)出現次數
# 輸出：
# 0 1
# 6 1
# A 4
# C 2
# E 5
# H 3
# ....(繼續印下去)

# 目標字串
text = "Hello welcome to Cathay 60th year anniversary"

# 初始化一個字典來存儲字母和數字出現的次數
count_dict = {}

# 遍歷每個字符
for char in text:
    # 只處理字母和數字
    if char.isalnum():  # 包含字母和數字
        char = char.upper()  # 將字母轉為大寫
        if char in count_dict:
            count_dict[char] += 1  # 若字母或數字已經在字典中，則次數加 1
        else:
            count_dict[char] = 1   # 若字母或數字不在字典中，則初始化為 1

# 按照字母和數字順序排序並輸出結果
for char in sorted(count_dict.keys()):
    print(f"{char} {count_dict[char]}")
