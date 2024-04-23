"""
In my society, averagely people make around 100 per month.
"""

import random
import numpy as np


class EvolutionParams:
    current_year = 1
    current_month = 1

class GeneralParams:
    average_monthly_payment = 100
    average_life_expectancy = 80

class SocietyParams:
    # --------------- Initial Population ---------------
    initial_population = 100000

    # --------------- Death Rate ---------------
    death_rate_healthy = 0.01
    death_rate_sick = 0.05
    death_rate_disabled = 0.1

    # --------------- Unemployment Rate ---------------
    unemployment_rate = 0.05

    # --------------- Inflation Rate ---------------
    inflation_rate_yearly = 0.05

    # --------------- Health Macro ---------------
    health_macro = {
        "healthy_rate": 0.7,
        "sick_rate": 0.15,
        "disabled_rate": 0.15
    }

    # --------------- Lowest Monthly Income ---------------
    # 30% of the average monthly payment
    lowest_monthly_income = 0.3 * GeneralParams.average_monthly_payment

    # --------------- Average Salary Increase Rate ---------------
    salary_yearly_increase_rate = 0.1  # an average value, for individuals, it should be different


    # --------------- Birth Rate ---------------



class SinglePersonParams:
    """
    Single person parameters:
    - age
    - life_expectancy
    - occupation
    - body_condition
    """

    # --------------- Age ---------------
    # There are 3 types of aging society: young, middle-aged, and aged
    age = np.round(np.random.gamma(shape=4, scale=10, size=SocietyParams.initial_population))

    # --------------- Life Expectancy ---------------
    life_expectancy = np.round(random.gauss(80, 20))

    # --------------- Occupation ---------------
    @staticmethod
    def occupation(age):
        if age < 6:
            return "baby"
        if age < 18:
            return "student"
        if age < 65:
            if random.random() < SocietyParams.unemployment_rate:
                return "unemployed"
            else:
                return "employed"
        else:
            return "retired"
    occupation = occupation(age)

    # --------------- Life Insurance ---------------
    @staticmethod
    def life_insurance(occupation):
        if occupation == "employed":
            return 35
        if occupation == "retired":
            return 18
        else:
            return 10
    life_insurance = life_insurance(occupation)

    # --------------- Body Condition ---------------
    @staticmethod
    def body_condition():
        # random number between 0 and 1, linearly distributed
        random_number = random.random()
        if random_number <= SocietyParams.health_macro["healthy_rate"]:
            return "healthy"
        if random_number <= SocietyParams.health_macro["healthy_rate"] + SocietyParams.health_macro["sick_rate"]:
            return "sick"
        else:
            return "disabled"
    body_condition = body_condition()

    # --------------- Health Cost ---------------
    @staticmethod
    def monthly_health_cost(body_condition):
        # Without life insurance
        if body_condition == "healthy":
            return 5
        if body_condition == "sick":
            return 50
        if body_condition == "disabled":
            return 25
    monthly_health_cost = monthly_health_cost(body_condition) - life_insurance

    # --------------- Initial Monthly Income ---------------
    @staticmethod
    def initial_monthly_income(occupation):
        if occupation == "unemployed":
            return SinglePersonParams.jobless_subsidy
        if occupation == "employed":
            return max(random.gauss(100, 60), SocietyParams.lowest_monthly_income)
        if occupation == "retired":
            return 0
    initial_monthly_income = initial_monthly_income(occupation)

    # --------------- Average Consumption Rate based on Salary ---------------
    @staticmethod
    def food_consumption_monthly_value(initial_monthly_income):
        if initial_monthly_income == 0:
            return 20
        if initial_monthly_income < 50:
            return 0.5 * initial_monthly_income
        if initial_monthly_income < 100:
            return 0.4 * initial_monthly_income
        if initial_monthly_income < 200:
            return 0.35 * initial_monthly_income
        if initial_monthly_income < 500:
            return 0.3 * initial_monthly_income
        if initial_monthly_income < 1000:
            return 0.25 * initial_monthly_income
        else:
            return 0.2 * initial_monthly_income
    food_consumption_monthly_value = food_consumption_monthly_value(initial_monthly_income)

    @staticmethod
    def other_consumption_monthly_value(initial_monthly_income):
        if initial_monthly_income == 0:
            return 0
        if initial_monthly_income < 50:
            return 0.5 * initial_monthly_income
        if initial_monthly_income < 100:
            return 0.4 * initial_monthly_income
        if initial_monthly_income < 200:
            return 0.35 * initial_monthly_income
        if initial_monthly_income < 500:
            return 0.3 * initial_monthly_income
        if initial_monthly_income < 1000:
            return 0.25 * initial_monthly_income
        else:
            return 0.2 * initial_monthly_income
    other_consumption_monthly_value = other_consumption_monthly_value(initial_monthly_income)

    # --------------- Savings ---------------
    @staticmethod
    def initial_saving(age):
        if age < 18:
            return 0
        occupation = SinglePersonParams.occupation(age)
        all_monthly_costs = (SinglePersonParams.monthly_health_cost +
                             SinglePersonParams.food_consumption_monthly_value +
                             SinglePersonParams.other_consumption_monthly_value)
        if occupation == "unemployed":
            return 12 * ((age - 18) * np.round(random.gauss(100, 50)) - all_monthly_costs)
        if occupation == "employed":
            return 12 * ((age - 18) * 12 * np.round(random.gauss(200, 100)) - all_monthly_costs)
        if occupation == "retired":
            return 12 * ((age - 65) * 12 * np.round(random.gauss(150, 100)) - all_monthly_costs)
    initial_saving = initial_saving(age)

    # --------------- Retirement Payment ---------------
    # Should be 70% of the income for the last 20 years
    retirement_payment = 0  # to be calculated

    # --------------- Jobless Subsidy ---------------
    # Should be 70% of lowest income
    jobless_subsidy = 0.7 * SocietyParams.lowest_monthly_income




def SinglePersonBehavior(SinglePersonParams):
    """
    Single person behavior:
    - consume
    - save
    - die
    - give birth
    - get sick
    - get disabled
    - get employed
    - get retired
    """

    # --------------- Consume ---------------
    food_consumption_monthly_value = SinglePersonParams.other_consumption_monthly_value(initial_monthly_income)


if __name__ == "__main__":
    print(parameters())