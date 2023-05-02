cd src

# PdfToText
mkdir -p xpdf
wget https://dl.xpdfreader.com/xpdf-tools-linux-4.04.tar.gz
tar zxvf xpdf-tools-linux-4.04.tar.gz -C xpdf
rm xpdf-tools-linux-4.04.tar.gz

# HunAlign
wget ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1.tgz
tar zxvf hunalign-1.1.tgz
cd hunalign-1.1/src/hunalign
make
rm hunalign-1.1.tgz
