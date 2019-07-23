# Industrial Robots README

Industrial Robots is an open source visual studio code and VSCodium extension that aims to provide syntax highlighting. This extension aims to support most of the industrial robots currently in use.

## Features

Currently Industrial Robots supports the following robots and their associated programing languages.
> - ABB
> - KUKA
> - Comau
> - Motoman
> - Fanuc
> - Universal Robots
> - Staubli
> - Kawasaki

Additional screenshots of the syntax highlighting are attached at the bottom

## Requirements

Installing the add-on has no requirements, simply install Industrial Robots from within visual studio like any other add-on.
If you are using RoboDK the add-on should already be installed in the integrated version of VSCodium.

## Building and making changes

The files in the python directory of the plugin are used to add and remove keywords and regular expressions to the add-on. The python scripts run under python 2 or 3. You edit the python called theme_NAME which relies uses a common library to apply the changes to the plugin.

Most of the functions contained within the python files are self descriptive and can be understood by looking at on the languages implementation.

repo_match() can either take a list of keywords to add to that category or a regular expression. If there is a "\\" at the start of the string it will be interpreted as a regular expression and passed as is to the json in field specified in the function.

If there is not a "\\" at the start of the string it will generate a regular expression that highlights all the space separated words in the string. As such you must not have any trailing spaces in these strings or the regular expression generated will break that files syntax.

To add a new language you would make a new python file based on the currently existing ones and modify the keywords as necessary. After modifying and running the script you also need to manually edit the plugins package.json file and the files that where generated.

## Known Issues

No known issues.

## Release Notes


### 1.0.0

Initial release of Industrial Robots plugin.

-----------------------------------------------------------------------------------------------------------

## Screenshots

![Image of Yaktocat](/screenshots/Fanuc.png)
