from flask import Flask, request, render_template, jsonify, g

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def home():
    template = 'input.html'
    return render_template(template, display='none', displayalert='none')
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
