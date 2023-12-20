from user.models import User
from post.models import Post, Image, Comment
from room.models import Group, Message
from chat.models import Chat, Image
from django.views import generic
from itertools import chain
from django.db.models import Q

class SearchResultsView(generic.ListView):
    template_name = "search_results.html"

    # def get_queryset(self):  # new
    #     query = self.request.GET.get("q")
    #     object_list = User.objects.filter(Q(username__icontains=query))
    #     return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        results = []
        qs = None
        object_list2= Post.objects.filter(Q(user__username__icontains=query) | Q(caption__icontains=query))
        object_list1 = Group.objects.filter(Q(message_room__icontains=query) | Q(message_room__body__icontains=query))
        object_list3 = Message.objects.filter(Q(user__icontains=query) | Q(body__icontains=query))
        
        results.append(object_list2)
        results.append(object_list1)
        
        if len(results)>0:
            qs = sorted(chain(*results), reverse=True, key=lambda obj: obj.created_at)
        context['result'] = qs

        return context