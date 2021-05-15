from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def posts_communication_system(request, post_id):
    try:
        post = request.user.posts_joined.get(id=post_id)
    except:
        return HttpResponseForbidden()
    return render(request, 'communicationsystem/socket.html', {'post': post})
