default:
	@echo "'make lint'" to run flake8 checks
	@echo "'make ui'" to compile ui files


.PHONY: lint
lint:
	flake8 --config=tools/flake8.cfg \
		pygesture/ \
		config.py \
		examples/analyze_classification \
		examples/analyze_tactest \
		examples/test_vrep.py \
		examples/test_mccdaq.py


PYUIC=pyuic5
UI_DIR=pygesture/ui/templates
UI_TEMPLATES=$(UI_DIR)/main_template.ui              \
			 $(UI_DIR)/train_widget_template.ui      \
			 $(UI_DIR)/test_widget_template.ui       \
			 $(UI_DIR)/signal_widget_template.ui     \
			 $(UI_DIR)/recording_viewer_template.ui  \
			 $(UI_DIR)/process_widget_template.ui    \
             $(UI_DIR)/new_session_template.ui       \
			 $(UI_DIR)/session_browser_template.ui

.PHONY: ui
ui: $(patsubst %.ui,%.py,$(UI_TEMPLATES))

%.py: %.ui
	$(PYUIC) $^ -o $@
