# [NOTES]
# github workflow outline:
#     http://scottchacon.com/2011/08/31/github-flow.html

SRC := "draft"
SRCXML := $(SRC).xml

all:	text

text:	$(SRCXML)
	xml2rfc text $(SRCXML) $(SRC).txt

# Pull and update this repository.
update:
	git pull -v -u

push:
	git push -v

.PHONY:	$(SRCXML)
