import datetime
from django.conf import settings

def get_next_task_id():
    return settings.REDIS_CLIENT.incr('tarefa:next_id')

def create_task(titulo, descricao, status):
    task_id = get_next_task_id()
    key = f'tarefa:{task_id}'
    settings.REDIS_CLIENT.hset(key, mapping={
        'titulo': titulo,
        'descricao': descricao,
        'data_criacao': str(datetime.now()),
        'status': status
    })
    return task_id

def get_task(task_id):
    key = f'tarefa:{task_id}'
    return settings.REDIS_CLIENT.hgetall(key) or None

def get_all_tasks():
    keys = settings.REDIS_CLIENT.keys('tarefa:*')
    tasks = []
    for key in keys:
        if key != 'tarefa:next_id':  
            task = settings.REDIS_CLIENT.hgetall(key)
            task['id'] = key.split(':')[1]
            tasks.append(task)
    return tasks

def update_task(task_id, field, value):
    key = f'tarefa:{task_id}'
    if settings.REDIS_CLIENT.exists(key):
        settings.REDIS_CLIENT.hset(key, field, value)
        return True
    return False

def delete_task(task_id):
    key = f'tarefa:{task_id}'
    return settings.REDIS_CLIENT.delete(key) > 0