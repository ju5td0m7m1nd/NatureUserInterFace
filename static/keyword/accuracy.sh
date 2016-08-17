sentencenum=0
accurate=0

while read line
do
  size=${#line}
  predictLabel=${line:$size-1:1}
  correctLabel=${line:$size-3:1}
  if [ $predictLabel = $correctLabel ]; then
    accurate=$((accurate+1))
  fi;
  sentencenum=$((sentencenum+1))
done < correct_output.txt
bc <<< "scale=2; $accurate / $sentencenum" 

