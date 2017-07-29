This client has dependencies.
The DefConGui class is available in this repo, but
the base64 methods come from apache.commons.codec and
DNS MX record comes from xbill.DNS. Download those libraries
and extract them here so you have the following directory structure


.
./DefConGui
./org
./org/apache
./org/apache/commons
./org/apache/commons/codec
./org/apache/commons/codec/binary
./org/apache/commons/codec/digest
./org/apache/commons/codec/language
./org/apache/commons/codec/language/bm
./org/apache/commons/codec/net
./org/xbill
./org/xbill/DNS
./org/xbill/DNS/spi
./org/xbill/DNS/spi/services
./org/xbill/DNS/tests
./org/xbill/DNS/utils
./org/xbill/DNS/windows


Building:

make
make jar

Running:

java -jar DefConGui-1.jar

