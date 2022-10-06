import os
import re
import click


def compare_qiime_taxonomy(taxo1_string, taxo2_string):
    best_taxonomy=""
    taxo1_list=taxo1_string.split(";")
    taxo2_list=taxo2_string.split(";")
    for i,j in zip(taxo1_list,taxo2_list):
        #print(i,"<-->",j)
        if i==j:
            #longest taxonomy is selected (even if unidentified, at least all fields are filled)
            if len(taxo1_list) > len(taxo2_list):
                best_taxonomy = taxo1_string
                print(best_taxonomy)
            elif len(taxo2_list) > len(taxo1_list):
                best_taxonomy = taxo2_string
                print(best_taxonomy)
            else:
				#they should be the same, so taxo1 or taxo2 is the same
                best_taxonomy = taxo2_string
                print(best_taxonomy)
        else:
            print(i," not equal to ",j)
            if "unidentified" in i or "Unassigned" in i:
                best_taxonomy=taxo2_string
            elif "unidentified" in j or "Unassigned" in j:
                best_taxonomy=taxo1_string
            else:
                print("WARNING: the two taxonomies are in conflict: ",i,"<-->",j)
                best_taxonomy="WARNING"       
    #print("******************************************************")
    return(best_taxonomy)

@click.command()
@click.option('--input_taxonomy1','-t1', default='./taxonomy_1.csv', help='', required=True)
@click.option('--input_taxonomy2', '-t2', default='./taxonomy_2.csv', help="", required=True)
@click.option('--output_taxonomy','-o', default='./output_taxonomy.csv', help='', required=True)
def compare_taxonomy(input_taxonomy1, input_taxonomy2,output_taxonomy):
    """Takes two qiime taxonomy files as input and compare feature with the same name, the deepest taxonomy is reatainied if the taxonomy strings differ for the same qiime feature""" 
    # does not work as many taxonomy strings lack many ranks! let's use split(;)  
    #taxonomy_string_format_regex = '(.+?)\tk__([A-Z][a-z]+);p__([A-Z][a-z]+);c__([A-Z][a-z]+);o__([A-Z][a-z]+);f__([A-Z][a-z]+);g__([A-Z][a-z]+);s__([A-Z][a-z]+_[a-z]+)\t[0-9]'
    feature_list = []
    with open(input_taxonomy1, 'r') as taxo1:
        dict_feature1=dict(i.split("\t")[0:2] for i in taxo1)
        with open(input_taxonomy2, 'r') as taxo2:
            dict_feature2=dict(i.split("\t")[0:2] for i in taxo2)
    with open(output_taxonomy, 'w') as output_tax:                  
        #print(dict_feature1)
        #print(dict_feature2)
        for key1 in dict_feature1:
            for key2 in dict_feature2:
                if key1==key2:
                    print("Working on ", key1)
                    best_taxonomy_on_earth=compare_qiime_taxonomy(dict_feature1[key1],dict_feature2[key2])
                    output_tax.write(key1 + "\t" + best_taxonomy_on_earth + "\n")
# starts the function					
if __name__ == '__main__':
    compare_taxonomy()
		
