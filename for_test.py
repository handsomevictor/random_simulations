import random
import numpy as np
import matplotlib.pyplot as plt

# 老龄化社会
def generate_age_aging(num_samples):
    return np.round(np.random.gamma(shape=1, scale=20, size=num_samples))

def generate_age_youthful(num_samples):
    return np.round(np.random.gamma(shape=3, scale=10, size=num_samples))

# 中等社会
def generate_age_balanced(num_samples):
    return np.random.uniform(low=0, high=100, size=num_samples)

# 生成 1000 个样本来展示不同类型的年龄分布
num_samples = 100000

aging_ages = generate_age_aging(num_samples)
youthful_ages = generate_age_youthful(num_samples)
balanced_ages = generate_age_balanced(num_samples)
# print mean
print(np.mean(aging_ages))
print(np.mean(youthful_ages))
print(len(aging_ages))
print(len(youthful_ages))

# 绘制直方图
plt.figure(figsize=(12, 6))
plt.hist(aging_ages, bins=300, color='blue', alpha=0.5, label='老龄化社会')
plt.hist(youthful_ages, bins=300, color='red', alpha=0.5, label='年轻化社会')
# plt.hist(balanced_ages, bins=300, color='green', alpha=0.5, label='中等社会')
plt.xlabel('年龄')
plt.ylabel('人数')
plt.title('不同社会形态的年龄分布')
plt.legend()
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

plt.show()
