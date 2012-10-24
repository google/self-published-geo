# [NOTES]
# github workflow outline:
#     http://scottchacon.com/2011/08/31/github-flow.html

SRC := "draft"
SRCXML := $(SRC).xml
DSTTXT := $(SRC).txt

text:	
	xml2rfc $(SRCXML) $(DSTTXT)

# Pull and update this repository.
update:
	git pull -v -u

push:
	git push -v
