#from jieba_analysis import *
import jieba_analysis as JBL
## 得到最终的研报提取结果 ##

# 处理的研报指定的目录 #
file_directory = "research_paper"

# 停用词相对路径
stopwords_directory = "add_vocabulary/stopwords.txt"

trend_directory = "add_vocabulary/trend_term.txt"
# 设置的 最多提取的结论 从每篇研报中 #
top_number = 10
# 提取的词 在原文中至少出现过的次数 #
Counts = 2
JBL.obtain_conclusion(file_directory, top_number, Counts,stopwords_directory)