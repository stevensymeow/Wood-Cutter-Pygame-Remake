PYI = pyinstaller

.PHONY: main

main_src = main.py
main_name = "Wood Cutter"
main_icon = mochicat.ico
main_data_dir = assets
main_flags = --noconsole --onefile --icon=$(main_icon) --name=$(main_name) --add-data "$(main_data_dir);$(main_data_dir)"

main: $(main_src)
	$(PYI) $(main_flags) $<
