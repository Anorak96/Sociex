from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Group, Message
from django.views import generic
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from user.models import User
from .forms import GroupForm, MessageForm
# Create your views here.

class RoomsView(generic.ListView):
    template_name = 'room/rooms.html'
    model = Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        context['groups'] = Group.objects.all()
        user = User.objects.get(pk=self.request.user.pk) # get object of logged in user
        groups = Group.objects.all().filter(members=user)
        context['grouped'] = groups
        grp_mess = []
        qs = None
        #=== Group message==
        for group in groups:
            u_group = group.message_room.all()  # type: ignore
            grp_mess.append(u_group)
        #=== sort and chain messages query===
        if len(grp_mess)>0:
            qs = sorted(chain(*grp_mess), reverse=True, key=lambda obj: obj.created_at)
        context['grp_msgs'] = qs
        return context
    
class RoomDetailView(generic.DetailView):
    model = Group
    template_name = "room/room.html"

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        context['group'] = Group.objects.get(pk=pk_)
        return context

class GroupCreateView(LoginRequiredMixin, generic.View):
    template_name = 'room/create.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = GroupForm()
        return render(request, self.template_name, context={'form':form })

    def post(self, request):
        form = GroupForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = user
            instance.save()
            instance.mods.add(user)
            instance.members.add(user)
            group = Group.objects.get(pk=instance.pk)
            return redirect(group.get_absolute_url())
        else:
            print(form.errors)
        context = {'form': form,}
        return render(request, self.template_name, context)
    
class MessageCreateView(LoginRequiredMixin, generic.View):
    template_name = 'room/room.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = MessageForm()
        return render(request, self.template_name, context={'form':form })

    def post(self, request):
        form = MessageForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.room = Group.objects.get(id=request.POST.get('group_message'))
            instance.save()
            mssage = Message.objects.get(pk=instance.pk)
            group = mssage.room.pk
            return redirect(group.get_absolute_url())
        else:
            print(form.errors)
        context = {'form': form,}
        return render(request, self.template_name, context)

class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Group
    template_name = 'room/group_delete.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        return reverse('room:groups')

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        group = Group.objects.get(pk=pk_)
        return group.created_by == self.request.user
    
class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Message
    template_name = 'room/message_delete.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        mess = Message.objects.get(pk=pk)
        mess_group = mess.room
        return reverse('room:group', kwargs={"pk": mess_group.pk})

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        messge = Message.objects.get(pk=pk_)
        return messge.user == self.request.user

class GroupJoinView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to' 

    def post(self, request, pk):
        pk_ = request.POST.get('prof_pk')
        group = Group.objects.get(pk=pk_)
        if self.request.user == group.members.all():
            group.members.remove(self.request.user)
        else:         
            group.members.add(self.request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    
class GroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Group    
    form_class = GroupForm
    template_name = 'room/group_update.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse('room:group', kwargs={"pk": pk})

    def form_valid(self, form):
        pk = self.kwargs['pk']
        group = Group.objects.get(pk=pk)
        if form.instance.created_by == self.request.user:
            form.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'You are not the owner of the group!')
            return super().form_invalid(form)
    
    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        group = Group.objects.get(pk=pk_)
        return group.created_by == self.request.user
    
class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Message    
    form_class = MessageForm
    template_name = 'room/message_update.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        mess = Message.objects.get(pk=pk)
        mess_group = mess.room
        return reverse('room:group', kwargs={"pk": mess_group.pk})

    def form_valid(self, form):
        pk = self.kwargs['pk']
        mess = Message.objects.get(pk=pk)
        if form.instance.user == self.request.user:
            form.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'You are not the owner of the Message!')
            return super().form_invalid(form)
    
    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        mess = Message.objects.get(pk=pk_)
        return mess.user == self.request.user