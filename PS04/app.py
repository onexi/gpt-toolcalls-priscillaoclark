from flask import Flask, render_template, request
from main import main

app = Flask(__name__)  # Refers to self (the current file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_message = request.form['user_message']
        try:
            result = main(user_message)
        except Exception as e:
            app.logger.error(f"Error processing request: {str(e)}")
            return "An error occurred. Please try again later.", 500
        return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)