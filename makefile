.PHONY: default
default:
	@echo "OY!"

.PHONY: test
test:
	@python3 fox_color_tests.py
	@echo "Looks good to me, boss!"