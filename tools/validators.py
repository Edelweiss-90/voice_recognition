def check_req_user_data(data):
    length = 12
    return type(data) is not str and data == '' or len(data) > length


def user_validator(func):
    def wrapper(self, request):
        valid_data = self._loads_data(request)

        username = valid_data['username']
        password = valid_data['password']
        message = 'Invalid data!'

        if check_req_user_data(username):
            return self._response_error(message)

        if check_req_user_data(password):
            return self._response_error(message)

        return func(self, request)

    return wrapper


def id_validator(func):
    def wrapper(self, request, id):

        if id.is_integer():
            return func(self, request, int(id))

        return self._response_error('id must be int!')

    return wrapper
