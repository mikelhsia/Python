from django.shortcuts import render, get_object_or_404
from .models import PeekabooCollection, PeekabooMoment

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def collection_list(request):
	collection_list = PeekabooCollection.objects.all()

	# 10 collection per page
	paginator = Paginator(collection_list, 10)

	# We get the page GET parameter that indicates the current page number.
	page = request.GET.get('page')
	try:
		collections = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		collections = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of result
		collections = paginator.page(paginator.num_pages)
	return render(request, 'collection/collection_list.html', {'page': page, 'collections': collections})

def collection_detail(request, collection_id):
	collection = get_object_or_404(PeekabooCollection, id=collection_id)
	return render(request, 'collection/collection_detail.html', {'collection': collection})