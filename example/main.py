import ExampleInterface
import sys
import json

sys.path.append("/opt/workspace/build/test/system_test/RTPS/TEST/")


inp = dict(a=16)

print(json.dumps(inp))

st = ""
val = ExampleInterface.metodo_uno(json.dumps(inp))


print(ExampleInterface.metodo_dos(json.dumps(dict(a=1.8, b="hola"))))
print(ExampleInterface.metodo_tres(json.dumps(dict(input=dict(a=1, b=2)))))
print(ExampleInterface.metodo_cuatro(json.dumps(dict(input=dict(a=1, b=2)))))
print(ExampleInterface.metodo_cinco(json.dumps(inp)))
