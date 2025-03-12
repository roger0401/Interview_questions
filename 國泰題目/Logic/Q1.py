# 國泰補習班中，有五位學生期中考的成績分別為[53, 64, 75, 19, 92]，但是老師在輸入成績的時候看反了，
# 把五位學生的成績改成了[35, 46, 57, 91, 29]，
# 請用一個函數來將學生的成績修正。
# 輸入: [35, 46, 57, 91, 29]
# 輸出: [53, 64, 75, 19, 92]

def reverse_scores(scores):
    """
    函數接收一個包含數字的列表，並將每個數字的數字位順序反轉後返回新列表。
    參數:
        scores (list): 包含數字的列表，每個數字的位數可能是 2 位或更多。
    返回:
        list: 所有數字都被反轉後的新列表。
    """
    # 使用列表推導式（List Comprehension）來處理每個數字
    return [int(str(num)[::-1]) for num in scores]

# 測試範例
wrong_scores = [35, 46, 57, 91, 29]  # 老師輸入錯誤的分數
corrected_scores = reverse_scores(wrong_scores)  # 呼叫函數進行修正

# 印出修正後的成績
print(corrected_scores)  
