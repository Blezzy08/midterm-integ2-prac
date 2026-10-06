# midterm-integ2-prac

## Backend

The backend prototype is a Flask API located in `backend/`.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app run --debug
```

The API health check is available at `http://127.0.0.1:5000/api/health`.
Run the backend tests from `backend/` with:

```powershell
python -m unittest discover -s tests
```
