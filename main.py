
import subprocess
import os
import time
import hashlib
import json

GENERATOR_V1 = 'java -jar ../generator-v1/leekscript.jar '
GENERATOR_V2 = '../generator/build/leek-wars-generator -q '

def main():
	result1, time1, hash1 = run(GENERATOR_V1 + 'scenario/fight_v1.json')
	result2, time2, hash2 = run(GENERATOR_V2 + 'scenario/fight_v1.json')
	parsed1 = json.loads(result1)
	parsed2 = json.loads(result2)

	if (hash1 == hash2):
		print("Result : " + result1)
	else:
		print("Result 1 : " + result1)
		print("Result 2 : " + result2)

	print("V1: " + format_time(time1) + " " + hash1)
	print("V2: " + format_time(time2) + " " + hash2)
	print('OK' if hash1 == hash2 else 'FAIL')

def run(command):
	start = time.time()
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	result, err = proc.communicate()
	end = time.time()
	h = hashlib.new('sha1')
	h.update(result)
	hash = h.hexdigest()
	return (result, end - start, hash)

def format_time(time):
	return str(round(time * 10000) / 10) + 'ms'

if __name__ == '__main__':
    main()