import pandas as pd
import os
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.models.widgets import Div
from bokeh.util.browser import view

def plot_distribution_3d():
    # 读取数据
    people_df = pd.read_csv(os.path.join(os.getcwd(), 'tmp_database', 'test_data.csv'))
    initial_saving = people_df['initial_saving']
    age = people_df['entrepreneurship_successful']

    # 创建 ColumnDataSource
    source = ColumnDataSource(data=dict(age=age, initial_saving=initial_saving))

    # 创建 WebGL 绘图
    p = figure(width=600, height=400, title="Age vs. Initial Saving",
               x_axis_label='Age', y_axis_label='Initial Saving', output_backend="webgl")

    # 添加散点图
    p.circle('age', 'initial_saving', source=source, size=5, color='blue', alpha=0.8)

    # 创建 HTML 文件并显示
    output_file("bokeh_3d_plot.html")
    show(column(Div(text="<h1>3D plots are not natively supported in Bokeh</h1>"),
                p))

plot_distribution_3d()
