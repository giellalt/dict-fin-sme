
# Dette skal bli ei makefil for å lage finsme.fst, 
# ei fst-fil som tar sme og gjev ei fin-omsetjing.

# Førebels er det berre eit shellscript.

# Kommando for å lage finsme.fst
echo "LEXICON Root" > bin/finsme.lexc
cat src/finsme.xml | tr '\n' '™' | sed 's/<e>/£/g;'| tr '£' '\n'| sed 's/<re>[^>]*>//g;'|tr '<' '>'| cut -d">" -f5,15| tr ' ' '_'| tr '>' ':'| grep -v '__'|sed 's/$/ # ;/g' >> bin/finsme.lexc
xfst -e "read lexc < bin/finsme.lexc"

#printf "read lexc < bin/finsme.lexc \n\
#invert net \n\
#save stack bin/finsme.fst \n\
#quit \n" > tmpfile
#xfst  < tmpfile
#rm -f tmpfile

# deretter i xfst:
# invert
# save bin/finsme.fst
