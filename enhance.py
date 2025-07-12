from flask import Flask, request, jsonify
import os
import shutil

app = Flask(__name__)

@app.route('/enhance', methods=['POST'])
def enhance():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = file.filename
    save_path = os.path.join('uploads', filename)
    enhanced_path = save_path.replace('.', '_enhanced.')

    os.makedirs('uploads', exist_ok=True)
    file.save(save_path)

    # Dummy enhancement logic: copy file
    shutil.copy(save_path, enhanced_path)

    return jsonify({
        'message': 'Enhanced successfully',
        'path': enhanced_path
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
