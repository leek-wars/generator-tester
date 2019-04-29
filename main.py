
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
	
	if (hash1 == hash2):
		print("Result : " + result2)
	else:
		print("Result 1 : \n" + result1)
		print("Result 2 : \n" + result2)
		analyse(result1, result2)

	print("V1: " + format_time(time1) + " " + hash1)
	print("V2: " + format_time(time2) + " " + hash2)
	print('OK' if hash1 == hash2 else 'FAIL')

def analyse(result1, result2):
	parsed1 = json.loads(result1.split("\n")[-2])
	parsed2 = json.loads(result2.split("\n")[-2])
	compare('actions', parsed1['fight'], parsed2['fight'])
	compare('leeks', parsed1['fight'], parsed2['fight'])
	compare('map', parsed1['fight'], parsed2['fight'])
	actions1 = parsed1['fight']['actions']
	actions2 = parsed2['fight']['actions']
	print("Report 1 : " + str(len(actions1)) + " actions")
	print("Report 2 : " + str(len(actions2)) + " actions")
	print("Actions 1 : " + str(actions1))
	print("Actions 2 : " + str(actions2))

def compare(item, part1, part2):
	if (part1[item] != part2[item]):
		print(item + " is different")
	else:
		print(item + " is OK")

def run(command):
	start = time.time()
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	result, err = proc.communicate()
	end = time.time()
	h = hashlib.new('sha1')
	h.update(result.split("\n")[-2])
	hash = h.hexdigest()
	return (result, end - start, hash)

def format_time(time):
	return str(round(time * 10000) / 10) + 'ms'

if __name__ == '__main__':
    main()