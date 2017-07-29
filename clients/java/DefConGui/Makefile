JAVAC = /usr/lib/jvm/java-7-openjdk/bin/javac
JFLAGS = -g
JAR = /usr/lib/jvm/java-7-openjdk/bin/jar -cmvf
MANIFEST = MANIFEST.MF

VERSION = 1

DNSSRC = org/xbill/DNS/*.java \
	 org/xbill/DNS/utils/*.java

PROGSRC = DefConGui/*.java

DNSCLASS = org/xbill/DNS/*.class \
	   org/xbill/DNS/utils/*.class

B64CLASS = org/apache/commons/codec/*.class \
	   org/apache/commons/codec/*/*.class

PROGCLASS = DefConGui/*.class


JARFILE = DefConGui-${VERSION}.jar

all:
	${JAVAC} ${JFLAGS} ${PROGSRC} ${DNSSRC}

jar:
	${JAR} ${MANIFEST} ${JARFILE} ${PROGCLASS} ${DNSCLASS} ${B64CLASS}
