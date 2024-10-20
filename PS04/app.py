from flask import Flask, render_template
from main import main
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_message = request.form['user_message']
    #user_message = "When is the next train from South Station to Kendall Square?"
    try:
        result = main(user_message)
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return "An error occurred. Please try again later.", 500
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)