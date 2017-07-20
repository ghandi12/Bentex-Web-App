# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.db import connections

import pandas as pd

# Create your views here.
def home(request):
	numbers = [1,2,3,4,5]
	name = 'Max Goodridge'
	args = {'myName': name, 'numbers': numbers}
	return render(request, 'accounts/home.html', args)

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/account')
	else:
		form = UserCreationForm()
		args = {'form': form}
		return render(request, 'accounts/reg_form.html', args)

def profile(request):
	args = {'user': request.user}
	
	return render(request, 'accounts/profile.html', args)

# @login_required()
# def test_page(request):
# 	return render(request, 'accounts/test.html')

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def assign_code(my_list):
    results_dict = {}
    code_810_list = [i for i in my_list if i['DOCTYPE'] == 810]
    code_404_list = [i for i in my_list if i['DOCTYPE'] == 404]
    code_856_list = [i for i in my_list if i['DOCTYPE'] == 856]

    results_dict['code_810'] = code_810_list
    results_dict['code_404'] = code_404_list
    results_dict['code_856'] = code_856_list
    
    return results_dict

def get_table_names():
    '''returns a list of table names'''
    with connections['mydb'].cursor() as cursor:
        get_tables_query = '''
        select name from sqlite_master where type = 'table';
        '''
        ex = cursor.execute(get_tables_query)
        tables = []
        for i in ex:
            tables.append(i[0].encode('utf-8'))
    return tables	

# @login_required()
# def test_page(request):
#     with connections['mydb'].cursor() as cursor:
#         tables = get_table_names()
#         all_records = []
#         for table in tables:
#             cursor.execute('SELECT * FROM %s' %(table))
#             table_data = dictfetchall(cursor)
#             for i in table_data:
#                 i[b'Table_Name'] = table
#                 i[b'Record_Set'] = len(table_data)
#                 all_records.append(i)
#         result = assign_code(all_records)
#     return render(request, 'accounts/test.html', context={'result':result})

#from accounts.models import TEST

# @login_required()
# def test_page(request):

#     result = TEST.objects.all()
#     return render(request, 'accounts/test2.html', context={'result':result})

# class Rout(object):
#     def db_for_read(self, model, **hints):
#         return 'mydb'


# @login_required()
# def test_page(request):
#     with connections['mydb'].cursor() as cursor:
#         tables = ['accounts_code_810', 'TEST2']
#         all_records = []
#         result = {}
#         result['ths'] = ['Invoice Number', 'Customer Number', 'Customer Purchase Order Number', 'DOCTYPE']
#         for table in tables:
#             cursor.execute('SELECT * FROM %s' %(table))
#             table_data = dictfetchall(cursor)
#             for i in table_data:
#                 i[b'Table_Name'] = table
                
#                 i[b'Record_Set'] = len(table_data)
#                 all_records.append(i)
        
#    return render(request, 'accounts/test2.html', context=result)

def listfetchall(cursor):
    "Return all rows from a cursor as a list"
    return [
        list(row)
        for row in cursor.fetchall()
    ]

def test_page(request):
    with connections['mydb'].cursor() as cursor:
        tables = ['accounts_code_810', 'TEST2']
        all_records = []
        result = {}
        result['ths'] = ['Invoice Number', 'Customer Number', 'Customer Purchase Order Number', 'DOCTYPE']
        tables_data = []
        names = []
        for table in tables:
            cursor.execute('SELECT * FROM %s' %(table))
            trs = listfetchall(cursor)
            table_data = {'record_set':len(trs), 'trs':trs}
            names.append(table.encode('utf-8'))
            #tables_data[table] = table_data
            table_data = {'name':table,'record_set':len(trs), 'trs':trs}
            tables_data.append(table_data)
        #tables_data['names'] = names
        result['tables_data'] = tables_data
    return render(request, 'accounts/test2.html', context=result)

def get_current_path(request):
    return {
       'current_path': request.get_full_path()
     }
def tables(request):
    with connections['mydb'].cursor() as cursor:
        tables = ['accounts_code_810', 'TEST2']
        all_records = []
        result = {}
        result['ths'] = ['Invoice Number', 'Customer Number', 'Customer Purchase Order Number', 'DOCTYPE']
        tables_data = []
        path = request.get_full_path().split('/')[-1]
        cursor.execute('SELECT * FROM %s' %(path))
        trs = listfetchall(cursor)
        #table_data = {'record_set':len(trs), 'trs':trs}
        table_data = {'record_set':len(trs), 'trs':trs}
        #tables_data.append(table_data)
        result['table_data'] = table_data
    return render(request, 'accounts/tables.html', context=result)
























