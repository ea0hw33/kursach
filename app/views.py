import datetime
import json
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.forms import modelformset_factory
from django.views.generic.edit import FormMixin, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout

from app.forms import *

from app.models import *



def logout_view(request):
    logout(request)
    return redirect('login')
    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.add_message(request, messages.ERROR,'Аккаунт не активен')  
                    return render(request, 'login.html', {'form': form})

            else:
                messages.add_message(request, messages.ERROR,'Неверный логин или пароль')  
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



class NIRview(ListView):
    model = NIR
    template_name = "nir_list.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NIRview, self).get_context_data(**kwargs)
        context["facultys"] = Fakultety.objects.all()
        return context  
    
    def get_queryset(self) -> QuerySet[Any]:
        
 
        available_years = []
        for i in NIR.objects.all():
            if i.date_start.year not in available_years:
                available_years.append(i.date_start.year)
        
        faculty = self.request.GET.get('faculty', [i.id for i in Fakultety.objects.all()])
        if type(faculty) is str:
            faculty = [faculty]
        type_nir = self.request.GET.get('type', ['vs', 'ol', 'kf'])
        if type(type_nir) is str:
            type_nir = [type_nir]
            
        if 'dateFilterType' in self.request.GET and self.request.GET['dateFilterType'] == 'day':
            dateformat = '%Y-%m-%d'
            date = self.request.GET['dateFilter']
            date = datetime.datetime.strptime(date, dateformat)
            new_context = NIR.objects.order_by('-date_start').filter(
                Fakultet__id__in=faculty,
                type__in = type_nir, 
                date_start__year = date.year,
                date_start__month = date.month,
                date_start__day = date.day
            )
        else:
            year = self.request.GET.get('dateFilter', available_years)
            if type(year) is str:
                year = [int(year)]
            new_context = NIR.objects.order_by('-date_start').filter(
                Fakultet__id__in=faculty,
                type__in = type_nir, 
                date_start__year__in = year
            )
        
        return new_context

    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.user_type != 'department_head':
            return super().get(request, *args, **kwargs)   
        else:
            return redirect('forhead')
    
class NIRviewHead(ListView):
    model = NIR
    template_name = "nir_list_head.html"
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.user_type == 'department_head':
            return super().get(request, *args, **kwargs)   
        else:
            return redirect('index')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NIRviewHead, self).get_context_data(**kwargs)
        context["facultys"] = Fakultety.objects.all()
        context["participants"] = []
        context["listeners"] = []
        context["orgcomit"] = []
        context["participants2"] = {}
        context["listeners2"] = {}
        context["orgcomit2"] = {}
        for nir in NIR.objects.all():
            for participant in uchastnikyOnNIR.objects.filter(nir = nir):
                if participant.isParticipent:
                    context["participants"].append(participant)
                    context["participants2"][nir.pk] = True
                else:
                    context["listeners"].append(participant)
                    context["listeners2"][nir.pk] = True
            
            for participant in orgkomitety.objects.filter(nir = nir):
                if participant.isParticipent:
                    context["participants"].append(participant)
                    context["participants2"][nir.pk] = True
                if participant.isAgent:
                    context["orgcomit"].append(participant)
                    context["orgcomit2"][nir.pk] = True
                if not participant.isParticipent and not participant.isAgent:
                    context["listeners"].append(participant)
                    context["listeners2"][nir.pk] = True
        
        return context  
    
    def get_queryset(self) -> QuerySet[Any]:
        
 
        available_years = []
        for i in NIR.objects.all():
            if i.date_start.year not in available_years:
                available_years.append(i.date_start.year)
        
        faculty = self.request.GET.get('faculty', [i.id for i in Fakultety.objects.all()])
        if type(faculty) is str:
            faculty = [faculty]
        type_nir = self.request.GET.get('type', ['vs', 'ol', 'kf'])
        if type(type_nir) is str:
            type_nir = [type_nir]
            
        if 'dateFilterType' in self.request.GET and self.request.GET['dateFilterType'] == 'day':
            dateformat = '%Y-%m-%d'
            date = self.request.GET['dateFilter']
            date = datetime.datetime.strptime(date, dateformat)
            new_context = NIR.objects.order_by('-date_start').filter(
                Fakultet__id__in=faculty,
                type__in = type_nir, 
                date_start__year = date.year,
                date_start__month = date.month,
                date_start__day = date.day
            )
        else:
            year = self.request.GET.get('dateFilter', available_years)
            if type(year) is str:
                year = [int(year)]
            new_context = NIR.objects.order_by('-date_start').filter(
                Fakultet__id__in=faculty,
                type__in = type_nir, 
                date_start__year__in = year
            )
        
        return new_context


    
class NIRregister(DetailView):
    model = NIR
    template_name = "participateInNIR.html"
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        nir = self.get_object()
        data = dict(request.POST)
        context = super(NIRregister, self).get_context_data(**kwargs)
        context['user'] = request.user
        
        if request.user.user_type == 'student':
            context['job'] = 'student'
            student = studenty.objects.get(user = request.user)
            isParticipent = "participantCheckbox" in data
            if isParticipent:
                role = "Участник"
            else:
                role = "Слушатель"
            record = uchastnikyOnNIR.objects.filter(nir=nir, user = student)
            if len(record) != 0:
                isParticipent = record[0].isParticipent
                if isParticipent:
                    role = "Участник"
                else:
                    role = "Слушатель"
                context['messagess'] = f'''{student.user.first_name} {student.user.last_name}, 
                вы были уже записаны на мероприятие в качестве {role},
                чтобы удалить запись, <a href=\"{reverse('participateINNIR', kwargs={'pk': nir.pk})}?deleteRecordst={record[0].pk}">нажмите сюда</a>
                '''
                messages.add_message(self.request, messages.SUCCESS, context['messagess'])   
            else: 
                uchastnikyOnNIR.objects.create(user = student, 
                                    nir =nir, isParticipent= isParticipent)
                context['messagess'] = f'''{student.user.first_name} {student.user.last_name}, 
                вы были записаны на мероприятие как {role}'''
                messages.add_message(self.request, messages.SUCCESS, context['messagess'])
                
        elif request.user.user_type == 'employee':
            context['job'] = 'employee'
            employee = sotrudnikyiOnKafedra.objects.get(user = request.user)
            isParticipent = "participantCheckbox" in data
            isAgent = "committeeCheckbox" in data
            
            if isParticipent:
                role = "участника"
                if isAgent:
                    role = "участника и представителя оргкомитета"
            elif isAgent:
                role = "представителя оргкомитета"
            else:
                role = "слушателя"
                
            record = orgkomitety.objects.filter(nir=nir, user = employee)
            if len(record) != 0:
                isParticipent = record[0].isParticipent
                isAgent = record[0].isAgent
                if isParticipent:
                    role = "участника"
                    if isAgent:
                        role = "участника и представителя оргкомитета"
                elif isAgent:
                    role = "представителя оргкомитета"
                else:
                    role = "слушателя"
                context['messagess'] = f'''{employee.user.first_name} {employee.user.last_name}, 
                вы были уже записаны на мероприятие в качестве {role},
                чтобы удалить запись, <a href=\"{reverse('participateINNIR', kwargs={'pk': nir.pk})}?deleteRecord={record[0].pk}">нажмите сюда</a>
                '''
                messages.add_message(self.request, messages.SUCCESS, context['messagess'])
            else:
                orgkomitety.objects.create(nir = nir, user = employee,
                                        isParticipent = isParticipent,
                                        isAgent = isAgent)
                context['messagess'] = f'''{employee.user.first_name} {employee.user.last_name}, 
                вы были записаны на мероприятие в качестве {role}'''
                messages.add_message(self.request, messages.SUCCESS, context['messagess'])
        return render(request, self.template_name, context=context)
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data = dict(request.GET)
        if 'deleteRecord' in data:
            orgkomitety.objects.filter(pk=int(data['deleteRecord'][0])).delete()
        elif 'deleteRecordst' in data:
            uchastnikyOnNIR.objects.filter(pk=int(data['deleteRecordst'][0])).delete()
        
        return super().get(request, *args, **kwargs)