import redis
import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)  
def get_next_id():
    return r.incr('tarefa_id')

@csrf_exempt
def criar_tarefa(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_tarefa = get_next_id()
        tarefa = {
            'id': id_tarefa,
            'titulo': data.get('titulo'),
            'descricao': data.get('descricao'),
            'status': data.get('status', 'Pendente')
        }
        r.set(f"tarefa:{id_tarefa}", json.dumps(tarefa))
        return JsonResponse({'status': 'criado', 'tarefa': tarefa})

@csrf_exempt
def ler_tarefa(request, id_tarefa):
    if request.method == 'GET':
        chave = f"tarefa:{id_tarefa}"
        tarefa_json = r.get(chave)
        if tarefa_json:
            tarefa = json.loads(tarefa_json)
            tarefa['id'] = id_tarefa  # Adiciona o ID na resposta
            return JsonResponse(tarefa)
        else:
            return JsonResponse({'erro': 'Tarefa não encontrada'}, status=404)

@csrf_exempt
def atualizar_tarefa(request, id_tarefa):
    if request.method == 'PUT':
        data = json.loads(request.body)
        chave = f"tarefa:{id_tarefa}"
        if not r.exists(chave):
            return JsonResponse({'erro': 'Tarefa não encontrada'}, status=404)
        tarefa_json = r.get(chave)
        tarefa = json.loads(tarefa_json)
        tarefa.update(data)
        r.set(chave, json.dumps(tarefa))
        return JsonResponse({'status': 'atualizado', 'tarefa': tarefa})

@csrf_exempt
def deletar_tarefa(request, id_tarefa):
    if request.method == 'DELETE':
        chave = f"tarefa:{id_tarefa}"
        if r.exists(chave):
            r.delete(chave)
            return JsonResponse({'status': 'deletado', 'id': id_tarefa})
        else:
            return JsonResponse({'erro': 'Tarefa não encontrada'}, status=404)

@csrf_exempt
def listar_tarefas(request):
    if request.method == 'GET':
        # SCAN para pegar todas as chaves "tarefa:*"
        tarefas = []
        for chave in r.scan_iter("tarefa:*"):
            tarefa_json = r.get(chave)
            if tarefa_json:
                tarefa = json.loads(tarefa_json)
                #pega o ID da chave (ex.: "tarefa:1" -> 1)
                tarefa['id'] = int(chave.split(':')[1])
                tarefas.append(tarefa)
        return JsonResponse({'tarefas': tarefas})