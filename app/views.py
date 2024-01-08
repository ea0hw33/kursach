import json
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView
from django.db.models import Count
from django.forms import modelformset_factory
from django.views.generic.edit import FormMixin, FormView
from django.contrib import messages

from app.models import *


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
        year = self.request.GET.get('year', available_years)
        if type(year) is str:
            year = [int(year)]
        
    
        new_context = NIR.objects.filter(
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
        
        if "studentId" in data:
            context['job'] = 'student'
            student = None
            isParticipent = "participantCheckbox" in data
            try:
                student = studenty.objects.get(num_zachetka = int(data['studentId'][0]))
            except Exception:
                messages.add_message(self.request, messages.ERROR, 'Студент не найден')
                context['messagess'] = 'Студент не найден'
            else:
                if isParticipent:
                    role = "Участник"
                else:
                    role = "Слушатель"
                record = uchastnikyOnNIR.objects.filter(nir=nir, student = student)
                if len(record) != 0:
                    isParticipent = record[0].isParticipent
                    if isParticipent:
                        role = "Участник"
                    else:
                        role = "Слушатель"
                    context['messagess'] = f'''{student.name} {student.surename}, 
                    вы были уже записаны на мероприятие в качестве {role},
                    чтобы удалить запись, <a href=\"{reverse('participateINNIR', kwargs={'pk': nir.pk})}?deleteRecordst={record[0].pk}">нажмите сюда</a>
                    '''
                    messages.add_message(self.request, messages.SUCCESS, context['messagess'])   
                else: 
                    uchastnikyOnNIR.objects.create(student = student, 
                                        nir =nir, isParticipent= isParticipent)
                    context['messagess'] = f'''{student.name} {student.surename},
                    вы были записаны на мероприятие как {role}'''
                    messages.add_message(self.request, messages.SUCCESS, context['messagess'])
        elif "employeeId" in data:
            context['job'] = 'employee'
            employee = None
            isParticipent = "participantCheckbox" in data
            isAgent = "committeeCheckbox" in data
            try:
                employee = sotrudnikyiOnKafedra.objects.get(pk = int(data['employeeId'][0]))
            except Exception:
                messages.add_message(self.request, messages.ERROR, 'Сотрудник не найден')
                context['messagess'] = 'Сотрудник не найден'
            else:
                if isParticipent:
                    role = "участника"
                    if isAgent:
                        role = "участника и представителя оргкомитета"
                elif isAgent:
                    role = "представителя оргкомитета"
                else:
                    role = "слушателя"
                    
                record = orgkomitety.objects.filter(nir=nir, sotrudnik = employee)
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
                    context['messagess'] = f'''{employee.name} {employee.surename}, 
                    вы были уже записаны на мероприятие в качестве {role},
                    чтобы удалить запись, <a href=\"{reverse('participateINNIR', kwargs={'pk': nir.pk})}?deleteRecord={record[0].pk}">нажмите сюда</a>
                    '''
                    messages.add_message(self.request, messages.SUCCESS, context['messagess'])
                else:
                    orgkomitety.objects.create(nir = nir, sotrudnik = employee,
                                            isParticipent = isParticipent,
                                            isAgent = isAgent)
                    context['messagess'] = f'''{employee.name} {employee.surename}, 
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