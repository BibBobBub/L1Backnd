#!flask/bin/python
import json, datetime
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
        'id_usr': 2,
        'id_categ': 2, 
        'time': '2022-10-23 23:43:26.211232',
        'size': 11020
    },
    {
        'id': 2,
        'id_usr': 1,
        'id_categ': 2, 
        'time': '2022-10-23 23:43:26.271232',
        'size': 1721
    },
    {
        'id': 3,
        'id_usr': 1,
        'id_categ': 2, 
        'time': '2022-10-23 23:43:26.271232',
        'size': 15
    },
    {
        'id': 4,
        'id_usr': 1,
        'id_categ': 1, 
        'time': '2022-10-23 23:43:26.271232',
        'size': 180
    },
    {
        'id': 5,
        'id_usr': 2,
        'id_categ': 2, 
        'time': '2022-10-23 23:43:26.271232',
        'size': 1200
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
    return jsonify( { 'user': make_public_task(user[(task_id-1)])} )

@app.route('/todo/api/v1.0/user', methods = ['GET'])
#@auth.login_required
def create_user():
    users = {
        'id': user[-1]['id'] + 1,
        'name': request.args.get('name', None),
    }
    user.append(users)
    return jsonify( { 'users': user[len(user)-1] } ), 201

@app.route('/todo/api/v1.0/categ', methods = ['GET'])
#@auth.login_required
def create_categ():
    categs = {
        'id': categ[-1]['id'] + 1,
        'name': request.args.get('name', None),
    }
    categ.append(categs)
    return jsonify( { 'categ': categ[len(categ)-1]} ), 201


@app.route('/todo/api/v1.0/pay', methods = ['GET'])
#@auth.login_required  datetime.datetime.now()
def create_pay():
    sizeR  = request.args.get('size', None)
    userR  = request.args.get('user', None)
    categR  = request.args.get('categ', None)
    x=0
    while x != len(user):
        if userR == user[x]['name']:
            payUser = user[x]['id']
        x+=1
    x=0
    while x != len(categ):
        if categR == categ[x]['name']:
            payCateg=categ[x]['id']
        x+=1                
    timePay=datetime.datetime.now()
    pays = {
        'id': pay[-1]['id'] + 1,
        'id_usr': payUser,
        'id_categ': payCateg, 
        'time': timePay,
        'size': sizeR
    }
    pay.append(pays)
    return jsonify( { 'pay': pays} ), 201

@app.route('/todo/api/v1.0/showPayUsr', methods = ['GET'])
#@auth.login_required  datetime.datetime.now()
def show_pay_usr():
    #sizeR  = request.args.get('size', None)
    userR  = request.args.get('user', None)
    #categR  = request.args.get('categ', None)
    x=0
    while x != len(user):
        if userR == user[x]['name']:
            Foud_id = user[x]['id']
            uu=0
            n=0
            paysUsr={}
            while uu != len(pay):
                if Foud_id == pay[uu]['id_usr']:
                    paysUsr[n] = {
                    'id': pay[uu]['id'],
                    'id_usr':pay[uu]['id_usr'],
                    'id_categ':pay[uu]['id_categ'], 
                    'time': pay[uu]['time'],
                    'size': pay[uu]['size']
                    }
                    n+=1
                uu+=1
        x+=1
    return (paysUsr)

@app.route('/todo/api/v1.0/showPayUsrCat', methods = ['GET'])
#@auth.login_required  datetime.datetime.now()
def show_pay_usr_cat():
    #sizeR  = request.args.get('size', None)
    userR  = request.args.get('user', None)
    categR  = request.args.get('categ', None)
    x=0
    while x != len(user):
        if userR == user[x]['name']:
            Foud_id = user[x]['id']
            uu=0
            n=0
            paysUsr={}
            while uu != len(pay):
                if Foud_id == pay[uu]['id_usr']:
                    paysUsr[n] = {
                    'id': pay[uu]['id'],
                    'id_usr':pay[uu]['id_usr'],
                    'id_categ':pay[uu]['id_categ'], 
                    'time': pay[uu]['time'],
                    'size': pay[uu]['size']
                    }
                    n+=1
                uu+=1
        x+=1
    x=0
    while x != len(categ):
        if categR == categ[x]['name']:
            Foud_id_Cat = categ[x]['id']
            uu=0
            n=1
            paysUsrCat={}
            while uu != len(paysUsr):
                if Foud_id_Cat == paysUsr[uu]['id_categ']:
                    paysUsrCat[n] = {
                    'id': paysUsr[uu]['id'],
                    'id_usr':paysUsr[uu]['id_usr'],
                    'id_categ':paysUsr[uu]['id_categ'], 
                    'time': paysUsr[uu]['time'],
                    'size': paysUsr[uu]['size']
                    }
                    n+=1
                uu+=1
        x+=1
    return (paysUsrCat)
    
if __name__ == '__main__':
    app.run(debug = True)
