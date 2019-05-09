import math
import numpy as np
import matplotlib.pyplot as plt 


def frequency_diagram(data, values, title, x_name, y_name, filename, x_labels = []):
    '''
    Creates a bar chart.
    Parameter data: List containing x values.
    Parameter values: List containing y values.
    Parameter title: Chart title
    Parameter x_name: X-axis label.
    Parameter y_name: Y-axis label.
    Parameter filename: Name of output file.
    Parameter x_labels: Optional alternate x-axis tick labels.
    '''
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots()
    ax.bar(data, values, width, color='Blue', zorder = 3)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_name)
    ax.set_xlabel(x_name)
    ax.set_title(title)
    ax.set_xticks(data)
    if x_labels != []: #If there are optional labels, add them.
        ax.set_xticklabels(x_labels)
    ax.set_yticks(np.arange(0, max(values)+10, 200))
    ax.grid(zorder = 0) #Puts graph lines behind bars.
    plt.savefig(filename, format = "png")
    plt.close(fig)


def pie_chart(data, values, title, filename):
    '''
    Creates a pie chart.
    Parameter data: List containing x values.
    Parameter values: List containing y values.
    Parameter title: Chart title
    Parameter filename: Name of output file.
    '''
    labels = data
    sizes = values

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)

    plt.savefig(filename, format = "png")
    plt.close(fig)


def dot_chart(data, values, title, x_name, scale, filename):
    '''
    Creates a dot chart.
    Parameter data: List containing x values.
    Parameter values: List containing y values.
    Parameter title: Chart title
    Parameter x_name: X-axis label.
    Parameter scale: Number that defines scale of x-axis values.
    Parameter filename: Name of output file.
    '''
    for x in range(len(values)):
        values[x] = 0 #Sets all y-values to 0.
    fig, ax = plt.subplots()
    ax.scatter(data, values, marker = '.', s = 200, alpha = 0.3, color = "blue")
    axes = plt.gca()
    axes.axes.get_yaxis().set_visible(False) #Hides y-axis.
    ax.set_xlabel(x_name)
    ax.set_title(title)
    ax.set_xticks(np.arange(round_down(min(data), scale), max(data)+scale, scale//2)) #Scales x-ticks to be spaced evenly, no matter the data.

    plt.savefig(filename, format = "png")
    plt.close(fig)


def histogram(data, title, x_name, filename, y_name = "Count", bin_num = 10):
    '''
    Creates a histogram chart.
    Parameter data: List containing data.
    Parameter title: Chart title
    Parameter x_name: X-axis label.    
    Parameter filename: Name of output file.
    Parameter y_name: Y-axis label.
    Parameter bin_num: Number of bins.
    '''
    fig, ax = plt.subplots()
    ax.hist(data, bins=bin_num, edgecolor = "black")
    ax.set_ylabel(y_name)
    ax.set_xlabel(x_name)
    ax.set_title(title)

    plt.savefig(filename, format = "png")
    plt.close(fig)


def scatter_plot(data, values, title, x_name, y_name, x_scale, filename, y_scale = 10, extra_data = False):
    '''
    Creates a scatter plot.
    Parameter data: List containing x values.
    Parameter values: List containing y values.
    Parameter title: Chart title
    Parameter x_name: X-axis label.
    Parameter y_name: Y-axis label.
    Parameter x_scale: Number that defines scale of x-axis values.
    Parameter filename: Name of output file.
    Parameter y_scale: Number that defines scale of y-axis values.
    Parameter extra_data: Optional adding of best fit line and stats.
    '''
    fig, ax = plt.subplots()
    ax.scatter(data, values, marker = '.', s = 50, color = "blue", zorder = 3)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.set_title(title)
    ax.set_xticks(np.arange(round_down(min(data), x_scale), max(data)+x_scale, x_scale))
    ax.set_yticks(np.arange(0, max(values)+y_scale, y_scale))
    ax.grid(zorder = 0)

    if extra_data:
        mean_x = np.mean(data) #Finds average of data.
        mean_y = np.mean(values)
        m = sum([(data[i] - mean_x) * (values[i] - mean_y) for i in range(len(data))]) / \
                            sum([(data[i] - mean_x) ** 2 for i in range(len(data))]) #Calculates slope of best fit line.

        b = mean_y - m * mean_x #Calculates y-intercept.
        
        r = sum([(data[i] - mean_x) * (values[i] - mean_y) for i in range(len(data))]) / \
                np.sqrt(sum([(data[i] - mean_x) ** 2 for i in range(len(data))]) * sum([(values[i] - mean_y) ** 2 for i in range(len(data))]))
        cov = r * np.std(data) * np.std(values) #Finds "r" value and "cov" value.

        ax.plot([min(data), max(data)], [m * min(data) + b, m * max(data) + b], label = "r =" + str(round(r, 2)) + ", cov = " + str(round(cov, 2)), color = "red")
        ax.legend()

    plt.savefig(filename, format = "png")
    plt.close(fig)


def box_plot(data, values, title, x_name, y_name, filename):
    '''
    Creates a box plot.
    Parameter data: List containing x-axis tick names.
    Parameter values: List containing lists of values to be plotted.
    Parameter title: Chart title
    Parameter x_name: X-axis label.
    Parameter y_name: Y-axis label.
    Parameter filename: Name of output file.
    '''
    fig, ax = plt.subplots()
    ax.boxplot(values, zorder = 3)

    ax.set_ylabel(y_name)
    ax.set_xlabel(x_name)
    ax.set_title(title)
    ax.set_xticklabels(data)
    ax.grid(zorder = 0)

    plt.savefig(filename, format = "png")
    plt.close(fig)
    

def multiple_bar_chart(graph1, graph2, graph3, x_values, title, x_name, y_name, filename):
    '''
    Creates a scatter plot.
    Parameter graph1: Y values to be graphed.
    Parameter graph2: Y values to be graphed.
    Parameter graph3: Y values to be graphed.
    Parameter x_values: X axis tick labels.
    Parameter title: Chart title
    Parameter x_name: X-axis label.
    Parameter y_name: Y-axis label.
    Parameter filename: Name of output file.
    '''
    width = 0.2  # the width of the bars
    ind = np.arange(len(x_values)) #Creates x-tick values.

    fig, ax = plt.subplots()
    ax.bar(ind - width, graph1, width, color='Blue', label='US')
    ax.bar(ind, graph2, width, color='Red', label='Europe')
    ax.bar(ind + width, graph3, width, color='Green', label='Japan')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_name)
    ax.set_xlabel(x_name)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(x_values)
    ax.legend()

    plt.savefig(filename, format = "png")
    plt.close(fig)

def round_down(num, divisor):
    '''
    Takes a number and rounds it down to the nearest multiple of the given number.
    Parameter num: Number to be rounded down.
    Parameter divisor: Multiple to be rounded down to.
    Returns: Rounded number..
    '''
    return num - (num%divisor)