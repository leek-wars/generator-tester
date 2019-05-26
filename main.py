#!/usr/bin/env python
import subprocess
import os
import time
import hashlib
import json
import sys

GENERATOR_V1 = 'java -jar ../generator-v1/leekscript.jar'
GENERATOR_V2 = '../generator/build/leek-wars-generator'
options = {}

def main():
	scenario = None
	for a in range(1, len(sys.argv)):
		arg = sys.argv[a]
		if arg.startswith('--'):
			options[arg[2:]] = True
		else:
			scenario = arg

	if scenario:
		print("~~ Generator tester " + color.BLUE + color.BOLD + "single scenario" + color.END + " ~~ " + str(options))
		run_scenario(scenario)
	else:
		print("~~ Generator tester " + color.BLUE + color.BOLD + "main mode" + color.END + " ~~ " + str(options))
		run_all()

def run_all():
	scenarios = [
		"001_no_ai.json",
		"002_basic.json",
		"003_simple.json",
		"004_logs.json",
		"005_max_turns.json",
		"006_medium.json",
	]
	print(color.BOLD + str(len(scenarios)) + " scenarios to run..." + color.END)
	success = 0
	for scenario in scenarios:
		if run_scenario('scenario/' + scenario):
			success = success + 1
	print(color.BOLD + "Total: [" + str(success) + "/" + str(len(scenarios)) + "]" + color.END)

def run_scenario(scenario):
	result1, logs1, time1, hash1 = run(GENERATOR_V1, scenario)
	result2, logs2, time2, hash2 = run(GENERATOR_V2, scenario)
	if "logs" in options:
		print(logs1)
		print(logs2)
	if (hash1 != hash2):
		print(color.RED + color.BOLD + '[ERR] ' + color.END + "Scenario [" + color.BOLD + scenario + color.END + "]")
		print("V1: " + format_time(time1) + ", " + str(len(result1)) + " bytes, " + color.GREY + hash1 + color.END)
		print("V2: " + format_time(time2) + ", " + str(len(result2)) + " bytes, " + color.GREY + hash2 + color.END)
		analyze(result1, result2)
	else:
		print(color.GREEN + color.BOLD + "[OK] " + color.END + "Scenario [" + color.BOLD + scenario + color.END + "] " + str(len(result1)) + " bytes " + color.GREY + hash1 + color.END)
		print("V1: " + format_time(time1) + ", " + str(len(result1)) + " bytes, " + color.GREY + hash1 + color.END)
		print("V2: " + format_time(time2) + ", " + str(len(result2)) + " bytes, " + color.GREY + hash2 + color.END)
	return hash1 == hash2

def analyze(result1, result2):
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
		print(color.BOLD + item + " 1: " + color.END + str(part1[item]))
		print(color.BOLD + item + " 2: " + color.END + str(part2[item]))
		return False
	else:
		print(item + " is OK")
		return True

def run(generator, scenario):
	start = time.time()
	command = " ".join([
		generator,
		("--logs" if "logs" in options else ""),
		("--nocache" if "nocache" in options else ""),
		scenario
	])
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	result, err = proc.communicate()
	end = time.time()
	h = hashlib.new('sha1')
	logs = ""
	if result:
		lines = result.split("\n")
		result = lines[-2]
		logs = "\n".join(lines[0:-2])
	h.update(result)
	hash = h.hexdigest()
	return (result, logs, end - start, hash)

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