import subprocess
import os
import json
import time


def pagination(cmd, have_params, output):
    f = open(output, "w")
    f.close()
    page_no = 1
    gate = 1
    exceeded = 0
    if (have_params):
        while (gate):
            cmd_edited = cmd + "&per_page=100&page=" + \
                str(page_no)+"\"" + " > " + "meta_data/inter.json"
            time.sleep(0.5)
            print(cmd_edited)
            subprocess.run(cmd_edited, shell=True)
            fob = open("meta_data/inter.json", "r")
            text = fob.read(4)
            fob.close()
            if (text == "[\n\n]" or page_no == 11 or not text):
                gate = 0
                if page_no == 11:
                    exceeded = 1
            else:
                cat_json(output, [output, "meta_data/inter.json"])
            page_no += 1
    else:
        while (gate):
            print(page_no)
            cmd_edited = cmd + "?per_page=100&page=" + \
                str(page_no)+"\"" + " > " + "meta_data/inter.json"
            print(cmd_edited)
            subprocess.run(cmd_edited, shell=True)
            fob = open("meta_data/inter.json", "r")
            text = fob.read(4)
            fob.close()
            if text == "[\n\n]" or page_no == 11 or not text:
                gate = 0
                if page_no == 11:
                    exceeded = 1

            else:
                cat_json(output, [output, "meta_data/inter.json"])

            page_no += 1
    return exceeded


def cat_json(output_filename, file_list):
    head = []

    for f in file_list:
        infile = open(f)
        temp = infile.read()
        file_data = []
        # print(len(temp))
        if len(temp) != 0:

            infile = open(f)
            file_data = json.load(infile)
        head += file_data

    outfile = open(output_filename, "w")

    json.dump(head, outfile)
    outfile.close()
    infile.close()

def cat_json_dict(output_filename, file_list):
    head = []

    for f in file_list:
        infile = open(f)
        temp = infile.read(4)
        file_data = []
        # print(len(temp))
        if f=="meta_data/iter4.json":
            if temp != "[\n\n]" and temp:
                infile = open(f)
                dat = json.load(infile)
                file_data.append(dat) #as iter4 is a dictionary
        elif len(temp) != 0:
            print(f)
            infile = open(f)
            file_data = json.load(infile)

        head += file_data

    outfile = open(output_filename, "w")
    json.dump(head, outfile)
    outfile.close()


def raw(text):
    """Returns a raw string representation of text"""

    escape_dict = {
    ',': '^',
    '\n': r'\n',
    '\r': r'\r',
    '\t': r'\t',
    '\'': r'\'',
    '\"': r'\"', }
    
    new_string = ''
    for char in text:
        try:
            new_string += escape_dict[char]
        except KeyError:
            new_string += char
    return new_string


def run_command(args, params, authentication):
    command = "curl -H \"Authorization: token " + \
        str(authentication)+"\" \"https://api.github.com"
    for i in args:
        command += "/"
        command += i
    if params:
        command += "?"
        for i in params:
            command += i
    return command

def run_command_accept(args, params, authentication):
    command = "curl -H \"Accept: application/vnd.github.groot-preview+json\" -H \"Authorization: token " + \
        str(authentication)+"\" \"https://api.github.com"
    for i in args:
        command += "/"
        command += i
    if params:
        command += "?"
        for i in params:
            command += i
    return command