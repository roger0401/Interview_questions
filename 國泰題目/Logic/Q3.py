# QA部門今天舉辦團康活動，有n個人圍成一圈，順序排號。
# 從第一個人開始報數（從1到3報數），凡報到3的人退出圈子。
# 請利用一段程式計算出，最後留下的那位同事，是所有同事裡面的第幾順位?
# 輸入：n值(0-100)
# 輸出：第幾順位

def find_last_person(n, step=3):
    people = list(range(1, n + 1))  # 建立人員列表 (從 1 到 n)
    index = 0  # 初始索引位置
    
    step -= 1  # 因為索引是從 0 開始，所以要減 1 才能對應正確的位置，這題為數到三

    while len(people) > 1:
        index = (index + step) % len(people)  # 計算要刪除的索引
        # removed_person = people[index]  # 取得即將被刪除的人
        people.pop(index)  # 刪除該人
        # print(f'被淘汰的人: {removed_person}, 剩餘人員: {people}, 當前 index: {index}')
    
    return people[0]  # 返回最後剩下的人

# 測試
n = int(input("請輸入人數 n (0-100): "))
if n == 0:
    print("沒有任何人參加")
else:
    last_person = find_last_person(n, step=3)  # 這裡的 step=3 表示「數 3 下刪 1 人」
    print(f"最後留下的同事是第 {last_person} 順位")