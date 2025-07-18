USER_FIELD_TEXTS = {
    'first_name': {
        'label': 'Имя',
        'placeholder': 'Имя',
        'help_text': ''
    },
    'last_name': {
        'label': 'Фамилия',
        'placeholder': 'Фамилия',
        'help_text': ''
    },
    'username': {
        'label': 'Имя пользователя',
        'placeholder': 'Имя пользователя',
        'help_text': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
    },
    'password1': {
        'label': 'Пароль',
        'placeholder': 'Пароль',
        'help_text': 'Ваш пароль должен содержать как минимум 3 символа.'
    },
    'password2': {
        'label': 'Подтверждение пароля',
        'placeholder': 'Подтверждение пароля',
        'help_text': 'Для подтверждения введите, пожалуйста, пароль ещё раз.'
    }
}

TASK_FIELD_TEXTS = {
    'name': {
        'label': 'Имя',
        'placeholder': 'Имя'
    },
    'description': {
        'label': 'Описание',
        'placeholder': 'Описание'
    },
    'status': {
        'label': 'Статус',
        'placeholder': ''
    },
    'executor': {
        'label': 'Исполнитель',
        'placeholder': ''
    },
    'labels': {
        'label': 'Метки',
        'placeholder': ''
    }
}

SUCCESS_MESSAGES = {
    'user': {
        'user_created': 'Пользователь успешно зарегистрирован',
        'user_updated': 'Пользователь успешно изменён',
        'user_deleted': 'Пользователь успешно удалён',
    },
    'status': {
        'status_created': 'Статус успешно создан',
        'status_updated': 'Статус успешно изменён',
        'status_deleted': 'Статус успешно удален',
    },
    'task':{
        'task_created': 'Задача успешно создана',
        'task_updated': 'Задача успешно изменена',
        'task_deleted': 'Задача успешно удалена',
    },
    'label': {
        'label_created': 'Метка успешно создана',
        'label_updated': 'Метка успешно изменена',
        'label_deleted': 'Метка успешно удалена',
    },
    'logged_in': 'Вы залогинены',
    'logged_out': 'Вы разлогинены',
}

ERROR_MESSAGES = {
    'not_authenticated': 'Вы не авторизованы! Пожалуйста, выполните вход.',
    'no_permission': 'У вас нет прав для этого действия.',
    'no_permission_update': 'У вас нет прав для изменения другого пользователя.',
    # 'no_permission_delete': 'У вас нет прав для удаления другого пользователя.', - не используется в демонстрационном проекте
    'user_has_tasks': 'Невозможно удалить пользователя, потому что он используется',
    'status_using': 'Невозможно удалить статус, потому что он используется',
    'only_author_can_delete': 'Задачу может удалить только ее автор',
    'label_using': 'Невозможно удалить метку, потому что она используется',
    'login_invalid': (
        "Пожалуйста, введите правильные имя пользователя и пароль. "
        "Оба поля могут быть чувствительны к регистру."
    ),
}