# merge_markers
Merge dietary data from multiple markers into a single dataset

<p>
The Python script here developed is composed of three distinct classes:
  
Sample: The Sample class takes an id on initiation, the purpose of this class is to hold, for each sample, all amplified markers and their correspondent prey items.

Primer: This class holds all prey items for the particular primer (defined by primer name provided on initialization).

Prey: The prey classification is stored here, on initiation it requires to know from which primer this prey is from and the line of prey classifications that must follow the order:  Class -> Order -> Family -> Genus -> Species</p>

## Expected Input

The input table needs to be formatted in the following way (without the header) as a csv file (; as separator). Make sure the csv file is UTF-8 encoded (Open the .csv in notepad -> Save As -> encoding UTF-8):

|Sample |	Marker |	Class |	Order |	Family |	Genus |	Species |	Final MOTU_name |
|:-----:|:------:|:------:|:-----:|:------:|:------:|:-------:|:---------------:|
|DL001	|18S	   |Magnoliopsida |	Rosales	  |Rosaceae |	Prunus	| unk	|Prunus sp._01|
|DL001	|18S	    |Magnoliopsida|	unk	|unk	|unk	|unk	|Magnoliopsida_05|
|DL001	|18S      |	Reptilia|	Squamata|	unk|	unk	|unk	|Squamata_02
|DL001	|ZBJ      |	Insecta|	Lepidoptera|	Noctuidae	|Autographa	|gamma|	Autographa gamma
|DL001	|ZBJ|	Insecta|	Lepidoptera|	Pterophoridae|	Emmelina|	monodactyla|	Emmelina monodactyla
|DL002	|18S|	Liliopsida|	Poales|	Poaceae|	unk|	unk|	Poaceae_03|
|DL002	|18S|	Magnoliopsida|	Asterales|	Asteraceae|	Erigeron|	unk|	Erigeron sp._01
|DL002	|18S|	Magnoliopsida|	Solanales|	unk|	unk|	unk|	Solanales_01
|DL002	|IN16STK|	Arachnida|	Araneae|	Philodromidae|	Philodromus	|Díspar|	Philodromus dispar
|DL002	|IN16STK|	Insecta|	Hymenoptera|	Formicidae|	Proformica|	unk	|Proformica sp._02
|DL002	|IN16STK|	Insecta|	Hymenoptera|	Formicidae|	unk	|unk|	Myrmicinae_04
|DL002	|IN16STK|	Insecta|	Hymenoptera|	unk	|unk|	unk|	Vespoidea_02
|DL002|IN16STK|Insecta|Orthoptera|Acrididae|Sphingonotus|unk|Sphingonotus sp._1|
|DL002|ZBJ|Insecta|Orthoptera|Acrididae|Sphingonotus|caerulans|Sphingonotus caerulans|


Sample = Sample ID

Marker = Molecular Marker where the following prey was detected

Class|Order|Family|Genus|Species = The levels of classification assumed by the script (unk mark unknown ranks)

Final MOTU_name = A MOTU name given by the user to identify the MOTU throughout the analysis

## Expected Output

The output table takes the following form (the header will not be written on the output):

|Sample|	Marker	|Class	|Order	|Family	|Genus	|Species	|MOTU	|Original Primer|	Merged?|	With Primer|	With MOTU|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
DL001|concatenated|Magnoliopsida|Rosales|Rosaceae|Prunus|unk|Prunus sp._01|18S|FALSE|
DL001|concatenated|Magnoliopsida|None|None|None|unk|Magnoliopsida_05|18S|FALSE|
DL001|concatenated|Reptilia|Squamata|None|None|unk|Squamata_02|18S|FALSE|
DL001|concatenated|Insecta|Lepidoptera|Noctuidae|Autographa|Gamma|Autographa gamma|ZBJ|FALSE|
DL001|concatenated|Insecta|Lepidoptera|Pterophoridae|Emmelina|monodactyla|Emmelina monodactyla|ZBJ|FALSE|
DL002|concatenated|Liliopsida|Poales|Poaceae|None|unk|Poaceae_03|18S|FALSE|
DL002|concatenated|Magnoliopsida|Asterales|Asteraceae|Erigeron|unk|Erigeron sp._01|18S|FALSE|
DL002|concatenated|Magnoliopsida|Solanales|None|None|unk|Solanales_01|18S|FALSE|
DL002|concatenated|Arachnida|Araneae|Philodromidae|Philodromus|Díspar|Philodromus dispar|IN16STK|FALSE|
DL002|concatenated|Insecta|Hymenoptera|Formicidae|Proformica|unk|Proformica sp._02|IN16STK|FALSE|
DL002|concatenated|Insecta|Hymenoptera|Formicidae|None|unk|Myrmicinae_04|IN16STK|FALSE|
DL002|concatenated|Insecta|Hymenoptera|None|None|Unk|Vespoidea_02|IN16STK|FALSE|
DL002|concatenated|Insecta|Orthoptera|Acrididae|Sphingonotus|caerulans|Sphingonotus caerulans|ZBJ|TRUE|IN16STK|Sphingonotus sp._1|

Sample = Sample ID

Marker = After analysis all marker entries should read concatenated

Class|Order|Family|Genus|Species = The levels of classification of the given prey item

MOTU =The MOTU kept after analysis

Original Primer = The primer from where the observation was taken

Merged? = True if other entries where merged with this one; False if no merging occurred

With Primer= Primer from where the merged information was retrieved

With MOTU = The MOTU of the merged entry

(With Primer and With MOTU could propagate in instances where multiple entries where collapsed into one)
<p></p>

## How to run
To run the script simply copy the script to a working folder and, on an open terminal inside that folder, type:

Linux: python3 merge_markers.py input_file output_file

Windows: python merge_markers.py input_file output_file





