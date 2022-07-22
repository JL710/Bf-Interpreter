import argparse
import re


def format(code: str) -> str:
    re_expr = re.compile(r"(#(.*))|/\*((.*)\n)*(\*/)|(//(.*))")
    code = re_expr.sub(" ", code)
    code = code.replace(" ", "")
    code = code.replace("\n", "")
    return code

    

class Interpreter:
    def __init__(self, code: str, debug: bool, memory_output: bool):
        self.__debug = debug
        self.__memory_output = memory_output

        self.__code = format(code)
        self.__memory = [0]
        self.__cursor = 0
        self.__point_zero = 0

        self.__instruction = 0
        self.__loops = [] # (int: memory_location, int: first instuction)

        while self.__instruction < len(self.__code):
            self.__do_instruction(self.__code[self.__instruction])
            if self.__memory_output:
                print(self.__memory)
            

    def __do_instruction(self, instruction: str):
        if instruction == ">":
            self.__cursor += 1
            if len(self.__memory) <= self.__cursor:
                self.__memory.append(0)
            self.__instruction += 1
        
        elif instruction == "<":
            self.__cursor -= 1
            if self.__cursor < 0:
                self.__cursor += 1
                self.__point_zero += 1
                self.__memory = [0] + self.__memory
            self.__instruction += 1

        elif instruction == "+":
            if self.__memory[self.__cursor] < 255:
                self.__memory[self.__cursor] += 1
            self.__instruction += 1

        elif instruction == "-":
            if self.__memory[self.__cursor] > 0:
                self.__memory[self.__cursor] -= 1
            self.__instruction += 1

        elif instruction == ".":
            print(chr(self.__memory[self.__cursor]), end="")
            self.__instruction += 1

        elif instruction == ",":
            self.__memory[self.__cursor] = ord(input("1 Ascii char: "))
            self.__instruction += 1

        elif instruction == "[":
            memory_location = self.__cursor - self.__point_zero
            first_location = self.__instruction + 1 # istruction after [
            self.__loops.append((memory_location, first_location))
            self.__instruction += 1

        elif instruction == "]":
            pass # TODO: everything here
            if self.__memory[self.__loops[-1][0] + self.__point_zero] == 0:
                self.__loops.pop()
                self.__instruction += 1
            else:
                self.__instruction = self.__loops[-1][1]

        elif instruction == "|":
            if self.__debug:
                print("-"*15)
                for index, location in enumerate(self.__memory):
                    if index == self.__cursor:
                        print(f"{index}:{location} <--")
                    else:
                        print(f"{index}:{location}")
                print("-"*15)
            self.__instruction += 1

        else:
            raise SyntaxError(f"The instruction {instruction} does not exist!")



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    file_or_code = parser.add_mutually_exclusive_group()
    file_or_code.add_argument(
        "--file", "-f", 
        help="The file with the brainfuck code.")

    file_or_code.add_argument(
        "--code", "-c",
        action="store_true",
        help="Code to execute."
    )

    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enables memoryoutput for |")

    parser.add_argument(
        "--memory-output", "-m",
        action="store_true",
        help="If set, memory will be printed after every instruction."
    )

    args = parser.parse_args()


    if args.file:
        with open(args.file, "r") as f:
            code = f.read()
        
        Interpreter(code, args.debug, args.memory_output)

    elif args.code:
        Interpreter(input("Code: "), args.debug, args.memory_output)
