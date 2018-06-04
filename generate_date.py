# 生成日期txt 文件 #
import datetime
import time

Date=['年','月','日']
today=datetime.date.today()

print('此刻日期为%d年%d月%d日'%(today.year,today.month,today.day))
year=today.year
month=today.month
day=today.day

month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
Month_days=[31,29,31,30,31,30,31,31,30,31,30,31]

oldest_year=1900
total_collection_date=[]
collection_date=[]

datetext='usrdic/date_collection.txt'
f=open(datetext,'w',encoding='utf-8')

for i_year in range(oldest_year,year+1):
    if i_year!=year:
        if year%4==0:
            for i_month in range(1,12+1):
                collection_date.append(str(i_year)+'年'+str(i_month)+'月')
                f.write(str(i_year)+'年'+str(i_month)+'月'+'\n')
                for i_day in range(1,month_days[i_month-1]+1):
                    f.write(str(i_year)+'年'+str(i_month)+'月'+str(i_day)+'日'+'\n')
                    total_collection_date.append(str(i_year)+'年'+str(i_month)+'月'+str(i_day)+'日')
        else:
            for i_month in range(1,12+1):
                collection_date.append(str(i_year)+'年'+str(i_month)+'月')
                f.write(str(i_year)+'年'+str(i_month)+'月'+'\n')
                for i_day in range(1,Month_days[i_month-1]+1):
                    f.write(str(i_year)+'年'+str(i_month)+'月'+str(i_day)+'日'+'\n')
                    total_collection_date.append(str(i_year)+'年'+str(i_month)+'月'+str(i_day)+'日')
    else:
        if year % 4 == 0:
            for i_month in range(1, month + 1):
                collection_date.append(str(year) + '年' + str(i_month) + '月')
                f.write(str(i_year) + '年' + str(i_month) + '月' + '\n')
                for i_day in range(1, month_days[i_month - 1] + 1):
                    f.write(str(i_year) + '年' + str(i_month) + '月' + str(i_day) + '日' + '\n')
                    total_collection_date.append(str(year) + '年' + str(i_month) + '月' + str(i_day) + '日')
        else:

            for i_month in range(1, month + 1):
                f.write(str(i_year) + '年' + str(i_month) + '月'  + '\n')
                collection_date.append(str(year) + '年' + str(i_month) + '月')
                for i_day in range(1, Month_days[i_month - 1] + 1):
                    f.write(str(i_year) + '年' + str(i_month) + '月' + str(i_day) + '日' + '\n')
                    total_collection_date.append(str(year) + '年' + str(i_month) + '月' + str(i_day) + '日')
f.close()

print(collection_date[::-1])
print(total_collection_date)











