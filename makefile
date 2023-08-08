GIT_TAG := $(shell git describe --tags | sed 's/v//g')

.PHONY: default
default:
	@echo "OY!"

.PHONY: test
test:
	@python3 fox_color_tests.py
	@echo "Looks good to me, boss!"

.PHONY: build
build:
	@rm -rf build
	@mkdir -p build
	@cp license fox-color-utils-license
	@zip -9 build/fox-color-utils-$(GIT_TAG).zip \
		fox_color_ren.py \
		fox_hex_utils_ren.py \
		fox_requirement_ren.py \
		fox-color-utils-license
	@rm fox-color-utils-license

.PHONY: docs
docs:
	@asciidoctor -o docs/index.html docs/index.adoc
