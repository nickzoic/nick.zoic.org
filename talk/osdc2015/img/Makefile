DIAFILES := $(shell find . -name '*.dia')
SVGFILES := $(patsubst %.dia,%.svg,$(DIAFILES))

ALL: $(SVGFILES)

%.svg: %.dia
	dia -e $@ $<
