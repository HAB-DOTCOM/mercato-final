from .models import catagory


def menu_links(request):
	links=catagory.objects.all()
	return dict(links=links)