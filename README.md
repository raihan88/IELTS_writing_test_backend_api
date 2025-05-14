**1. Create a virtual environment:**
```
python -m venv .venv
.venv\Scripts\activate
```
**2. Install requirements:**
```
pip install -r requirements.txt
```
*Make sure you are in the same directory that contains  `requirements.txt` file*

**3. Run:**
```
cd app
uvicorn app.main:main --reload
```
**4. Check API documentaion:**

visit: `http://127.0.0.1:8000/docs`
