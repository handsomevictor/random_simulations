"""
In my society, averagely people make around 100 per month.
"""
import os
import random
import string
import numpy as np
import pandas as pd

from simulation_rich_and_poor.tool_functions import generate_random_family_ID


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


def birth_willingness_monthly_func(age: int, num_of_children, is_married):
    """
    Returns the probability of giving birth each month
    """
    multiple_children_multiplier = 0.3
    if not is_married:
        return 0

    if age < 18:
        probability = 0.01
    elif age < 23:
        probability = 0.25 / (23 - 18)  # We have to span the probability over the these years
    elif age < 27:
        probability = 0.3 / (27 - 23)
    elif age < 30:
        probability = 0.2 / (30 - 27)
    elif age < 40:
        probability = 0.10 / (40 - 30)
    else:
        probability = 0

    real_probability = probability * (multiple_children_multiplier ** num_of_children)
    real_probability /= 12
    return real_probability


def initial_num_of_children_func(age):
    if age < 18:
        return 0
    if age < 23:
        return 1 if random.random() < 0.2 else 0
    if age < 30:
        tmp = random.random()
        return 1 if tmp < 0.5 else \
            2 if (tmp < 0.5 and random.random() < 0.4) else 0
    if age < 40:
        tmp = random.random()
        return 1 if tmp < 0.1 else \
            2 if (tmp < 0.3 and random.random() < 0.3) else \
                3 if (tmp < 0.2 and random.random() < 0.05) else 0
    else:
        return 2 if random.random() < 0.15 else 1


def monthly_health_cost_func(body_condition):
    # 之后添加重病的费用
    # Without life insurance
    if body_condition == "healthy":
        return 5
    if body_condition == "sick":
        return 30
    if body_condition == "disabled":
        return 15
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
        return SinglePerson().jobless_subsidy
    if occupation == "employed":
        return np.round(max(random.gauss(100, 60), lowest_monthly_income), 4)
    if occupation == "retired":
        return 0
    else:
        return 0


def food_consumption_monthly_value_func(monthly_income):
    # Use lognormal to generate the food consumption - currently if monthly income is 100, the food consumption is
    # averagely around 20
    # To survive, the minimum food consumption is 12 (12 / the lowest income - 30 = 40%)
    mean_lognormal_food_consumption_monthly = 1
    std_deviation = 0.2

    consumption_value = (random.lognormvariate(mean_lognormal_food_consumption_monthly, std_deviation)
                         * monthly_income / 12)
    return max(consumption_value, 12)


def other_consumption_monthly_value_func(initial_monthly_income):
    other_consumption_monthly_mean = np.random.gamma(shape=1.2, scale=initial_monthly_income / 1.2, size=1)[0]
    if initial_monthly_income == 0:
        return 0
    if initial_monthly_income < 50:
        return np.round(0.5 * other_consumption_monthly_mean, 4)
    if initial_monthly_income < 100:
        return np.round(0.3 * other_consumption_monthly_mean, 4)
    if initial_monthly_income < 200:
        return np.round(0.25 * other_consumption_monthly_mean, 4)
    if initial_monthly_income < 500:
        return np.round(0.2 * other_consumption_monthly_mean, 4)
    if initial_monthly_income < 1000:
        return np.round(0.13 * other_consumption_monthly_mean, 4)
    else:
        return np.round(0.1 * other_consumption_monthly_mean, 4)


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


def entrepreneur_ratio_monthly_fluctuation_func(already_entrepreneur, age, saving=None):
    """
    Returns the probability of becoming an entrepreneur each month
    """
    # Everyone may become an entrepreneur, but the probability is related to age and saving.
    # currently saving is not used
    if not already_entrepreneur:
        if age < 15:
            return 0
        if age < 23:
            return 0.03 / 12
        if age < 28:
            return 0.02 / 12
        if age < 40:
            return 0.005 / 12
        if age < 65:
            return 0.00025 / 12
        else:
            return 0
    elif already_entrepreneur:
        # set the probability of failure to be 0.03 each month
        return 1 - 0.03


def marriage_rate_monthly_func(age):
    """
    按当今社会的情况，18岁以下的人不结婚，18岁到23岁的人结婚概率为20%，23岁到30岁的人结婚概率为50%，30岁到40岁的人结婚概率为10%，
    40岁到65岁的人结婚概率为5%，65岁以上的人不结婚
    """
    if age < 18:
        return False
    elif age < 23:
        return random.random() < (0.2 / 12)
    elif age < 30:
        return random.random() < (0.5 / 12)
    elif age < 40:
        return random.random() < (0.1 / 12)
    elif age < 65:
        return random.random() < (0.05 / 12)
    else:
        return False


class CurrentTime:
    def __init__(self):
        self.current_year = 1
        self.current_month = 1


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

    # --------------- Entrepreneurship Success Rate ---------------
    entrepreneurship_success_rate = 0.05


# noinspection PyTypeChecker
class SinglePerson:
    """
    Single person parameters:
    - age
    - life_expectancy
    - occupation
    - body_condition
    """

    def __init__(self, family_id):
        self.monthly_saving = None
        self.occupation = None
        self.life_expectancy = None
        self.dead = None
        self.age_month = None
        self.age = None
        self.sex = None
        self.current_time = None
        self.current_year = None
        self.current_month = None
        self.already_married = None
        self.entrepreneurship = None
        self.successful_entrepreneur = None
        self.life_insurance = None
        self.body_condition = None
        self.monthly_health_cost = None
        self.initial_monthly_income = None
        self.last_period_employee_income = None
        self.current_period_income = None
        self.food_consumption_monthly_value = None
        self.other_consumption_monthly_value = None
        self.initial_saving = None
        self.retirement_monthly_payment = None
        self.total_saving = None
        self.jobless_subsidy = None
        self.baby_cost = None
        self.num_of_children = None
        self.birth_willingness = None
        self.salary_yearly_increase_rate = None

        self.family_id = family_id

    def set_initial_params(self):
        # --------------- Current Time ---------------
        self.current_time = CurrentTime()

        # --------------- Sex ---------------
        self.sex = random.choice(['woman', 'man'])

        # --------------- Age ---------------
        def set_age():
            age = np.round(np.random.gamma(shape=3, scale=12, size=1)[0])
            age = min(max(age, 1), 110)
            if age >= 100:
                # generate again
                age = np.round(np.random.gamma(shape=3, scale=11, size=1)[0])
                age = min(max(age, 1), 110)
            age_month = np.round(random.random() * 12)
            return age, age_month

        self.age, self.age_month = set_age()

        # --------------- Life Expectancy ---------------
        self.life_expectancy = np.round(random.gauss(70, 10))

        # if age larger than life expectancy, set this person to Dead and remove this person
        while self.age >= self.life_expectancy:
            self.age, self.age_month = set_age()
            self.life_expectancy = np.round(random.gauss(70, 10))

        self.dead = False

        # --------------- Occupation ---------------
        self.occupation = occupation_func(self.age)

        # --------------- Marriage ---------------
        self.already_married = marriage_rate_monthly_func(self.age)

        # --------------- Entrepreneurship ---------------
        self.entrepreneurship = True if random.random() < entrepreneur_ratio_func(self.age) else False
        self.successful_entrepreneur = True if (self.entrepreneurship and
                                                random.random() < SocietyParams.entrepreneurship_success_rate) \
            else False

        # --------------- Life Insurance ---------------
        self.life_insurance = life_insurance_func(self.occupation)

        # --------------- Body Condition ---------------
        self.body_condition = body_condition_func()

        # --------------- Health Cost ---------------
        monthly_health_cost = monthly_health_cost_func(self.body_condition) - self.life_insurance
        self.monthly_health_cost = max(monthly_health_cost, 0)

        # --------------- Initial Monthly Income ---------------
        self.initial_monthly_income = initial_monthly_income_func(self.occupation, SocietyParams.lowest_monthly_income)
        self.last_period_employee_income = self.initial_monthly_income  # for calculating retirement payment
        self.current_period_income = 0  # Assume 0, to be updated in the next month

        # --------------- Average Consumption Rate based on Salary ---------------
        self.food_consumption_monthly_value = food_consumption_monthly_value_func(self.initial_monthly_income)
        self.other_consumption_monthly_value = other_consumption_monthly_value_func(self.initial_monthly_income)

        # --------------- Savings ---------------
        def initial_saving(occupation_func,
                           age,
                           monthly_health_cost,
                           food_consumption_monthly_value,
                           other_consumption_monthly_value,
                           entrepreneurship=False):
            all_monthly_costs = monthly_health_cost + food_consumption_monthly_value + other_consumption_monthly_value
            if not entrepreneurship:
                if age < 18:
                    return 0
                occupation = occupation_func(age)
                if occupation == "unemployed":
                    return 12 * (age - 18) * (50 - all_monthly_costs)
                if occupation == "employed":
                    return 12 * (age - 18) * (100 - all_monthly_costs)
                if occupation == "retired":
                    return (12 * (age - 18) * (100 - all_monthly_costs) +
                            12 * (age - 65) * (np.round(random.gauss(40, 5)) - all_monthly_costs))
            elif entrepreneurship:
                # If he is a successful entrepreneur
                if self.successful_entrepreneur:
                    # Monthly income is 20 times the average monthly payment
                    return 12 * (age - 15) * (20 * 100 - all_monthly_costs)
                else:
                    # If he is not a successful entrepreneur
                    if age < 18:
                        return 12 * (age - 18) * (np.round(240) - all_monthly_costs)
                    elif age < 23:
                        return 12 * (age - 18) * (np.round(250) - all_monthly_costs)
                    elif age < 35:
                        return 12 * (age - 18) * (np.round(200) - all_monthly_costs)
                    elif age < 65:
                        return 12 * (age - 18) * (np.round(175) - all_monthly_costs)

        self.initial_saving = np.round(max(initial_saving(occupation_func, self.age,
                                                          self.monthly_health_cost,
                                                          self.food_consumption_monthly_value,
                                                          self.other_consumption_monthly_value,
                                                          self.entrepreneurship), 0), 0)

        self.total_saving = self.initial_saving

        # --------------- Retirement Payment ---------------
        # Should be 70% of the income for the last 20 years (ideally, but now we just use the last month payment)
        self.retirement_monthly_payment = 0  # to be calculated in the next month

        # --------------- Jobless Subsidy ---------------
        # Should be 70% of lowest income
        self.jobless_subsidy = 0.7 * SocietyParams.lowest_monthly_income if self.occupation == "unemployed" else 0

        # --------------- Individual Birth Willingness ---------------
        self.num_of_children = initial_num_of_children_func(self.age)
        self.birth_willingness = birth_willingness_monthly_func(self.age, self.num_of_children, self.already_married)

        # --------------- Baby Cost ---------------
        # Assume this is 0, will update starting from the next month
        self.baby_cost = 0

        # --------------- Salary Yearly Increase Rate ---------------
        self.salary_yearly_increase_rate = salary_yearly_increase_rate_func(self.age, self.entrepreneurship)

    def update_next_month_behavior(self, record_baby=False):
        """
        Single person behavior: This depicts how individual behave for the next month.
        - consume
        - save
        - die
        - give birth
        - get sick
        - get disabled
        - get employed
        - get retired
        """
        # --------------- Update Current Time and Age ---------------
        self.current_time.current_month += 1
        self.age_month += 1
        if self.current_time.current_month > 12:
            self.current_time.current_month = 1
            self.current_time.current_year += 1
        if self.age_month > 12:
            self.age += 1
            self.age_month = 1

        # --------------- Update Death ---------------
        if self.age >= self.life_expectancy:
            self.dead = True

        # --------------- Update Marriage ---------------
        if not self.already_married:
            self.already_married = marriage_rate_monthly_func(self.age)

        # --------------- Update Baby / Birth Willingness ---------------
        if self.already_married:
            self.birth_willingness = birth_willingness_monthly_func(self.age, self.num_of_children,
                                                                    self.already_married)

            if random.random() < self.birth_willingness:
                self.num_of_children += 1
                # Generate a new baby with the same family ID
                new_baby = SinglePerson(self.family_id)
                new_baby.set_initial_params()

                new_baby.age = 1
                new_baby.age_month = 1
                new_baby.current_time = self.current_time

                if record_baby:
                    new_baby.write_to_individual_database()

        ############################################################################
        # --------------- Income Cash Flow ---------------
        # --------------- Update Occupation ---------------
        # # Every month, the occupation may change to unemployed, employed, or retired
        self.occupation = occupation_func(self.age)

        # -------------- Update Entrepreneurship ---------------
        self.entrepreneurship = True if random.random() < entrepreneur_ratio_monthly_fluctuation_func(
            self.entrepreneurship, self.age) else False

        # --------------- Update Salary Yearly Increase Rate ---------------
        self.salary_yearly_increase_rate = salary_yearly_increase_rate_func(self.age, self.entrepreneurship)

        # judge entrepreneurship
        if self.entrepreneurship:
            if self.successful_entrepreneur:
                # Monthly income is meanly 15 times the average monthly payment
                self.current_period_income = 15 * np.round(np.random.gamma(shape=5, scale=20, size=1)[0])
            else:
                if self.age < 18:
                    self.current_period_income = np.round(np.random.gamma(shape=4, scale=35, size=1)[0])
                elif self.age < 23:
                    self.current_period_income = np.round(np.random.gamma(shape=5, scale=50, size=1)[0])
                elif self.age < 35:
                    self.current_period_income = np.round(np.random.gamma(shape=6, scale=30, size=1)[0])
                elif self.age < 65:
                    self.current_period_income = np.round(np.random.gamma(shape=7, scale=20, size=1)[0])
        else:
            if self.occupation == "unemployed":
                self.current_period_income = self.jobless_subsidy
            elif self.occupation == "baby" or self.occupation == "student":
                self.current_period_income = 0
            elif self.occupation == "employed":
                self.current_period_income = self.initial_monthly_income if self.initial_monthly_income != 0 \
                    else initial_monthly_income_func(self.occupation, SocietyParams.lowest_monthly_income)
            elif self.occupation == "retired":
                self.current_period_income = 0  # will receive retirement payment below

        # If the year passed, increase the salary, including the entrepreneur
        if self.current_time.current_month == 1:
            self.current_period_income = np.round(self.current_period_income * (1 + self.salary_yearly_increase_rate))
            self.initial_monthly_income = np.round(self.initial_monthly_income *
                                                   (1 + self.salary_yearly_increase_rate)) \
                if self.initial_monthly_income != 0 else self.current_period_income

        # --------------- Update Life Insurance ---------------
        self.life_insurance = life_insurance_func(self.occupation)

        # --------------- Jobless Subsidy ---------------
        # Should be 70% of lowest income
        self.jobless_subsidy = 0.7 * SocietyParams.lowest_monthly_income if self.occupation == "unemployed" else 0

        # --------------- Retirement Payment ---------------
        if self.occupation != "retired":
            self.last_period_employee_income = self.current_period_income
        else:
            pass

        if self.occupation == "retired":
            self.retirement_monthly_payment = 0.7 * self.last_period_employee_income

        ############################################################################
        # --------------- Normal Consumption Cash Flow ---------------
        # Now it's fixed, will be changed to normal distribution
        self.food_consumption_monthly_value = food_consumption_monthly_value_func(self.current_period_income)
        self.other_consumption_monthly_value = other_consumption_monthly_value_func(self.current_period_income)

        # --------------- Health Cost ---------------
        # If there is a baby, the cost will increase
        self.body_condition = body_condition_func()
        monthly_health_cost = monthly_health_cost_func(self.body_condition) - self.life_insurance
        self.monthly_health_cost = max(monthly_health_cost, 0)

        # --------------- Baby Cost ---------------
        # Assume the cost of one baby is random distribution of mean 60 and std 20 per month
        self.baby_cost = np.round(np.random.normal(60, 20) * self.num_of_children)

        ############################################################################
        # ------------------------------ Saving ------------------------------
        self.monthly_saving = (self.current_period_income + self.retirement_monthly_payment
                               - self.food_consumption_monthly_value - self.other_consumption_monthly_value -
                               self.monthly_health_cost - self.baby_cost)

        # --------------- Update Total Saving ---------------
        self.total_saving += self.monthly_saving

    def write_to_individual_database(self):
        tmp_df = pd.DataFrame({
            "family_id": self.family_id,
            "current_year": self.current_time.current_year,
            "current_month": self.current_time.current_month,
            "sex": self.sex,
            "age": self.age,
            "age_month": self.age_month,
            "life_expectancy": self.life_expectancy,
            "dead": self.dead,
            "occupation": self.occupation,
            "already_married": self.already_married,
            "entrepreneurship": self.entrepreneurship,
            "successful_entrepreneur": self.successful_entrepreneur,
            "life_insurance": self.life_insurance,
            "body_condition": self.body_condition,
            "monthly_health_cost": self.monthly_health_cost,
            "baby_cost": self.baby_cost,
            "initial_monthly_income": self.initial_monthly_income,
            "current_period_income": self.current_period_income,
            "last_period_employee_income": self.last_period_employee_income,
            "food_consumption_monthly_value": self.food_consumption_monthly_value,
            "other_consumption_monthly_value": self.other_consumption_monthly_value,
            "initial_saving": self.initial_saving,
            "monthly_saving": self.monthly_saving,
            "total_saving": self.total_saving,
            "retirement_monthly_payment": self.retirement_monthly_payment,
            "jobless_subsidy": self.jobless_subsidy,
            "birth_willingness": self.birth_willingness,
            "num_of_children": self.num_of_children,
            "salary_yearly_increase_rate": self.salary_yearly_increase_rate
        }, index=[0])

        if not os.path.exists(os.path.join(os.getcwd(), 'tmp_database', "population_individual_database",
                                           self.family_id)):
            os.makedirs(os.path.join(os.getcwd(), 'tmp_database', "population_individual_database", self.family_id))
        tmp_df.to_csv(os.path.join(os.getcwd(), 'tmp_database', "population_individual_database", self.family_id,
                                   f'individual_info_{self.current_time.current_year}-'
                                   f'{self.current_time.current_month}.csv'), index=False)


if __name__ == "__main__":
    random_person = SinglePerson()
    print(random_person.__dict__)
    # 不要在这个层级调用这个函数，因为这个函数会写入文件到本目录下
    random_person.write_to_individual_database()
