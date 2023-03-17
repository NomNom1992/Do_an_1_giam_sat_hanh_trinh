from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
import sqlite3
app = Flask(__name__)

# @app.route('/Users/Admin/OneDrive/Máy%20tính/Đồ%20án%201/')

# def home():
	# return render_template('/Users/Admin/OneDrive/Máy%20tính/Đồ%20án%201/index.html')

# @app.route('/Users/Admin/OneDrive/Máy%20tính/Đồ%20án%201/api')
# def api():
#     printf(123)
	# return render_template('/Users/Admin/OneDrive/Máy%20tính/Đồ%20án%201/api.html')

# if __name__ == '__main__':
#     app.run(debug=True)



@app.route('/')
def index():
	return render_template('index.html')



@app.route('/login', methods=['POST'])
def login():
	data = request.json
	print(data)
	conn = sqlite3.connect('account.db')
	c = conn.cursor()
	c.execute("SELECT * FROM accounts")
	accounts = c.fetchall()
	conn.close()
	for account in accounts:
		if data['username'] == account[1] and data['password'] == str(account[2]):
			return jsonify({'success': True, 'message': 'Login successful'})
	return jsonify({'success': False, 'message': 'Login failed'})



@app.route('/home')
def home():
	return render_template('home.html')



@app.route('/getlistcar')
def listcar():
	conn = sqlite3.connect('account.db')
	c = conn.cursor()
	c.execute("SELECT * FROM drivers")
	drivers = c.fetchall()
	conn.close()
	json_data = []
	for row in drivers:
		json_data.append({
			'driver_id': row[0],
			'name': row[1],
			'phone': row[3],
			'lp': row[4],
			'gplx': row[5]
		})
	return jsonify(json_data)



@app.route('/detail/<lp>')
def detail(lp):
	conn = sqlite3.connect('account.db')
	c = conn.cursor()
	c.execute("SELECT driver_id,name,phone_number,drivers.lp,avt,type,rfid,giayphep,lat,lng FROM drivers,cars WHERE drivers.lp = cars.lp AND drivers.lp = ?",(lp,))
	detail = c.fetchall()
	print(detail[0])
	conn.close()
	detail_json = []
	for row in detail:
		detail_json.append({
			'id': row[0],
			'name': row[1],
			'phone': row[2],
			'lp': row[3],
			'avt': row[4],
			'type': row[5],
			'rfid': row[6],
			'giayphep': row[7],
			'lat': row[8],
			'lng': row[9]
		})

	# return render_template('37a15534.html')
	return render_template('detail.html', css_url=url_for('static', filename='css/all.min.css'), data = detail_json)

# @app.route('/car/<lp>')
# def car(lp):
# 	conn = sqlite3.connect('account.db')
# 	c = conn.cursor()
# 	c.execute("SELECT driver_id,name,phone_number,drivers.lp,avt,type,rfid,giayphep,lat,lng FROM drivers,cars WHERE drivers.lp = cars.lp AND drivers.lp = ?",(lp,))
# 	detail = c.fetchall()
# 	detail_json = []
# 	detail_json.append({
# 		'driver_id': detail[0],
# 		'name': detail[1],
# 		'phone': detail[2],
# 		'lp': detail[3],
# 		'avt': detail[4],
# 		'type': detail[5],
# 		'rfid': detail[6],
# 		'giayphep': detail[7],
# 		'lat': detail[8],
# 		'lng': detail[9]
# 	})
# 	return jsonify(detail_json)
@app.route('/add-new-driver')
def add():
	return render_template('adddriver.html')



@app.route('/add/send', methods=['POST'])
def new_info():
	data = request.json
	conn = sqlite3.connect('account.db')
	c = conn.cursor()
	c.execute('INSERT INTO drivers(driver_id, name, age, phone_number, lp, gplx) VALUES (?, ?, ?, ?, ?, ?)',(data['id'], data['name'], data['age'], data['phone'], data['license'], data['gplx']))
	c.execute('INSERT INTO accounts(username, password) VALUES (?, ?)',(data['username'], data['password']))
	c.execute('INSERT INTO cars(lp, type) VALUES (?, ?)',(data['license'], data['type']))
	
	conn.commit()
	conn.close()
	return jsonify({'success': True, 'message': 'add infomation successful'})

@app.route('/avtchudo')
def serve_image():
    return send_from_directory('imgs', 'avtchudo.jpg')



@app.route('/caricon')
def serve_icon():
    return send_from_directory('imgs', 'car_icon.png')



if __name__ == '__main__':
	app.run(debug=True)