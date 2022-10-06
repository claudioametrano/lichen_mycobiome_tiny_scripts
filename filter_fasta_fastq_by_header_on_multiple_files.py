#USE: export sequence from the list file (one header per line ) from fasta in a new file, work on multiple files selected by extension
import os 
import re
from Bio import SeqIO
import glob
 
path = os.getcwd()

header_list = []

header_file_list = input("Input the header list file name (one header per line): ")			
with open(header_file_list, 'r') as filehandle:
	for line in filehandle:
		# remove the linebreak which is the last character of the string
		currentPlace= line[0:-1]
		#append headers to the list
		header_list.append(currentPlace)
print(header_list)

extension = input("extension of the fasta or fastq files to be filtered (no '.' needed, example: fas): ")
#print (path)
for seq_file in glob.glob(path + "/*." + extension):
	#print(seq_file)
	count_discarded = 0
	count_seq = 0
	for record in SeqIO.parse(seq_file, "fasta"):
		count_seq += 1
		if record.id in header_list:
			#print(record.id)
			with open(seq_file + "_filtered.fasta", "a") as output_handle:
				SeqIO.write(record, output_handle, "fasta")
		else:
			#print("the sequence ",record.id,"is not in the list and therefore is discarded!")
			count_discarded +=1 
	print("Sequences discarded for file ",seq_file,": ", count_discarded) 			
	print("Total sequences were: ",count_seq) 	
