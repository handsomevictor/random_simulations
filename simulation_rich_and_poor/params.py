"""
In my society, averagely people make around 100 per month.
"""

import random
import numpy as np


def occupation_func(age):
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


def birth_willingness_func(age):
    if age < 18:
        return 0.01
    if age < 23:
        return 0.25
    if age < 27:
        return 0.55
    if age < 30:
        return 0.70
    if age < 40:
        return 0.80
    else:
        return 0.81


def monthly_health_cost_func(body_condition):
    # Without life insurance
    if body_condition == "healthy":
        return - 5
    if body_condition == "sick":
        return - 50
    if body_condition == "disabled":
        return - 25
    else:
        return 0


def body_condition_func():
    # random number between 0 and 1, linearly distributed
    random_number = random.random()
    if random_number <= SocietyParams.health_macro["healthy_rate"]:
        return "healthy"
    if random_number <= SocietyParams.health_macro["healthy_rate"] + SocietyParams.health_macro["sick_rate"]:
        return "sick"
    else:
        return "disabled"


def initial_monthly_income_func(occupation, lowest_monthly_income):
    if occupation == "unemployed":
        return SinglePersonParams().jobless_subsidy
    if occupation == "employed":
        return np.round(max(random.gauss(100, 60), lowest_monthly_income), 4)
    if occupation == "retired":
        return 0
    else:
        return 0


def food_consumption_monthly_value_func(initial_monthly_income):
    # Later, change the ratio to normal distribution values with that value to be the mean
    if initial_monthly_income < 30:
        return 20
    if initial_monthly_income < 50:
        return np.round(0.5 * initial_monthly_income, 4)
    if initial_monthly_income < 100:
        return np.round(0.4 * initial_monthly_income, 4)
    if initial_monthly_income < 200:
        return np.round(0.35 * initial_monthly_income, 4)
    if initial_monthly_income < 500:
        return np.round(0.3 * initial_monthly_income, 4)
    if initial_monthly_income < 1000:
        return np.round(0.25 * initial_monthly_income, 4)
    else:
        return np.round(0.2 * initial_monthly_income, 4)


def other_consumption_monthly_value_func(initial_monthly_income):
    if initial_monthly_income == 0:
        return 0
    if initial_monthly_income < 50:
        return np.round(0.5 * initial_monthly_income, 4)
    if initial_monthly_income < 100:
        return np.round(0.4 * initial_monthly_income, 4)
    if initial_monthly_income < 200:
        return np.round(0.35 * initial_monthly_income, 4)
    if initial_monthly_income < 500:
        return np.round(0.3 * initial_monthly_income, 4)
    if initial_monthly_income < 1000:
        return np.round(0.25 * initial_monthly_income, 4)
    else:
        return np.round(0.2 * initial_monthly_income, 4)


def life_insurance_func(occupation):
    if occupation == "employed":
        return 35
    if occupation == "retired":
        return 18
    else:
        return 10


def salary_yearly_increase_rate_func(age, entrepreneurship):
    if not entrepreneurship:
        if age < 18:
            return 0
        if age < 23:
            return max(np.round(random.gauss(0.15, 0.05), 4), 0)
        if age < 28:
            return max(np.round(random.gauss(0.1, 0.05), 4), 0)
        if age < 40:
            return max(np.round(random.gauss(0.05, 0.05), 4), 0)
        if age < 65:
            return max(np.round(random.gauss(0.02, 0.01), 4), 0)
        else:
            return 0
    else:
        if age < 18:
            return max(np.round(random.gauss(1, 0.1), 4), 0)
        if age < 23:
            return max(np.round(random.gauss(1.5, 0.05), 4), 0)
        if age < 28:
            return max(np.round(random.gauss(2, 0.05), 4), 0)
        if age < 40:
            return max(np.round(random.gauss(0.8, 0.01), 4), 0)
        if age < 65:
            return max(np.round(random.gauss(0.5, 0.005), 4), 0)
        else:
            return 0


def entrepreneur_ratio_func(age):
    if age < 18:
        return 0
    if age < 23:
        return 0.05
    if age < 28:
        return 0.02
    if age < 40:
        return 0.01
    if age < 65:
        return 0.005
    else:
        return 0


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
    lowest_monthly_income = 0.3 * 100


class SinglePersonParams:
    """
    Single person parameters:
    - age
    - life_expectancy
    - occupation
    - body_condition
    """

    def __init__(self):
        # --------------- Sex ---------------
        self.sex = random.choice(['woman', 'man'])

        # --------------- Age ---------------
        age = np.round(np.random.gamma(shape=3, scale=12, size=1)[0])
        age = min(max(age, 1), 110)
        if age >= 100:
            # generate again
            age = np.round(np.random.gamma(shape=3, scale=11, size=1)[0])
            age = min(max(age, 1), 110)
        self.age = age

        # --------------- Life Expectancy ---------------
        self.life_expectancy = np.round(random.gauss(70, 10), 0)

        # if age larger than life expectancy, set this person to Dead and remove this person
        if self.age >= self.life_expectancy:
            self.dead = True
        else:
            self.dead = False

        # --------------- Occupation ---------------
        self.occupation = occupation_func(self.age)

        # --------------- Entrepreneurship ---------------
        self.entrepreneurship = True if random.random() < entrepreneur_ratio_func(self.age) else False

        # --------------- Life Insurance ---------------
        self.life_insurance = life_insurance_func(self.occupation)

        # --------------- Body Condition ---------------
        self.body_condition = body_condition_func()

        # --------------- Health Cost ---------------
        self.monthly_health_cost = monthly_health_cost_func(self.body_condition) + self.life_insurance

        # --------------- Initial Monthly Income ---------------
        self.initial_monthly_income = initial_monthly_income_func(self.occupation, SocietyParams.lowest_monthly_income)

        # --------------- Average Consumption Rate based on Salary ---------------
        self.food_consumption_monthly_value = food_consumption_monthly_value_func(self.initial_monthly_income)
        self.other_consumption_monthly_value = other_consumption_monthly_value_func(self.initial_monthly_income)

        # --------------- Savings ---------------
        def initial_saving(occupation_func, age,
                           monthly_health_cost,
                           food_consumption_monthly_value,
                           other_consumption_monthly_value):
            if age < 18:
                return 0
            occupation = occupation_func(age)
            all_monthly_costs = monthly_health_cost + food_consumption_monthly_value + other_consumption_monthly_value
            if occupation == "unemployed":
                return 12 * ((age - 18) * np.round(random.gauss(50, 10)) - all_monthly_costs)
            if occupation == "employed":
                return 12 * ((age - 18) * 12 * np.round(random.gauss(100, 50)) - all_monthly_costs)
            if occupation == "retired":
                return (12 * ((age - 18) * 12 * np.round(random.gauss(100, 50)) - all_monthly_costs) +
                        12 * ((age - 65) * 12 * np.round(random.gauss(40, 5)) - all_monthly_costs))

        self.initial_saving = np.round(max(initial_saving(occupation_func, self.age,
                                                          self.monthly_health_cost,
                                                          self.food_consumption_monthly_value,
                                                          self.other_consumption_monthly_value), 0), 4)

        # --------------- Retirement Payment ---------------
        # Should be 70% of the income for the last 20 years
        self.retirement_payment = 0  # to be calculated

        # --------------- Jobless Subsidy ---------------
        # Should be 70% of lowest income
        self.jobless_subsidy = 0.7 * SocietyParams.lowest_monthly_income

        # --------------- Individual Birth Willingness ---------------
        self.birth_willingness = birth_willingness_func(self.age)

        # --------------- Salary Yearly Increase Rate ---------------
        self.salary_yearly_increase_rate = salary_yearly_increase_rate_func(self.age, self.entrepreneurship)


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
    food_consumption_monthly_value = other_consumption_monthly_value_func(SinglePersonParams.initial_monthly_income)


if __name__ == "__main__":
    print(
        f"Person's age: {SinglePersonParams.age}\n"
        f"Person's life expectancy: {SinglePersonParams.life_expectancy}\n"
        f"Person's occupation: {SinglePersonParams.occupation}\n"
        f"Person's body condition: {SinglePersonParams.body_condition}\n"
        f"Person's monthly health cost: {SinglePersonParams.monthly_health_cost}\n"
        f"Person's initial monthly income: {SinglePersonParams.initial_monthly_income}\n"
        f"Person's food consumption monthly value: {SinglePersonParams.food_consumption_monthly_value}\n"
        f"Person's other consumption monthly value: {SinglePersonParams.other_consumption_monthly_value}\n"
        f"Person's initial saving: {SinglePersonParams.initial_saving}\n"
        f"Person's retirement payment: {SinglePersonParams.retirement_payment}\n"
        f"Person's jobless subsidy: {SinglePersonParams.jobless_subsidy}\n"
        f"Person's birth willingness: {SinglePersonParams.birth_willingness}\n"
        f"Person's salary yearly increase rate: {SinglePersonParams.salary_yearly_increase_rate}\n"
        f"Person's entrepreneurship: {SinglePersonParams.entrepreneurship}\n"
    )
