# Small server (use uswgi)

The script shows how you can run your own application.

### Installation:
Run this comand in terminal.
You can use virtualenv before this command if you like
```python
apt-get update
apt-get install python3-dev
pip install uwsgi
```

### Running:
glone this git repo to your PC
and run the script with this command

```python
uwsgi --socket 127.0.0.1:8080 --protocol=http -w small_server
```

After that put in your browser this:
```python
127.0.0.1:8080/contact/
127.0.0.1:8080/about/
127.0.0.1:8080
```
If you see different pages - It works.
