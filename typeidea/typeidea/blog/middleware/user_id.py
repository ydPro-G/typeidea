import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10

# user_id 中间件
class UserIDMiddleware:
    # 接受请求
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 生成uid
        uid = self.generate_uid(request)
        # 将uid赋值给request对象，因为request是类的实例，可以动态赋值
        # 后面的view可以拿到uid并使用
        request.uid = uid
        response = self.get_response(request)
        # 设置cookie，httponly(只在服务端访问)，这样用户在访问就会带上同样的uid
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response
    
    # 如果没有这个uid就生成新的uid
    def generate_uid(self,request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid