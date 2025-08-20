from flask import Flask, Response, jsonify, request
from drawing.finger_drawer import FingerDrawer
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from frontend (React)

# Create an instance of the FingerDrawer class
drawer = FingerDrawer()

# 🎥 Video stream endpoint
@app.route('/video_feed')
def video_feed():
    return Response(drawer.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 🧼 Clear canvas endpoint
@app.route('/clear', methods=['POST'])
def clear_canvas():
    drawer.clear_canvas()
    return "Canvas cleared", 200

# 🧽 Toggle eraser mode endpoint
@app.route('/eraser', methods=['POST'])
def toggle_eraser():
    try:
        data = request.get_json()
        is_eraser = data.get("eraser", False)
        drawer.set_eraser_mode(is_eraser)
        return jsonify({"eraser": is_eraser}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 🏁 Start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
