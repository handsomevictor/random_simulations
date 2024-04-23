import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

from simulation_rich_and_poor.params import SinglePersonParams


# generate 1000 people of single person
def generate_one_person(_):
    single_person = SinglePersonParams()
    # remove people that age > life_expectancy
    while single_person.dead:
        single_person = SinglePersonParams()

    # save detail to tmp_database as csv file
    tmp_df = pd.DataFrame({
        "age": single_person.age,
        "life_expectancy": single_person.life_expectancy,
        "occupation": single_person.occupation,
        "body_condition": single_person.body_condition,
        "monthly_health_cost": single_person.monthly_health_cost,
        "initial_monthly_income": single_person.initial_monthly_income,
        "food_consumption_monthly_value": single_person.food_consumption_monthly_value,
        "other_consumption_monthly_value": single_person.other_consumption_monthly_value,
        "initial_saving": single_person.initial_saving,
        "retirement_payment": single_person.retirement_payment,
        "jobless_subsidy": single_person.jobless_subsidy,
        "birth_willingness": single_person.birth_willingness,
        "salary_yearly_increase_rate": single_person.salary_yearly_increase_rate,
        "entrepreneurship": single_person.entrepreneurship,
        "entrepreneurship_successful": single_person.successful_entrepreneur
    }, index=[0])
    tmp_df.to_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data.csv'), mode='a', header=False, index=False)


def generate_people(num_people, max_workers=None):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        people = list(tqdm(executor.map(generate_one_person, range(num_people)), total=num_people))

    people_df = pd.read_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data.csv'))
    people_df.columns = ["age", "life_expectancy", "occupation", "body_condition", "monthly_health_cost",
                         "initial_monthly_income", "food_consumption_monthly_value", "other_consumption_monthly_value",
                         "initial_saving", "retirement_payment", "jobless_subsidy", "birth_willingness",
                         "salary_yearly_increase_rate", "entrepreneurship", "entrepreneurship_successful"]
    # sort by age
    people_df = people_df.sort_values(by='age')
    people_df.to_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data.csv'), index=False)

    # sort by initial_saving
    people_df = people_df.sort_values(by='initial_saving', ascending=False)
    people_df.head(1000).to_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data_initial_saving.csv'), index=False)

    # sort by entrepreneurship
    people_df = people_df.sort_values(by='entrepreneurship', ascending=False)
    people_df.head(1000).to_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data_entrepreneurship.csv'), index=False)

    # sort by entrepreneurship_successful
    people_df = people_df.sort_values(by=['entrepreneurship', 'entrepreneurship_successful'], ascending=False)
    people_df.head(1000).to_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data_entrepreneurship_successful.csv'),
                                index=False)
    return people


def plot_distribution(column_name):
    people_df = pd.read_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data.csv'))
    # plot the distribution of age
    plt.figure(figsize=(12, 6))
    plt.hist(people_df[column_name], bins=30, color='blue', alpha=0.5, label='年龄分布')
    plt.xlabel('initial_saving')
    plt.ylabel('人数')
    plt.title('年龄分布')
    plt.legend()
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.show()


def plot_distribution_3d():
    people_df = pd.read_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data.csv'))
    initial_saving = people_df['initial_saving']
    age = people_df['age']
    count = len(initial_saving)

    # 创建一个三维图形对象
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')

    # 绘制三维柱状图
    hist, xedges, yedges = np.histogram2d(initial_saving, age, bins=20)
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0
    dx = dy = 8 * np.ones_like(zpos)  # 增加柱子的宽度
    dz = hist.ravel()
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average', alpha=0.5)

    # 设置图形标题和标签
    ax.set_xlabel('Initial Saving')
    ax.set_ylabel('Age')
    ax.set_zlabel('Count')
    ax.set_title('Initial Saving and Age Distribution')

    # 显示图形
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.show()


if __name__ == "__main__":
    # remove the file
    try:
        os.remove(os.path.join(os.getcwd(), 'tmp_database', 'test_data.csv'))
    except FileNotFoundError:
        pass

    generate_people(100000, max_workers=None)
    # print("Done!")
    #
    # plot_distribution_3d()
    plot_distribution(column_name='age')
