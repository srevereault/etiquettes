!#/bin/bash

for TYPE in Bénévole Speaker Staff Sponsor Bird Entrée Presse
	do 
		echo Vérification du nombre : $TYPE
		echo -n AWK : 
		awk "/$TYPE/" $1 | wc -l
		echo -n GREP : 
		grep -c "$TYPE" $1
	done


read -p "On y va ? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	for TYPE in Bénévole Speaker Staff Sponsor Bird Entrée Presse
	do 
		echo génération du csv : $TYPE
		awk "NR == 1 || /$TYPE/" $1 > $TYPE.csv
		echo génération du pdf : $TYPE
		python etiq.py -i $TYPE.csv 
		mv basic.pdf $TYPE.pdf
	done
fi

## Un peu de cosmetique
mv Entrée.pdf participant.pdf
mv Bird.pdf early_bird.pdf 
