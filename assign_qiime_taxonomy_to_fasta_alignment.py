import click
import os 
from Bio import SeqIO
import csv
from glob import glob
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

@click.command()
@click.option('--taxonomy','-t', default= "taxonomy.csv", help='tab separated taxonomy file: "name \t qiime formatted taxonomy or species name"')
@click.option('--extension','-e', default= 'fas', help='extension of the file to be processed')
@click.option('--input_path','-p', default= './', help='path where the fasta files are')

def substitute_headers(taxonomy, extension, input_path):
	#print(taxonomy, extension, input_path)
	for f in glob(os.path.join(input_path, "*." + extension)):
		count = 0
		header_changed_list = []
		print("Working on file: ",f)
		if f.endswith(extension):
			with open(f.rstrip("\.fas") + "_renamed.fasta","w") as fasta_renamed:	
				with open(taxonomy, 'r') as tax:
					csv_tax = csv.reader(tax, delimiter='\t')
					for line in csv_tax:
						for seq in SeqIO.parse(f,"fasta"):
							# add a sequecne to the output file after adding th taxonomy string to it
							if line[0] == seq.id:
								header_changed_list.append(line[0])
								#print(seq.id)
								#print(line[1])
								count += 1
								#this strips the old header out (.id is only the accession in theory .description is the whole header instead
								seq.description = ""
								seq.id = seq.id +"_"+ line[1]
								# replace sequence with the same but uppercase
								sequence = str(seq.seq).upper()
								# arrange sequence and id in a format that SeqIO can write to file
								record = SeqRecord(Seq(sequence), seq.id, "","")
								SeqIO.write(record, fasta_renamed,"fasta")
				# now that all the header which are present in the taxonomy file are writtewn to file, take the list of the changed header and only add to fasta the seqs whose headers are unchanged
				for seq1 in SeqIO.parse(f,"fasta"):
					if seq1.id in header_changed_list:
						pass
					else:
						header_changed_list.append(seq1.id)
						SeqIO.write(seq1, fasta_renamed,"fasta")
 		
		print("Added ", count, "species name or taxonomy to ",f," alignment headers" )
							
							
							
							
# starts the function
if __name__ == '__main__':
	substitute_headers()
				
		


	
	

















"""
supermatrix_accession_file = path_to_finaltrees + 'Accessions_not_found.csv'
	accessions_plus_taxonomy_file = path_to_finaltrees + 'Accessions_plus_taxonomy.csv'
	with open(supermatrix_accession_file, 'w') as accessions, open(accessions_plus_taxonomy_file, 'w') as accessions_tax,\
			open(supermatrix_file, 'r') as supermatrix, open(os.path.join(main_script_dir, "Accession_plus_taxonomy_Pezizomycotina.txt")) as tax_in:
		supermatrix_content = supermatrix.readlines()
		all_accessions = []
		accessions_added = []
		for line in supermatrix_content:
			regex = re.search("^>(GCA_[0-9]+\.[0-9])", line)
			if regex:
				all_accessions.append(regex.group(1))
			else:
				pass
		for line in tax_in:
			if line.split(",")[0] in all_accessions:
				accessions_tax.write(line)
				accessions_added.append(line.split(",")[0])
			else:
				pass
		#by this point, all previously known taxonomies have been added
		for id in accessions_added:
			all_accessions.remove(id)
		accessions.write("\n".join(all_accessions))
"""
