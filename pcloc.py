#!/usr/bin/python3.7

# python script to wrap cloc
# to get pretty outputs
# @author : mubeenghauri <ghauri.mubeen@gmail.com>

import subprocess
import sys
from io import BytesIO
from rich.console import Console
from rich.table import Table

# creating console object
console = Console()

cmd = ['cloc']
for arg in sys.argv[1:]: 
	cmd.append(arg)

#print("cmd : ", cmd)

with console.status("Calculating Lines of Code...", spinner="point"):
	proc = subprocess.run(cmd, capture_output=True)
	stroutput = proc.stdout.decode().split('\n')
	
	
text_file_count = str(stroutput[0])
unique_files = str(stroutput[1])
files_ignored = str(stroutput[2])

console.print(text_file_count.split('\r')[-1:][0].strip(' '), style="bold green", justify="center") # text files count
console.print(unique_files.split('\r')[-1:][0].strip(' '), style="bold yellow", justify="center") # unique files
console.print(files_ignored.split('  ')[-1:][0].strip(' '), style="bold red", justify="center") # files ignored
print('\n') # blank-line
console.print(stroutput[4], justify="center") # credit + stats

console.rule("[bold green] Stats w.r.t Language")

table = Table(title="Lines of Code", show_lines=True)

table.add_column("Language", justify="right", style="cyan", no_wrap=True)
table.add_column("files", style="magenta")
table.add_column("blank", style="green")
table.add_column("comment", style="green")
table.add_column("code", style="green")

def cleaned_vals(line):
	ret = []
	for i in line.split('  '):
		if i != '':
			# if i has an integer value, only then
			# strip it of white-spaces, otherwise not
			try: 
				int(i)
				ret.append(i.strip(' '))
			except ValueError:
				ret.append(i)
	
	if len(ret) == 5:
		return ret
	else: 
		console.print("[red] ERROR WITH ", ret)

for i in stroutput[7:]:
	if '-' not in i and len(i) != 0: 
		#splitted = i.split('             ')
		#splitted = i.split('        ')
		# example of what splitted holds : ['Python', '1', '4', '3', '24']
		splitted = cleaned_vals(i)
		#print(splitted)
		table.add_row(splitted[0],
					  splitted[1], 
					  splitted[2], 
					  splitted[3], 
					  splitted[4]) 
console.print(table, justify="center")

console.print("Total Number of rows : ",len(stroutput))
console.print("Credits for Beautifying, mubeenghauri", style="green")
