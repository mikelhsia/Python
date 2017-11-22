from django.shortcuts import render
import tushare as ts
import json
from django.http import HttpResponse

def goToHomeIndex(request):
	print("We're in the page")
	return render(request, 'home.html')


def goToHomeIndexDataSet(request):
	# print("We're in the ajax!")
	if request.method == "POST":
		code = request.POST['code']
		# print("Code: {}".format(code))
		try:
			close = ts.get_hist_data(code, start='2017-10-01', end='2017-11-20')
			return HttpResponse(json.dumps(close.close.tolist()))
		except:
			return HttpResponse([])
