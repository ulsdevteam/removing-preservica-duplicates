#!/bin/bash

# Where is the ingest monitor message file downloaded from Preservica?
MESSAGEFILE=$1
if [ "$MESSAGEFILE" == "" ]
then
  >&2 echo "USAGE: $0 <filename>"
  exit 1
fi
# Where can we setup a temporary working directory?
TMPDIR=`mktemp -d`
# Have we seen any errors which require operator intervention?
ERRORFLAG=
# Where is the ingest monitor message file downloaded from Preservica?

# LOGFILE1=$1
# LOGFILE2=$2
# IDENTIFIER=$3
# if [ "$LOGFILE1" == "" ] || [ "$LOGFILE2" == "" ] || [ "$IDENTIFIER" == "" ]
# then
#   >&2 echo "USAGE: $0 <filename1> <filename2>"
#   exit 1
# fi
# # Where can we setup a temporary working directory?
# TMPDIR=`mktemp -d`
# # Have we seen any errors which require operator intervention?
# ERRORFLAG=

# # column7 is entity title
# # Use a python script to extract the fifth (islandora identifier) and sixth (preservica identifier) columns from the CSV
# cat <<'EOF'> $TMPDIR/extract-identifiers.py
# import sys
# import csv
# with open(sys.argv[1], 'r') as csvfile:
#   linereader = csv.reader(csvfile)
#   for line in linereader:
#     if line[4].startswith('pitt'):
#       print(line[6] + ',' + line[5])
# EOF

# python $TMPDIR/extract-identifiers.py $LOGFILE1 > $PWD/"$LOGFILE1"islandora.csv
# python $TMPDIR/extract-identifiers.py $LOGFILE2 > $PWD/"$LOGFILE2"islandora.csv


# sort "$PWD/$LOGFILE1"islandora.csv -o "$PWD/$LOGFILE1"islandora.csv
# sort "$PWD/$LOGFILE2"islandora.csv -o "$PWD/$LOGFILE2"islandora.csv


# #diff -u "$PWD/"$LOGFILE1"islandora.log" "$PWD/"$LOGFILE2"islandora.log" | grep 

# comm -12 ""$PWD"/"$LOGFILE1"islandora.csv" ""$PWD"/"$LOGFILE2"islandora.csv" > common_islandora.csv
# if [ $? -ne 0 ]; then
#     echo "error running comm command"
#     exit 1
# fi 

# rm $PWD/"$LOGFILE1"islandora.log
# rm $PWD/"$LOGFILE2"islandora.log

# Use a python script to extract the fifth (islandora identifier) and sixth (preservica identifier) columns from the CSV
cat <<'EOF'> $TMPDIR/extract-identifiers.py
import sys
import csv
with open(sys.argv[1], 'r') as csvfile:
  linereader = csv.reader(csvfile)
  for line in linereader:
    if line[4].startswith('pitt:'):
      print(line[4] + '|' + line[5])
EOF
python $TMPDIR/extract-identifiers.py $MESSAGEFILE > $TMPDIR/id-pairs.pipe
# python $TMPDIR/extract-identifiers.py $MESSAGEFILE > 145-islandora-preservica.csv

# Extract just the PIDs
cut -d'|' -f1 $TMPDIR/id-pairs.pipe > $TMPDIR/dsio.pids
mkdir $TMPDIR/rels-ext
# Fetch the RELS-EXT for each PID in the list
drush -qy --root=/var/www/html/drupal7/ --user=$USER --uri=http://gamera.library.pitt.edu islandora_datastream_crud_fetch_datastreams --pid_file=$TMPDIR/dsio.pids --dsid=RELS-EXT --datastreams_directory=$TMPDIR/rels-ext --filename_separator=^
if [[ $? -ne 0 ]]
then
  >&2 echo "CRUD fetch returned an error"
  ERRORFLAG=1
fi
# Iterate across each PID
while read -r line
do
  rels_ext_file=$TMPDIR/rels-ext/`echo $line | cut -d'|' -f1`^RELS-EXT.rdf
  PREF=`echo $line | cut -d'|' -f1`
  echo "PREF: $PREF"
  # Transform the RELS-EXT with our XSLT, adding in the new presericaExportDate
  # xsltproc --stringparam pref "$PREF" -o $i $TMPDIR/update-preservica-ingest.xsl $i
  #extract the ref
# preservicaRef=$(xmllint --xpath "string(//rdf:Description/islandora:preservicaRef)" --noout --namespace-islandora="http://islandora.ca/ontology/relsext#" $rels_ext_file)
preservicaRef=$(xmllint --xpath "string(//*[local-name()='preservicaRef' and namespace-uri()='http://islandora.ca/ontology/relsext#'])" $rels_ext_file)  

echo "preservica ref from islandora: $preservicaRef"
echo "$preservicaRef" >> pref-only.csv

  if [[ $? -ne 0 ]]
  then
    >&2 echo "xsltproc failed on $i"
    ERRORFLAG=1
  fi 
done < $TMPDIR/id-pairs.pipe

# Only delete the working directory if there were no errors
if [[ "$ERRORFLAG" = "" ]]
then
  rm -rf $TMPDIR
else
  >&2 echo "Examine $TMPDIR for errors"
  exit 2
fi
