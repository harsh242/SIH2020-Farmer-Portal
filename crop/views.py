from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Crop, Category, Types
from .forms import CropForm, BidForm
from django.urls import reverse, reverse_lazy
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone

@login_required
def post_create(request):
    form = CropForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.farmer = request.user
        instance.save()
        form.save_m2m()
        return redirect('crop:home')
    context = {
        "form": form,
    }
    return render(request, "crop/post_form.html", context)

class UserPostListView(ListView):
    model = Crop
    template_name = 'crop/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Crop.objects.filter(farmer=user).order_by('-date_posted')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Crop
    fields = ('farmer', 'cat', 'name', 'quantity', 'unit', 'description', 'pickup', 'image')
    success_url = reverse_lazy('crop:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.farmer:
            return True
        return False

@login_required
def post_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    crop.delete()
    return redirect('crop:home')

def buy(request, pk):
    object = get_object_or_404(Post, pk=pk)
    object.owner = request.user
    object.save()
    return redirect('core:post-detail', pk) 

def post_detail(request, pk):
    object = get_object_or_404(Crop, pk=pk)
    now = timezone.now()
    bids = Crop.objects.all()
    bids = bids.filter(stuff=object)
    highest = (None,None)
    if bids:
        high = {}
        for i in bids:
            high[int(i.value)]=i.author
        sorted_d = sorted(high.items(), key=operator.itemgetter(0),reverse=True)
        highest = sorted_d[0]
    form = BidForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.stuff = object
        instance.save()
        form.save_m2m()
        return redirect('crop:post-detail', pk)
    context = {
        "form": form,
        "now": now,
        "object": object,
        "highest": highest[0],
        "bidder": str(highest[1]),
        }

def home(request):
    posts = Crop.objects.all()
    posts = posts[::-1]
    recent_posts = posts[:4]
    context = {
        'posts': posts,
        'recent_posts': recent_posts,
    }
    return render(request, 'crop/home.html', context)
