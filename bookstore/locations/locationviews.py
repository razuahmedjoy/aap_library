from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import codecs
import json

def get_districts(request):
    districtFile = codecs.open("bookstore/locations/districts.json","r",encoding="utf8")
    listDistricts = json.load(districtFile)
  
    return JsonResponse({"data":listDistricts})


def get_area(request):
  areaFiles = codecs.open("bookstore/locations/areasFinal.json","r",encoding="utf8")
  list_area = json.load(areaFiles)
  
  filtered_area = []
  if "district_id" in request.GET:

    district_id = int(request.GET["district_id"])
    
    filtered_area = list(filter(lambda d: d['cityId'] == district_id, list_area))

    
    return JsonResponse({"data":filtered_area})
