from flask import Flask, request, jsonify, redirect
import sys
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
app.debug = True

# In-memory store for comments
comments = []

@app.route('/', methods=['GET', 'POST'])
def main():
    request.environ['wsgi.input_terminated'] = True

    headers = {header[0]: header[1] for header in request.headers}
    body = request.get_data(as_text=True)

    print("="*50, file=sys.stdout)
    print(f"Headers: {headers}", file=sys.stdout)
    print(f"Body: {body}", file=sys.stdout)
    print("="*50, file=sys.stdout)

    return jsonify(headers=headers, body=body)

@app.route('/redirect', methods=['GET'])
def redirect_to_desynk():
    return redirect("/desynk", code=302)

@app.route('/desynk', methods=['GET', 'POST'])
def desynk():
    request.environ['wsgi.input_terminated'] = True

    headers = {header[0]: header[1] for header in request.headers}
    body = request.get_data(as_text=True)

    print("="*50, file=sys.stdout)
    print(f"Headers: {headers}", file=sys.stdout)
    print(f"Body: {body}", file=sys.stdout)
    print("="*50, file=sys.stdout)

    return jsonify(headers=headers, body=body)

@app.route('/comments', methods=['GET', 'POST'])
def handle_comments():
    if request.method == 'POST':
        comment = request.get_data(as_text=True)
        print("====== *comment* =======", file=sys.stdout)
        print(comment, file=sys.stdout)
        print("====== *comment-end* =======", file=sys.stdout)
        comments.append(comment)
        return "Comment added", 200

    elif request.method == 'GET':
        return "\n".join(comments), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)

