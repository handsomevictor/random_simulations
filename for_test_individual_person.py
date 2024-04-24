import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from simulation_rich_and_poor.params import SinglePerson
from simulation_rich_and_poor.tool_functions import generate_random_family_ID


def generate_single_person_history(random_family_ID, num_iterations):
    random_person = SinglePerson(random_family_ID)
    random_person.set_initial_params()
    random_person.write_to_individual_database()

    for i in range(num_iterations):
        random_person.update_next_month_behavior()
        random_person.write_to_individual_database()


def read_single_person_history(family_id):
    columns = ['family_id', 'current_year', 'current_month', 'sex', 'age', 'age_month', 'life_expectancy', 'dead',
               'occupation',
               'already_married', 'entrepreneurship', 'successful_entrepreneur', 'life_insurance', 'body_condition',
               'monthly_health_cost', 'baby_cost', 'initial_monthly_income', 'current_period_income',
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
    # filter out dead people
    final_df = final_df[final_df['dead'] == 0]

    final_df.to_csv(os.path.join('tmp_database', 'population_individual_database', family_id, 'all_history.csv'),
                    index=False)
    return final_df


def plot_single_person_history(family_id):
    df = read_single_person_history(family_id)
    # plot line chart on total_saving
    # x axis is 1,2...months
    plt.plot(range(len(df)), df['total_saving'])
    plt.xlabel('Months')
    plt.ylabel('Total Saving')
    plt.title('Total Saving over time')
    plt.show()


if __name__ == "__main__":
    random_family_ID = generate_random_family_ID()
    generate_single_person_history(random_family_ID, 1000)

    plot_single_person_history(random_family_ID)
