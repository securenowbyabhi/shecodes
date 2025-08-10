STEPS FOR FOLDER STRUCTURE :

aditiverma@Mac Documents % mkdir checkIncheckout 
aditiverma@Mac Documents % cd checkIncheckout 
aditiverma@Mac checkIncheckout % mkdir backend
aditiverma@Mac checkIncheckout % cd backend 
aditiverma@Mac backend % mkdir app app/models app/routes app/controllers
aditiverma@Mac backend % touch app.py
aditiverma@Mac backend % touch .env
aditiverma@Mac backend % touch requirements.txt
aditiverma@Mac backend % cd app
aditiverma@Mac app % touch __init__.py db.py
aditiverma@Mac app % touch models/user.py
aditiverma@Mac app % touch routes/auth_routes.py
aditiverma@Mac app % touch controllers/auth_controller.py

----------------------------------------------------------------------

STEPS FOR PYTHON FLASK:


cd backend 

python3 -m venv venv

source venv/bin/activate     # Mac/Linux

 OR on Windows:

 venv\Scripts\activate

pip freeze > requirements.txt

or 

pip install Flask flask-pymongo pymongo python-dotenv flask-cors

pip install --upgrade pip

pip install --upgrade certifi


python3 -m venv venv

python3 app.py



----------------------------------------------------------------------

STEPS FOR REACT 

cd frontend

node -v

npm -v

npm install

npm install react-router-dom

npm install react-toastify

npm install react-bootstrap bootstrap react-router-bootstrap

npm start

 <!-- above command should install all required files in and it will come under package.json -->
<!-- package.json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "axios": "^1.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
} -->



----------------------------------------------------------------------
# This is setup for getting MONGO URL and SECRET KET 
Inside .env file 
add your
MONGO_URI=mongodb+srv://your_user:your_pass@cluster0.mongodb.net/testdb?retryWrites=true&w=majorityt

your_user -> username for ATLAS
your_pass -> password for ATLAS
testdb -> database name 
(if your password has special character it needs to be encoded like if password is p@ssw/rd#1 then put p%40ssw%2Frd%231 )


SECRET_KEY=your_secret_key
(GENERATE THIS WAY : python3 -c "import secrets; print(secrets.token_hex(16).)"
--> a2c4e5f7b9d1a3e6f8b7c1d2e4f5a6b7. --> similar code can get generated
)


----------------------------------------------------------------------
// CORS SETUP 
if REACT has to connect with PYTHON FLASK especially in mac local port 500 does not work 
hence the changes in app.py
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(port=8000, debug=True)

Reason -
macos uses port 5000 internally, so you're trying to connect to a o/s service, not your flask app -- change the port your app runs on with a port=xxxx modifier, e.g. app.run(debug=True, port=8000)
