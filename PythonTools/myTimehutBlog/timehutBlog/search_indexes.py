from haystack import indexes
from .models import PeekabooCollection, PeekabooMoment

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # Every SearchIndex requires that one of its fields has document=True. The convention is to name this
	# field text. This field is the primary search field. With use_template=True, we
	# are telling Haystack that this field will be rendered to a data template to build the
	# document the search engine will index.
	text = indexes.CharField(document=True, use_template=True)
	
	# publish = indexes.DateTimeField(model_attr='publish')

	def get_model(self):
		return PeekabooCollection

	def index_queryset(self, using=None):
		return self.get_model().all()
