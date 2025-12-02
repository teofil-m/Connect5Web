# Backend Dependency Installation Guide

## Issue: ModuleNotFoundError: No module named 'flask_socketio'

This error occurs when Python dependencies are not properly installed.

### Quick Fix

Run one of these commands in PowerShell from the `backend` folder:

```powershell
# Option 1: Install all requirements at once
pip install -r requirements.txt

# Option 2: Install Flask-SocketIO specifically
pip install Flask-SocketIO==5.3.4

# Option 3: Manual batch installation
pip install Flask==2.3.3 Flask-CORS==4.0.0 Flask-SocketIO==5.3.4 python-socketio==5.9.0 python-engineio==4.7.1
```

### Complete Setup

If you're getting import errors, follow these steps:

1. **Navigate to backend folder**:
   ```powershell
   cd d:\AI-training\Blocks\backend
   ```

2. **Upgrade pip** (optional but recommended):
   ```powershell
   python -m pip install --upgrade pip
   ```

3. **Install all dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```powershell
   python -c "from flask_socketio import SocketIO; print('Success!')"
   ```

5. **Run the server**:
   ```powershell
   python game_server.py
   ```

### Using the Helper Script

Double-click or run:
```bash
backend\install_dependencies.bat
```

This will automatically install all dependencies and verify them.

### Requirements

The `requirements.txt` file contains:
- Flask==2.3.3
- Flask-CORS==4.0.0
- **Flask-SocketIO==5.3.4** ← This was missing and is now added
- python-socketio==5.9.0
- python-engineio==4.7.1

### Troubleshooting

**Still getting import errors?**

1. Check Python version: `python --version` (should be 3.8+)
2. Check pip version: `pip --version`
3. Try upgrading: `python -m pip install --upgrade pip setuptools wheel`
4. Try installing with `--no-cache-dir`:
   ```powershell
   pip install --no-cache-dir -r requirements.txt
   ```

**Permission denied?**

Try running PowerShell as Administrator.

**ModuleNotFoundError persists?**

Try uninstalling and reinstalling:
```powershell
pip uninstall Flask-SocketIO -y
pip uninstall python-socketio -y
pip install -r requirements.txt
```

### What Each Package Does

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| Flask-CORS | Cross-origin requests support |
| Flask-SocketIO | WebSocket support for real-time updates |
| python-socketio | SocketIO protocol implementation |
| python-engineio | Engine.IO protocol (used by SocketIO) |

### Verification

After installation, you should see this output:

```powershell
PS> python game_server.py
 * Serving Flask app 'game_server'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

If you see this, the backend is ready!

### Next Steps

Once backend is running:
1. Open a new PowerShell window
2. Navigate to `frontend` folder
3. Run `npm start`
4. Open browser to `http://localhost:4200`

### Need Help?

See: [QUICKSTART.md](../QUICKSTART.md) - Troubleshooting section
