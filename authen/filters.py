import django_filters

from authen.models import User

from calori.models import Calo

class calo_Filter(django_filters.FilterSet):
     class Meta:
        model =  Calo
        fields= {
                'name':['icontains'],'calories':['exact'],
                 'limt_reach':['exact'],
                 'quantity':['exact'],'created_at':['icontains']
                 }    


class user_Filter(django_filters.FilterSet):
    class Meta:
        model =User
        fields ={'username':['icontains'],'id':['exact']}