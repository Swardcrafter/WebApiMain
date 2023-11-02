from flask import Flask, request
import os
import random
import websockets
import asyncio
import json

ws = None

websocket_server_url = os.environ['WEBSOCKET_URL']

app = Flask(__name__)
username_good = os.environ['USERNAME']
password_good = os.environ['PASSWORD']


async def send_hello_message_to_ws(websocket_url, message):
	async with websockets.connect(websocket_url) as ws:
		await ws.send(message)
		print(f"Sent {message}")

@app.route('/runmainstuff')
def mainapi():
	global username_good
	global password_good
	username = request.args.get('username')
	password = request.args.get('password')
	api_call = request.args.get('api_call')
	if username == username_good and password == password_good:
		print("Logged")
		if api_call == "say_hello":
			asyncio.run(send_hello_message_to_ws(websocket_server_url, "say_hello"))  # Send message to WebSocket
			print("Hello")
		if api_call == "toggle_light":
			asyncio.run(send_hello_message_to_ws(websocket_server_url, "toggle_light"))  # Send message to WebSocket
			print("Hello")
		if api_call == "change_track":
			change = request.args.get('change')
			asyncio.run(send_hello_message_to_ws(websocket_server_url, f"change_track&{change}"))
		if api_call == "copy_desmos":
			website = request.args.get('website')
			asyncio.run(send_hello_message_to_ws(websocket_server_url, f"copy_desmos&{website}"))
		if api_call == "run_command":
			command = request.args.get('command')
			asyncio.run(send_hello_message_to_ws(websocket_server_url, f"run_command&{command}"))
		if api_call == "say_message":
			message = request.args.get('message')
			flash_light = request.args.get('flash_light')
			asyncio.run(send_hello_message_to_ws(websocket_server_url, f"say_message&{message}&{flash_light}"))  # Send message to WebSocket
			print("Test")
		if api_call == "flash_light":
			times = request.args.get('times')
			asyncio.run(send_hello_message_to_ws(websocket_server_url, f"flash_light&{times}"))  # Send message to WebSocket
			print("Test")
		return "Logged."
	else:
		return "Wrong."


@app.route('/')
def main():
  return "api"

async def start_websocket_client(websocket_url):
	async with websockets.connect(websocket_url) as ws:
		result = await ws.recv()
		print(result)


async def run():
	# Start both the Flask app and the websocket client concurrently
	await asyncio.gather(
		start_websocket_client(websocket_server_url),
		asyncio.to_thread(app.run, host='0.0.0.0', port=random.randint(2000, 9000))
	)


if __name__ == '__main__':
	asyncio.run(run())