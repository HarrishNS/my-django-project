from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

from .models import Follow

User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def follow_user(request):
    try:
        data = json.loads(request.body)
        follower_id = data.get("follower_id")
        followed_id = data.get("followed_id")

        if not follower_id or not followed_id:
            return JsonResponse({"error": "follower_id and followed_id are required"}, status=400)

        if follower_id == followed_id:
            return JsonResponse({"error": "Cannot follow yourself."}, status=400)

        follower = get_object_or_404(User, id=follower_id)
        followed = get_object_or_404(User, id=followed_id)

        follow, created = Follow.objects.get_or_create(follower=follower, followed=followed)
        if not created:
            return JsonResponse({"message": "Already following."})

        return JsonResponse({"message": "Followed successfully."}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def unfollow_user(request):
    try:
        data = json.loads(request.body)
        follower_id = data.get("follower_id")
        followed_id = data.get("followed_id")

        if not follower_id or not followed_id:
            return JsonResponse({"error": "follower_id and followed_id are required"}, status=400)

        follow = Follow.objects.filter(follower_id=follower_id, followed_id=followed_id)
        if follow.exists():
            follow.delete()
            return JsonResponse({"message": "Unfollowed successfully."})
        else:
            return JsonResponse({"message": "Not following the user."}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_follow_data(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)

        followers_qs = user.followers.select_related('follower')
        following_qs = user.following.select_related('followed')

        followers = list(followers_qs.values_list('follower__email', flat=True))
        following = list(following_qs.values_list('followed__email', flat=True))

        return JsonResponse({
            "user_id": user.id,
            "email": user.email,
            "followers_count": len(followers),
            "following_count": len(following),
            "followers": followers,
            "following": following
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Create your views here.
