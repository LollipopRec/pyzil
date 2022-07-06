import sys
import json
from importlib import import_module
import argparse

#python3 LollipopServer.py -a '1111' -d 'helloworld.Hello' -m train -i hello.json -p params.json -o output.json

contractMap = {}
def check(contractCode):
    code = compile(contractCode, 'contract', 'exec')
    if code is not None:
        return hash(code)
    return None

def run(addr, code, method, input, param, output):
    if contractMap.get(addr, None) == None:
        module, class_name = code.rsplit('.', 1)
        module = import_module(module)
        my_class = getattr(module, class_name)
        my_instance = my_class()
        with open(input, 'r') as f:
            data = json.load(f)
        for item in data:
            setattr(my_instance, item, data[item])
        contractMap[addr] = my_instance
    with open(param, 'r') as f:
            param = json.load(f)
    
    result = getattr(contractMap[addr], method)(*param['params'])

    with open(input, 'r') as f:
        data = json.load(f)
    for item in data:
        data[item] = getattr(my_instance, item)

    with open(output, 'w') as f:
        json.dump(data, f)
    
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lollipop')
    parser.add_argument("-a", "--contractAddress", help="display a square of a given number")
    parser.add_argument("-d", "--contractCode")
    parser.add_argument("-m", "--method")
    parser.add_argument("-i", "--input", help="json file path for initializing the class")
    parser.add_argument("-p", "--params", help="json file path for parameters of the method")
    parser.add_argument("-o", "--output", help="json file path for persisting the members of the class")
    args = parser.parse_args()
    addr = check(args.contractCode)
    run(addr, args.contractCode, args.method, args.input, args.params, args.output)
