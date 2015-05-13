default:
	@echo "'make check'" to run tests
	@echo "'make lint'" to run flake8 checks
	@echo "'make ui'" to compile ui files


.PHONY: check
check:
	nosetests -v pygesture


.PHONY: lint
lint:
	flake8 --config=tools/flake8.cfg \
		pygesture/ \
		config.py \
		examples/analyze \
		examples/process


PYUIC=pyuic4
UI_DIR=pygesture/ui
UI_TEMPLATES=$(UI_DIR)/calibrationdialog_template.ui \
			 $(UI_DIR)/settings_template.ui          \
			 $(UI_DIR)/main_template.ui              \
			 $(UI_DIR)/train_template.ui             \
			 $(UI_DIR)/train_widget.ui               \
			 $(UI_DIR)/test_widget.ui                \
			 $(UI_DIR)/test_template.ui              \
			 $(UI_DIR)/signal_dialog_template.ui     \
			 $(UI_DIR)/signal_widget.ui

.PHONY: ui
ui: $(patsubst %.ui,%.py,$(UI_TEMPLATES))

%.py: %.ui
	$(PYUIC) $^ -o $@
