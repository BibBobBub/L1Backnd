from flask import Flask, render_template
app = Flask(__name__)
name_list = ["John", "Billy"]
John = {'car': 100, 'food': 1000}
Billy = {'car': 100, 'food': 1000}
@app.route('/')
def index():
  return render_template('template.html')

@app.route('/my-link/')
def my_link():
  print ('I got clicked!')
  print (name_list[0])
  print (Billy.keys())
  return render_template('template.html')

@app.route('/set-usr/')
def set_usr():
  print ('I got clicked!')

  return render_template('index.html')

@app.route('/set-categ/')
def set_categ():
  print ('I got clicked!')

  return render_template('index.html')

@app.route('/set-spending/')
def set_spending():
  print ('I got clicked!')

  return render_template('index.html')

@app.route('/show-categ/')
def show_categ():
  print ('I got clicked!')

  return render_template('index.html')

@app.route('/show-usr/<usr_key>', methods=['GET'])
def show_usr(usr_key):
  print ('usr_key.keys()')
  #return render_template('index.html')
  return (usr_key)
@app.route('/show-spending/')
def show_spending():
  print ('I got clicked!')
  
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)
