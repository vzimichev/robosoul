from utils import *
import pandas as pd
from openpyxl.chart import LineChart,Reference,Series
from openpyxl import load_workbook


if __name__ == "__main__":
    start_time = time.time()
    params = ['strategy','foresight','learning rate','hyper','cool']
    executor_filename = 'executor_report.xls'
    steps_filename = 'steps_ev.xlsx'
    target_filename = 'target_ev.xlsx'
    rev_target_filename = 'reverse_target_ev.xlsx'
    data = {'executor': [*['' for k in params],*list(np.loadtxt(executor_filename, 'int'))]}
    target = {}

    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['target'] == 'prediction':
            data.update({i['prefix'] :   [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'int', delimiter=',')[:,0])]})
            target.update({i['prefix'] : [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'float', delimiter=',')[:,1])]})
    index = [*params,*[i for i in range(1,len(data['executor'])-len(params)+1)]]

    df = pd.DataFrame(data,index=index)
    df.to_excel(steps_filename)
    output('[Upd]'+steps_filename)
    print('Steps to fall\n',df)
    tf = pd.DataFrame(target, index=index)
    tf.to_excel(target_filename)
    output('[Upd]'+target_filename)
    print('Target function\n',tf)
    
    report = load_workbook(filename=target_filename)     
    sheet = report.active 
    chart = LineChart()
    k = 2
    for i in target:
        values = Reference(sheet, min_col = k, min_row = len(params) + 2, max_row = sheet.max_row)
        series = Series(values , title = i)
        chart.series.append(series)
        k += 1
    chart.title = " Absolute value of target function (prediction)"
    chart.x_axis.title = " Iteration "
    chart.y_axis.title = " Target function "
    sheet.add_chart(chart, "H2") 
    report.save(target_filename)
    output('[Upd]'+target_filename+'\nCharts plotted.')
    
    rev_target = {}
    for i in CONFIG: 
        if i['target'] == 'reverse':
            rev_target.update({i['prefix'] : [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'float', delimiter=','))]})
   
    tf = pd.DataFrame(rev_target, index=index)
    tf.to_excel(rev_target_filename)
    output('[Upd]'+rev_target_filename)
    print('Target function\n',tf)
    
    report = load_workbook(filename=rev_target_filename)     
    sheet = report.active 
    chart = LineChart()
    k = 2
    for i in target:
        values = Reference(sheet, min_col = k, min_row = len(params) + 2, max_row = sheet.max_row)
        series = Series(values , title = i)
        chart.series.append(series)
        k += 1
    chart.title = " Absolute value of target function (reverse)"
    chart.x_axis.title = " Iteration "
    chart.y_axis.title = " Target function "
    sheet.add_chart(chart, "H2") 
    report.save(rev_target_filename) 
    output('[Upd]'+rev_target_filename+'\nCharts plotted.')
    
    output('Session of viewer.py ended in ','time',time.time()-start_time)  