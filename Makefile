run-debug:
	flask --debug run
run-demo:
	gunicorn3 -e SCRIPT_NAME=/hackaday/paste --bind 0.0.0.0:8004 app:app
