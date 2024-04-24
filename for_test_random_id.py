import random
import matplotlib.pyplot as plt

# 定义参数
mean_lognormal_food_consumption_monthly = 1
std_deviation = 0.2

# 生成对数正态分布的随机数据
data = [random.lognormvariate(mean_lognormal_food_consumption_monthly, std_deviation) for _ in range(1000)]
data = [7 * x for x in data]
print(sum(data) / len(data))

salary = 100
print(random.lognormvariate(mean_lognormal_food_consumption_monthly, std_deviation) * salary / 12)

# 绘制直方图
plt.hist(data, bins=30, density=True, alpha=0.75, color='b')

# 添加标题和标签
plt.title('Food Consumption Distribution')
plt.xlabel('Food Consumption')
plt.ylabel('Frequency')

# 显示图形
plt.show()
