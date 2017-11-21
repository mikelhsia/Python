from django.shortcuts import render
import tushare as ts
import json

def goToHomeIndex(request):
	close = ts.get_hist_data("002594", start='2017-10-01', end='2017-11-20')
	return render(request, 'home.html', {'byd_close_list': json.dumps(close.close.tolist())})