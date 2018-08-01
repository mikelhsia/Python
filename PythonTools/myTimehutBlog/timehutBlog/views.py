from django.shortcuts import render, get_object_or_404
from .models import PeekabooCollection, PeekabooMoment

# Create your views here.
def collection_list(request):
	collections = PeekabooCollection.objects.all()
	return render(request, 'collection/collection_list.html', {'collections': collections})

def collection_detail(request, collection_id):
	collection = get_object_or_404(PeekabooCollection, id=collection_id)
	return render(request, 'collection/collection_detail.html', {'collection': collection})