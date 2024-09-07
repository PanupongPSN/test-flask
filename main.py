from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    print("Home route called")  # Debug log
    return "Hello from Flask!"


if __name__ == '__main__':
    app.run()
#update