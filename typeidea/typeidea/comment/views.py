from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView

# 验证码
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import JsonResponse
from django.utils import timezone

from .forms import CommentForm
# Create your views here.

# 评论
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        
        # 验证&保存
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
            
            context = {
                'succeed': succeed,
                'form': comment_form,
                'target': target,
            }
            return self.render_to_response(context)


# 评论验证码接口
# class VerifyCaptcha(View):
#     # 在get函数中生成图片验证码
#     def get(self, request):
#         # 存储生成密钥存入id
#         captcha_id = CaptchaStore.generate_key()
#         return JsonResponse({
#             'captcha_id': captcha_id,
#             'image_src':captcha_image_url(captcha_id),
#         })
#     # 在post函数中校验验证码以及清理掉验证通过的验证码
#     def post(self, request):
#         captcha_id = request.POST.get('captcha_id')
#         chaptcha = request.POST.get('captcha', '')
#         captcha = captcha.lower()

#         try:
#             CaptchaStore.objects.get(response = captcha, hashkey=captcha_id,
#             expiration_gt=timezone.now()).delete()
#             # 存储不存在
#         except CaptchaStore.DoesNotExist:
#             return JsonResponse({'msg': '验证码错误'}, status=400)
        
#         return JsonResponse({})

