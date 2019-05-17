#!/usr/bin/env python
import subprocess
import os
import time
import hashlib
import json

GENERATOR_V1 = 'java -jar ../generator-v1/leekscript.jar '
GENERATOR_V2 = '../generator/build/leek-wars-generator '

def main():
	run_scenario("001_no_ai.json")
	run_scenario("002_basic.json")
	# run_scenario("fight_v1.json")

def run_scenario(scenario):
	print(color.BOLD + "Run scenario [" + scenario + "]" + color.END)
	result1, time1, hash1 = run(GENERATOR_V1 + 'scenario/' + scenario)
	result2, time2, hash2 = run(GENERATOR_V2 + 'scenario/' + scenario)
	
	if (hash1 != hash2):
		# print("Result 1 : \n" + result1)
		# print("Result 2 : \n" + result2)
		analyse(result1, result2)

	print("V1: " + format_time(time1) + " " + color.GREY + hash1 + color.END)
	print("V2: " + format_time(time2) + " " + color.GREY + hash2 + color.END)
	print(color.GREEN + color.BOLD + '[OK]' + color.END if hash1 == hash2 else color.RED + color.BOLD + '[FAIL!]' + color.END)

def analyse(result1, result2):
	parsed1 = dict()
	parsed2 = dict()
	try:
		parsed1 = json.loads(result1)
	except:
		print("Failed to parse result from generator v1")
		return
	try:
		parsed2 = json.loads(result2)
	except:
		print("Failed to parse result from generator v2 :")
		print(result2)
		return
	compare('leeks', parsed1['fight'], parsed2['fight'])
	compare('map', parsed1['fight'], parsed2['fight'])
	compare('logs', parsed1, parsed2)
	compare('actions', parsed1['fight'], parsed2['fight'])

def compare(item, part1, part2):
	if (part1[item] != part2[item]):
		print(item + " is different")
		print(item + " 1: " + str(part1[item]))
		print(item + " 2: " + str(part2[item]))
		return False
	else:
		print(item + " is OK")
		return True

def run(command):
	start = time.time()
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	result, err = proc.communicate()
	end = time.time()
	h = hashlib.new('sha1')
	# print("raw result " + result)
	if result:
		result = result.split("\n")[-2]
	h.update(result)
	hash = h.hexdigest()
	return (result, end - start, hash)

def format_time(time):
	return str(round(time * 10000) / 10) + 'ms'

class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	GREY = '\033[37m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

if __name__ == '__main__':
    main()