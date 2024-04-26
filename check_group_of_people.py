import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from itertools import repeat

from simulation_rich_and_poor.params import SinglePerson
from simulation_rich_and_poor.tool_functions import generate_random_family_ID


def generate_single_person_history(num_iterations):
    random_family_ID = generate_random_family_ID()
    random_person = SinglePerson(random_family_ID, age=1, life_expectancy=100, age_month=1, preset_params=True,
                                 entrepreneurship=None, successful_entrepreneur=None)
    random_person.set_initial_params()
    random_person.write_to_individual_database()

    for i in range(num_iterations):
        random_person.update_next_month_behavior()
        random_person.write_to_individual_database()


def generate_group_of_people_history(num_people, num_iterations):
    # use ThreadPoolExecutor
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     # use tqdm
    #     list(tqdm(executor.map(generate_single_person_history, repeat(num_iterations)), total=num_people))

    # use for loop - somehow for loop is much much faster than ThreadPoolExecutor
    for i in tqdm(range(num_people)):
        generate_single_person_history(num_iterations)


def save_single_person_total_saving(family_id):
    columns = ['family_id', 'current_year', 'current_month', 'sex', 'age', 'age_month', 'life_expectancy', 'dead',
               'occupation',
               'already_married', 'entrepreneurship', 'successful_entrepreneur', 'life_insurance', 'body_condition',
               'monthly_health_cost', 'baby_cost', 'initial_monthly_income', 'current_period_income',
               "highest_salary_ever",
               'last_period_employee_income', 'food_consumption_monthly_value', 'other_consumption_monthly_value',
               'initial_saving', "monthly_saving", 'total_saving', 'retirement_monthly_payment', 'jobless_subsidy',
               'birth_willingness',
               'num_of_children', 'salary_yearly_increase_rate']

    # use os.walk
    final_df = pd.DataFrame(columns=columns)
    for root, dirs, files in os.walk(os.path.join('tmp_database', 'population_individual_database', family_id)):
        for file in files:
            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(root, file), header=0)
                # concat vertically
                final_df = pd.concat([final_df, df], axis=0)

    # sort by current_date
    final_df = final_df.sort_values(by=['current_year', 'current_month'], ascending=True)
    final_df.to_csv(os.path.join('tmp_database', 'population_individual_database', family_id, 'all_history.csv'),
                    index=False)
    # return final_df['total_saving']


def plot_all_people_total_saving(family_id_list):
    plt.figure(figsize=(12, 6))
    for family_id in tqdm(family_id_list):
        df = pd.read_csv(os.path.join('tmp_database', 'population_individual_database', family_id, 'all_history.csv'))
        total_saving_list = df['total_saving']
        plt.plot([i/12 for i in range(len(total_saving_list))], total_saving_list)
    plt.xlabel('Age')
    plt.ylabel('Total Saving')
    plt.title('Total Saving over time')
    plt.show()


def plot_total_saving_distribution(family_id_list):
    plt.figure(figsize=(12, 6))
    last_total_saving_list = []
    for family_id in tqdm(family_id_list):
        df = pd.read_csv(os.path.join('tmp_database', 'population_individual_database', family_id, 'all_history.csv'))
        # only select the last row
        total_saving_last = df['total_saving'].values[-12 * 30]
        last_total_saving_list.append(total_saving_last)
    plt.hist(last_total_saving_list, bins=100, color='blue', alpha=0.5, label='Total Saving Distribution')
    plt.xlabel('Total Saving')
    plt.ylabel('Number of People')
    plt.title('Total Saving Distribution')
    # plt.legend()
    plt.show()


if __name__ == '__main__':
    # generate_group_of_people_history(num_people=300, num_iterations=100 * 12)

    family_id_list = os.listdir(os.path.join('tmp_database', 'population_individual_database'))
    family_id_list = [i for i in family_id_list if len(i) == 24]

    # use concurrent
    # with ProcessPoolExecutor(max_workers=4) as executor:
    #     list(tqdm(executor.map(save_single_person_total_saving, family_id_list), total=len(family_id_list)))

    # plot_all_people_total_saving(family_id_list)
    plot_total_saving_distribution(family_id_list)