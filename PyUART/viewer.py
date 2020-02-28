from utils import *
import pandas as pd
from openpyxl.chart import LineChart,Reference,Series
from openpyxl import load_workbook


if __name__ == "__main__":
    start_time = time.time()
    params = ['strategy','foresight','learning rate','hyper','cool']
    executor_filename = 'executor_report.xls'
    steps_filename = 'steps_ev.xlsx'
    loss_filename = 'loss_ev.xlsx'
    rev_loss_filename = 'reverse_loss_ev.xlsx'
    data = {'executor': [*['' for k in params],*[i for i in list(np.loadtxt(executor_filename, 'int'))][:-1]]}
    loss = {}

    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['target'] == 'prediction':
            data.update({i['prefix'] :   [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'int', delimiter=',')[:,0])]})
            loss.update({i['prefix'] : [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'float', delimiter=',')[:,1])]})
    index = [*params,*[i for i in range(1,len(data['executor'])-len(params)+1)]]

    df = pd.DataFrame(data,index=index)
    df.to_excel(steps_filename)
    output('[Upd]'+steps_filename)
    print('Steps to fall\n',df)
    tf = pd.DataFrame(loss, index=index)
    tf.to_excel(loss_filename)
    output('[Upd]'+loss_filename)
    print('Loss function\n',tf)
    
    report = load_workbook(filename=loss_filename)     
    sheet = report.active 
    chart = LineChart()
    k = 2
    for i in loss:
        values = Reference(sheet, min_col = k, min_row = len(params) + 2, max_row = sheet.max_row)
        series = Series(values , title = i)
        chart.series.append(series)
        k += 1
    chart.title = " Absolute value of loss function (prediction)"
    chart.x_axis.title = " Iteration "
    chart.y_axis.title = " Loss function "
    sheet.add_chart(chart, "H2") 
    report.save(loss_filename)
    output('[Upd]'+loss_filename)
    output('Charts plotted.')
    
    rev_loss = {}
    for i in CONFIG: 
        if i['target'] == 'reverse':
            rev_loss.update({i['prefix'] : [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'float', delimiter=','))]})
   
    tf = pd.DataFrame(rev_loss, index=index)
    tf.to_excel(rev_loss_filename)
    output('[Upd]'+rev_loss_filename)
    print('Loss function\n',tf)
    
    report = load_workbook(filename=rev_loss_filename)     
    sheet = report.active 
    chart = LineChart()
    k = 2
    for i in loss:
        values = Reference(sheet, min_col = k, min_row = len(params) + 2, max_row = sheet.max_row)
        series = Series(values , title = i)
        chart.series.append(series)
        k += 1
    chart.title = " Absolute value of loss function (reverse)"
    chart.x_axis.title = " Iteration "
    chart.y_axis.title = " Loss function "
    sheet.add_chart(chart, "H2") 
    report.save(rev_loss_filename) 
    output('[Upd]'+rev_loss_filename)
    output('Charts plotted.')
    
    output('Session of viewer.py ended in ','time',time.time()-start_time)  