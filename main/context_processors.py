from .models import Tred


def searchFunction(request):
    context = {}
    treds = Tred.objects.all()

    if "search" in request.GET:
        query = request.GET.get("q")

        search_box = request.GET.get("search-box")
        if search_box == 'Всё':
            objects = treds.filter(title__icontains=query).union(treds.filter(content__icontains=query))
        else:
            if search_box == 'Описание':
                objects = treds.filter(content__icontains=query)
            else:
                objects = treds.filter(title__icontains=query)

        context = {
            "objects": objects,
            "query": query,
        }

    return context
