
import subprocess
import os
import time
import hashlib

GENERATOR_V1 = 'java -jar ../generator-v1/leekscript.jar '
GENERATOR_V2 = '../generator/build/leek-wars-generator -q '

start = time.time()
proc = subprocess.Popen(GENERATOR_V1 + 'scenario/fight_v1.json', shell=True, stdout=subprocess.PIPE)
result1, err = proc.communicate()
end = time.time()

start2 = time.time()
proc = subprocess.Popen(GENERATOR_V2 + 'scenario/fight_v1.json', shell=True, stdout=subprocess.PIPE)
result2, err = proc.communicate()
end2 = time.time()

print("Result 1 : " + result1)
print("Result 2 : " + result2)

h1 = hashlib.new('sha1')
h1.update(result1)
hash1 = h1.hexdigest()

h2 = hashlib.new('sha1')
h2.update(result2)
hash2 = h2.hexdigest()

print("Time v1", end - start, hash1)
print("Time v2", end2 - start2, hash2)