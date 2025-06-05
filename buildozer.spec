[app]

title = My Kivy App
package.name = mykivyapp
package.domain = org.example

source.include_exts = py,png,jpg,kv,atlas

# Your main script (adjust if needed)
source.main = main.py

version = 0.1

requirements = python3,kivy

# Permissions (add more if needed)
android.permissions = INTERNET

# Orientation (portrait/landscape)
android.orientation = portrait

# (Optional) icon
# icon.filename = %(source.dir)s/data/icon.png

[buildozer]

log_level = 2
warn_on_root = 1
