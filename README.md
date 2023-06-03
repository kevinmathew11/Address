# Address
Store address entry along with latitude and longitude. Also the user can retrive all address within a distance radius from a given location

# Instruction

#### 1.Clone the repository

#### 2.Activate virtual machine

```
python -m venv address_env
.\address_env\Scripts\activate
```

#### 3.Install the required packages mentioned in requirements.txt file
```
pip install -r requirements.txt
```

#### 4.Start the fastapi server on port 8000
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 5.Open any browser and go to url http://0.0.0.0:8000/docs



