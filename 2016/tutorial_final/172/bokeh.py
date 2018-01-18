
# coding: utf-8

# # 0-Introduction  
# ## 0.1-What is Bokeh?
# Bokeh is a python visualization library that targets modern web browsers for presentation.
# Compares to some other plotting library like [matplotlib](http://matplotlib.org/), Bokeh is easier to create interactive plots, dashboards and data application with more beautiful and meaningful visual presentation. The high performance of interactivity with streaming and large scale datasets is also one of its advantage.  Bokeh can help anyone who would like to quickly and easily create interactive plots, dashboards, and data applications. A more detailed introduction can be found on [Bokeh's website](https://github.com/bokeh/bokeh).
# 
# 
# ## 0.2-How does Bokeh work?
# The snapshot below can quickly explain the workflow of how Bokeh helps to present data and target on web browsers:

# <img src="files/Bokeh_Intro.png" width="400px" height="300px">
# 

#    From the snapshot above we can notice that: Bokeh supports multiple different language such as Python, R,lua and Julia. These underlying components generate JSON files which contains data and finally received by BokehJS, a JavaScript library. Therefore, like famous D3.js, Bokeh can support large-scale steaming data visualization and allows developers who are not very familiar to JavaScript to build their prototype on light weight python framework like [Flask](http://flask.pocoo.org/) or [Django](https://www.djangoproject.com/).
# 
# 
# 
# ## 0.3-What can Bokeh do?
# Here we choose some great short examples on [Bokeh websites](http://bokeh.pydata.org/en/latest).  
# 
# 
# *(Click on any of the thumbnails to open the interactive version.)*
# 
# <table><tr>
# <td><a href="http://bokeh.pydata.org/docs/gallery/burtin.html" target="_blank"><img width=50% src="files/burtin.png"></a></td>
# <td><a href="http://bokeh.pydata.org/docs/gallery/periodic.html" target="_blank"><img width=50% src="files/periodic.png"></a></td>
# <td><a href="http://bokeh.pydata.org/docs/gallery/boxplot.html" target="_blank"><img width=50% src="files/boxplot.png"></a></td>
# </tr>
# <tr>
# <td><a href="http://bokeh.pydata.org/docs/gallery/texas.html" target="_blank"><img width=50% src="files/texas.png"></a></td>
# <td><a href="http://bokeh.pydata.org/docs/gallery/chord_chart.html" target="_blank"><img width=50% src="files/chord_chart.png"></a></td>
# <td><a href="http://bokeh.pydata.org/docs/gallery/les_mis.html" target="_blank"><img width=50% src="files/les_mis.png"></a></td>
# </tr></table>
# 
# 
# 
# <br>
# To offer both simplicity and the powerful and flexible features needed for advanced customizations, Bokeh exposes three interface levels to users:
# 
# * a low-level [bokeh.models](http://bokeh.pydata.org/en/latest/docs/reference/models.html#bokeh-models) interface that provides the most flexibility to application developers.
# * an intermediate-level [bokeh.plotting](http://bokeh.pydata.org/en/latest/docs/reference/plotting.html#bokeh-plotting) interface centered around composing visual glyphs.
# * a high-level [bokeh.charts](http://bokeh.pydata.org/en/latest/docs/reference/charts.html#bokeh-charts) interface to build complex statistical plots quickly and simply.
# <img src="files/Bokeh_Interface.png" width="400px" height="300px">
# 

# # 1-Let's Start!
# 
# ## 1.1-installation
# 
# * For the 15-688 course purpose, [Anaconda](https://www.continuum.io/why-anaconda) has already pre-installed the Bokeh package so no extra work for you :).
# 
# * For your own environment, the easiest way to install is use pip: 
# 
# * (you should be confident that you have installed all needed dependencies, such as NumPy):
# 

# ```python 
# pip install bokeh
# ```
# 

# ## 1.2-Get started
# 
# To let you have a better undetstanding for Bokeh, I will go through the three interfaces provided by
# Boeh: Charts,Plotting and Models. Each with one short example. 
# 
# Let's start from the Chart model:
# 
# ### 1.2.1-Charts 
# As mentioned above in part 0.2, 'Charts' is the most high-level interface in Bokeh to provide a fast&convenient way for common statistical charts (such as  box plot, bar chart, area plot, heat map, donut chart and many others) with minimum amount of code. Usually the input data will be Pandas dataframe or similar table-like data. The general workflow for using Chart is:
# 1. Import the library and functions/ methods
# 2. Prepare the data
# 3. Set the output mode (Notebook, Web Browser or Server)
# 4. Create chart with styling option (if required)
# 5. Visualize the chart
# 
# I will write code corresponding to these five steps by adding comments in the next short example: we draw a timeseries chart here to see the stock price changing trend between year 2000 and 2015. The data here is grabbed from [Yahoo Finance API](https://developer.yahoo.com/finance/). 

# In[1]:

#-----1st step here is to import the library and functions, we draw a time-----
import pandas as pd
from bokeh.charts import TimeSeries, show, output_file,output_notebook
from bokeh.layouts import column


#-----2nd step: prepare the data-----
AAPL = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])
MSFT = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=MSFT&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])
IBM = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=IBM&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])
data = dict(
    AAPL=AAPL['Adj Close'],
    Date=AAPL['Date'],
    MSFT=MSFT['Adj Close'],
    IBM=IBM['Adj Close'],
)

#----3rd step: Set the output mode (Notebook, Web Browser or Server)-----
# Here we use output_notebook for demo, you can change to output_fule easily 
# using the next line code in comment.
output_notebook()#output_file("timeseries.html")

#----4th step:Create chart with styling option-----
tsline = TimeSeries(data,
    x='Date', y=['IBM', 'MSFT', 'AAPL'],
    color=['IBM', 'MSFT', 'AAPL'], dash=['IBM', 'MSFT', 'AAPL'],
    title="Timeseries", ylabel='Stock Prices', legend=True)


#----5th step:Visualize the chart-----
show(column(tsline))


# The time seires plot is generated following our 'five steps' mentioned above. You can play with chart using the tool bar on the right sight: easily zoom in and out or drag the selected area to see more details. Here we quickly go through some other common charts you may need in Bokeh:
# 
# 

# In[2]:

from bokeh.charts import Bar, output_notebook, show
from bokeh.sampledata.autompg import autompg as df

p = Bar(df, label='yr', values='mpg', agg='median', group='origin',
        title="Median MPG by YR, grouped by ORIGIN", legend='top_right')

output_notebook()
show(p)


# In[3]:

from bokeh.charts import Bar, output_notebook, show
from bokeh.sampledata.autompg import autompg as df

p = Bar(df, label='origin', values='mpg', agg='mean', stack='cyl',
        title="Avg MPG by ORIGIN, stacked by CYL", legend='top_right')

output_notebook()
show(p)


# In[4]:

from bokeh.charts import Histogram, output_notebook, show
from bokeh.sampledata.autompg import autompg as df

p = Histogram(df, values='mpg', bins=50,
              title="MPG Distribution (50 bins)")

output_notebook()
show(p)


# ### 1.2.2-Plottings
# For 'Plottings' model, it generates a figure for plotting and add it to the current document or webpage. The genral workflow is very similar to the 'Charts' model except for sevral new functions and graph types are included.
# The first example we give here is a 'burble' or 'circle' graph with random size, position and colors with specifc meaning to show the render expressiveness of Bokeh package.  

# In[5]:

import numpy as np

from bokeh.plotting import figure, output_notebook, show

# prepare some data
N = 4000
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
]

# output to static HTML file (with CDN resources)
output_notebook()

TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

# create a new plot with the tools above, and explicit ranges
p = figure(tools=TOOLS, x_range=(0,100), y_range=(0,100))

# add a circle renderer with vectorized colors and sizes
p.circle(x,y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)

# show the results
show(p);


# The second example here demonstrate how to draw sine function with several variations on line pattern and colors.
# Beware of the details like how to add graph titles and legends when showing a graph.

# In[6]:

from bokeh.plotting import figure,output_notebook,show
import numpy as np

x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)

plot = figure(title="Sine Function")
plot.xaxis.axis_label='x'
plot.yaxis.axis_label='amplitude'
output_notebook()

plot.line(x, y, 
  line_color='blue',
  line_width=2,
  legend='sin(x)')

plot.circle(x, 2*y, 
  fill_color='red',
  line_color='black',
  fill_alpha=0.2,
  size=10,
  legend='2sin(x)')

#line_dash is an aribrary length list of lengths
#alternating in [color, blank, color, ...]
plot.line(x, np.sin(2*x),
  line_color='green',
  line_dash=[10,5,2,5], 
  line_width=2,
  legend='sin(2x)')
show(plot)


# ### 1.2.3-Models
# The most lowest-level concept for BOkeh is 'Models'. Since Bokeh mainly aims at modern web browser presentation, one of the central design principlas of Boleh is that, in spite of the langugae used by end users (Python, R or lua etc.), the result objet is a graph that encompasses all the data stream and visualization aspects. Moreover, all the models objects can be serialized and used by the previously mentioned BokehJS library to render the plot. Ultimately all Bokeh plots consist of collections of models.
# Different from the previous sections. Bokeh 'Models' uses very little defaults unlike the 'Figure' and ‘Chart’ interfaces mentioned above. Instead, we will go through a real world example for how to use Bokeh graphing technique in our data science research. If you are really interested with using Bokeh 'Models'. [Here](https://github.com/bokeh/bokeh/tree/master/examples) is a good start for tutorial.
# 

# ## 2.1-Real example
# As we all know, graphing technique itself may not be the most essential part during data science research: it has to combined with real algorithm or data, to show its visualization power. In the next example, we use a neutral network model to predict whether a song has made it onto the Billboard Top 50, based on its year of release (integer number from 1900 to 2000), length of recording (float number from 0 to 7), genre of jazz (True or False) and genre of Rock and Roll (True or False).
# 
# If you are not very familiar with [Neutral network](https://en.wikipedia.org/wiki/Artificial_neural_network), it is a computational model inspired by biological science where how brain solves problems with large clusters of biological neurons connected by axons. Tutorials of neutral network can be easily find somewhere else, in this tutorial, we can simply treat it as a black box with following parameters:
# 
# * step size (or learning rate)
# * number of neurons (you can think it as the complexity of the algorithm we want to set) 
# * stop criteria (in this case we use number of iteration times)
# 
# One problem for neutral network training and probably every machine learning problem is over-fitting: the main goal for machine learning algorithm is to minimize target function on given training data once it is chosen, but when a model is excessively complex, such as having too many parameters relative to the number of observations. A model that has been over-fitted has poor predictive performance, as it overreacts to minor fluctuations in the training data. Therefore, during the training time, we could collect the data for both training error and testing error to find out the turning point when testing error starts to grow and then find out the best iteration number for the given model.
# 
# In the code we show below, training and testing data is read from local file after initialization, at the beginning of each training session, we randomly assign initial weight for each node in the neutral network. One training session is regarded as finishing all the updates on neurons’ weight after all the iterations. Given the limited training time, multiple training sessions can be done and the best result will be chosen.
# 
# After running the following code, several graphs will be generated to show the trends for both training error and testing error changes as the number of iterations goes up for each training session. For the default setting used in the code, we generate three different plots to see similar patterns: training error keeps going down as more iterations completed, while the testing error first goes down then starts to go up which shows the pattern of over-fitting. Therefore, the best training time should be chosen at the pivot point on the graph.
# 

# In[7]:

import csv
import sys
import math
import random
import numpy as np
import time
from bokeh.plotting import figure,output_notebook,show


# standardize the input data to be within range 0 to 1
def standard(data, high=1.0, low=0.0):
    mins = np.min(data, axis=0)
    maxs = np.max(data, axis=0)
    rng = maxs - mins
    return high - (((high - low) * (maxs - data)) / rng)

#function to calculate testing data error rate using current weights
def test_err_rate(hidden_weight_1, output_weight_1):
    hidden_input1 = np.dot(test_data,hidden_weight_1.T)
    hidden_output1 = 1/(np.exp(np.negative(hidden_input1))+1)
    final_input1 = np.dot(hidden_output1, output_weight_1)
    final_output1 = 1/(np.exp(np.negative(final_input1))+1)
    err = 0
    for i in range(len(answer)):
        if final_output1[i] >0.5 and answer[i] =='no':
            err += 1.0
        if final_output1[i] <0.5 and answer[i] =='yes':
            err += 1.0
    return err / len(answer)

#function to calculate testing data cumulative error using current weights
def test_cumu_err(hidden_weight_1, output_weight_1):
    hidden_input1 = np.dot(test_data,hidden_weight_1.T)
    hidden_output1 = 1/(np.exp(np.negative(hidden_input1))+1)
    final_input1 = np.dot(hidden_output1, output_weight_1)
    final_output1 = 1/(np.exp(np.negative(final_input1))+1)
    err = 0
    for i in range(len(answer)):
        if answer[i] =='no':
            err += final_output[i] ** 2
        else:
            err += (1.0 - final_output[i]) ** 2
    return err

#paprameters settings here:            
answer = ['yes','yes','yes','no','no','no','yes','yes','yes','no','no','yes','no','no','no','no','yes','no','yes','yes','no','no','no','no','yes','yes']
training_file = 'training_file.csv'
testing_file = 'testing_file.csv'
training_time = 25
hidden_unit_size = 16
ori_step_size = 0.15
training_iter = 80000
train_error_group = []
test_error_group = []
x_axis  = []
start = time.time()

#read input training data and transfer it to right format
with open(training_file,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = csvreader.next()
    for i in range(len(header)):
        header[i] = header[i].strip()
    label = header[-1]
    raw_data = [row for row in csvreader]
    length = len(raw_data)
    input_size = len(header)  
    label_list = np.array([[1.0] if row[-1] == 'yes' else [0.1] for row in raw_data])
    for row in raw_data:
        row[2] = 1.0 if row[2] == 'yes' else 0.1
        row[3] = 1.0 if row[3] == 'yes' else 0.1
        row[4] = 1.0 if row[4] == 'yes' else 0.1
        
    raw_data = standard(np.array(raw_data).astype(float))
    raw_data[:,-1] = 1

#read input testing data and transfer it to right format
with open(testing_file,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    test_header = csvreader.next()
    for i in range(len(test_header)):
        test_header[i] = test_header[i].strip()
    test_data = list(csvreader)
    for row in test_data:
        row.append(random.uniform(0.0,1.0))
        row[2] = 1.0 if row[2] == 'yes' else 0.1
        row[3] = 1.0 if row[3] == 'yes' else 0.1
    test_data = np.array(standard(np.array(test_data).astype(float)))
    test_data[:,-1] = 1.0

    
    restart = 0
    error = np.inf
    rate = np.inf
    train_error_group = []
    test_error_group = []
    
#training start:
    while time.time() - start < training_time:
        restart += 1
        train_error_list = []
        test_error_list = []
        output_weight = np.array([[random.uniform(0.0, 1.0)] for i in range(hidden_unit_size)])
        hidden_weight = np.array([[random.uniform(0.0, 1.0) for i in range(len(header))] for j in range(hidden_unit_size)])
    
        for i in range(training_iter):
            step_size = ori_step_size - (time.time()-start)/float(1000)
            hidden_input = np.dot(raw_data,hidden_weight.T)
            hidden_output = 1/(np.exp(np.negative(hidden_input))+1)
            final_input = np.dot(hidden_output, output_weight)
            final_output = 1/(np.exp(np.negative(final_input))+1)
            final_error = final_output * (1-final_output) * (label_list - final_output)
            output_weight += np.dot(hidden_output.T,final_error) * step_size
            hidden_error = hidden_output * (1-hidden_output)*np.dot(final_error,output_weight.T)
            hidden_weight += np.dot(hidden_error.T,raw_data) * step_size 

            if i % 500 == 0:
                test_training_rate = test_err_rate(hidden_weight,output_weight)
                if test_training_rate < rate:
                    best_output_weight = np.copy(output_weight)
                    best_hidden_weight = np.copy(hidden_weight)
                    rate = test_training_rate
                #print rate, test_training(best_hidden_weight,best_output_weight)
            if i % 2000 == 0:
                tmp = np.sum(np.square(final_output - label_list))/2
                if tmp < error:
                    error = tmp
                train_error_list.append(tmp)
                test_error_list.append(test_cumu_err(hidden_weight,output_weight))
                x_axis.append(i)
        train_error_group.append(train_error_list)
        test_error_group.append(test_error_list)
    
    print 'TRAINING COMPLETED! NOW PREDICTING.'
#testing start:
    hidden_input = np.dot(test_data,best_hidden_weight.T)
    hidden_output = 1/(np.exp(np.negative(hidden_input))+1)
    final_input = np.dot(hidden_output, best_output_weight)
    final_output = 1/(np.exp(np.negative(final_input))+1)
    predict =[]
    for output in final_output:
        if output >=0.5:
            predict.append('yes')
        else:
            predict.append('no')
    print 'restart time',restart
    print 'Our prediction:' ,predict
    print 'Anwser:', answer
    err = 0
    for i in range(len(predict)):
        if predict[i] != answer[i]:
            err+=1
    print 'err rate',err/float(len(predict))
    for i in range(len(train_error_group)):
        plot = figure(title="Error vs. Number of iterations: "+str(i+1))
        plot.xaxis.axis_label='Iteration time'
        plot.yaxis.axis_label='Error'
        output_notebook()
        plot.line(x_axis, train_error_group[i], 
          line_color='green',
          line_dash=[10,5,2,5], 
          line_width=3,
          legend='traning error')
        plot.line(x_axis, test_error_group[i], 
          line_color='black',
          line_dash=[10,5,2,5], 
          line_width=3,
        legend='testing error')
        show(plot)


# In[ ]:



