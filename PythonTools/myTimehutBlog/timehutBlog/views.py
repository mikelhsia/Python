from django.shortcuts import render, get_object_or_404
from .models import PeekabooCollection, PeekabooMoment

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .form import EmailCollectionForm
from django.core.mail import send_mail

# This class-based view is analogous to the previous post_list view.
class CollectionView(ListView):
	'''
		- Use a specific queryset instead of retrieving all objects. Instead of defining a queryset attribute, we could
		have specified model = Post and Django would have built the generic Post.objects.all() queryset for us.
		- Use the context variable posts for the query results. The default variable is object_list if we don't specify any context_object_name.
		- Paginate the result displaying three objects per page.
		- Use a custom template to render the page. If we don't set a default template, ListView will use blog/post_list.html.”
	'''
	queryset = PeekabooCollection.objects.all()
	context_object_name = 'collections'
	paginate_by = 5
	template_name = 'collection/collection_list.html'

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

	# thumbnails = [PeekabooMoment.objects.filter(event=x.id)[0].src_url for x in collections]
	# return render(request, 'collection/collection_list.html', {'page': page, 'collections': collections, 'thumbnails': thumbnails})

	return render(request, 'collection/collection_list.html', {'page': page, 'collections': collections})



def collection_detail(request, collection_id):
	collection = get_object_or_404(PeekabooCollection, id=collection_id)
	moment_list = PeekabooMoment.objects.filter(event=collection_id)
	return render(request, 'collection/collection_detail.html', {'collection': collection, 'moment_list': moment_list})


def collection_share(request, collection_id):
	# Retrieve collection by id
	collection = get_object_or_404(PeekabooCollection, id=collection_id)
	sent = False

	if request.method == 'POST':
		# Form was submitted
		form = EmailCollectionForm(request.POST)

		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data

			# ... send email
			# collection_url = request.build_absolute_uri(collection.get_absolute_url())
			subject = f"{cd['name']} ({cd['email']}) recommends you reading {collection.id}"
			message = f"{collection.caption}"
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
	else:
		form = EmailCollectionForm()

	# TODO: SMTPServerDisconnected: Connection unexpectedly closed need to be resolved
	return render(request, 'collection/share.html', {'collection': collection, 'form': form, 'sent': sent})
