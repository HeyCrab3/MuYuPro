from db import data_import
result = int(input("你确认要初始化数据库吗？这个操作是不可逆的！0取消，1确认"))
if result == 0:
    exit(1)
else:
    data_import()
    print('成功！')
