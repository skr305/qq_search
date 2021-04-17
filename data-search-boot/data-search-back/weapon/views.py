from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def get_weapon_info(request, name, year):
    if(name == "mp5"):
        return HttpResponse(name + ', ' + 'made in Germany,with high shooting speed and a good applicability --' + str(year))
    elif(name == "Yukiro"):
        return HttpResponse(name + ', ' + 'made in Japan, has a large amount of drainage, equiping 4 large bore [305mm] chase gun) --' + str(year))
    else:
        return HttpResponse(name + ', ' + 'no data about it is known now ' + '--' + str(year))     
        