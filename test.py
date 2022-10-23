#!flask/bin/python
import json
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()
#AUTH
@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog


#CODE ERR    
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

user = [
    {
        'id': 1,
        'name': u'John',
    },
    {
        'id': 2,
        'name': u'Billy',
    }
]

categ = [
    {
        'id': 1,
        'name': u'Car',
    },
    {
        'id': 2,
        'name': u'Food',
    }
]

pay = [
    {
        'id': 1,
        'id_usr': u'Buy groceries',
        'id_categ': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'time': False,
        'size': 1000
    },
    {
        'id': 2,
        'id_usr': 1,
        'id_categ': 2, 
        'time': False,
        'size': 11000
    }
]

class MapEncoder(json.JSONEncoder): # dla json.dumps
    def default(self, obj):
        if isinstance(obj, map):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task
    
@app.route('/todo/api/v1.0/categ', methods = ['GET'])
#@auth.login_required 
def get_categ():
    #ress = map(make_public_task, categ) # dla json.dumps
    return jsonify( { 'category': categ } )
    #return jsonify( { 'categ': json.dumps(ress, cls=MapEncoder) } ) Krasivu varik

@app.route('/todo/api/v1.0/user/<int:task_id>', methods = ['GET'])
#@auth.login_required
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, user))
    
    #if len(list(task)) == 0:
    #    abort(404)
    return jsonify( { 'task': make_public_task(user[0])} )

@app.route('/todo/api/v1.0/user', methods = ['POST'])
#@auth.login_required
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400)
    task = {
        'id': user[-1]['id'] + 1,
        'name': request.json['name'],
        #'description': request.json.get('description', ""),
        #'done': False
    }
    user.append(task)
    return jsonify( { 'task': make_public_task(task) } ), 201

@app.route('/todo/api/v1.0/user/<int:task_id>', methods = ['PUT'])
#@auth.login_required
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, user))
#    if len(task) == 0:
 #       abort(404)
    if not request.json:
        abort(400)
    #if 'name' in request.json and type(request.json['name']) != unicode:
    #    abort(400)
   # if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    #if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['name'] = request.json.get('name', task[0]['name'])
    #task[0]['description'] = request.json.get('description', task[0]['description'])
    #task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/todo/api/v1.0/user/<int:task_id>', methods = ['DELETE'])
#@auth.login_required
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, user))
    if len(task) == 0:
        abort(404)
    user.remove(task[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)