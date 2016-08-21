crf_learn crf_template TrainData/train_all_data.txt model
crf_test -m model TestData/correct_all_data.txt > correct_output.txt 

