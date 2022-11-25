# Last commit: https://github.com/kpu/kenlm/commit/bcd4af619a2fa45f5876d8855f7876cc09f663af

# OSCAR SMALL
!git clone https://user:pass@huggingface.co/datasets/nthngdy/oscar-small

# UNZIP
! gzip -d oscar-small/data/*.gz

# HEAD
! head -n 10 oscar-small/data/fa

# download kenlm
!git clone https://github.com/kpu/kenlm.git

# install kenlm
%cd /content/kenlm
! pip install .

# build kenlm
%cd /content/kenlm
!mkdir -p build
%cd build
!cmake ..
!make -j 8

# Create file, each sentence in each line
# !echo -e "Hello this is amir.\nThis is new Year." >> /content/kenlm/build/corpus.txt
# !echo -e "من امیر را دوست دارم.\n امیر من را دوست دارد." >> /content/kenlm/build/corpus.txt
# ! wget https://raw.githubusercontent.com/language-ml/course-nlp-ir-1-text-exploring/main/exploring-datasets/literature/iranian/ganjoor_collection/ferdousi.txt -O /content/kenlm/build/corpus.txt

# you don't need --discount_fallback if you use your real data (which may huge)
%cd /content/kenlm/build
! bin/lmplz -o 5 </content/oscar-small/data/af_char.txt >/content/oscar-small/data/af.arpa
# ! /content/kenlm/bin/lmplz -o 2 -S 80% -T /tmp <text.txt >text.arpa --discount_fallback


! head -n 40 /content/oscar-small/data/af.arpa

# binarization
%cd /content/kenlm/build/
! bin/build_binary /content/oscar-small/data/af.arpa /content/oscar-small/data/af.binary

