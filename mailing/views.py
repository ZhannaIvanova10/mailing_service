from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Mailing, Client, Message
from .forms import MailingForm, ClientForm, MessageForm

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return Mailing.objects.all()  # Временно показываем все рассылки

class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'
    
    # Временно убираем фильтрацию
    # def get_queryset(self):
    #     return Mailing.objects.filter(owner=self.request.user)

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    
    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    
    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)
# Клиенты
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'
    
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')
    
    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)
# Сообщения
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'
    
    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    
    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')
    
    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)
# Попытки (заглушка)
class AttemptListView(LoginRequiredMixin, ListView):
    template_name = 'mailing/attempt_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return []

# Главная страница
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'mailing/home.html')
    
    # Получаем рассылки пользователя
    user_mailings = Mailing.objects.filter(owner=request.user)
    
    context = {
        'total_mailings': Mailing.objects.filter(owner=request.user).count(),
        'active_mailings': Mailing.objects.filter(owner=request.user, status='started').count(),
        'total_clients': Client.objects.filter(owner=request.user).count(),
        'user_mailings': user_mailings,
    }
    return render(request, 'mailing/home.html', context)

@login_required
def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
    from django.contrib import messages
    messages.success(request, f'Рассылка "{mailing.message.subject}" запущена!')
    return redirect('mailing:mailing_detail', pk=pk)
