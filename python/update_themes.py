global language_i
global repository
global config_i

def ToJSON(python_var):
    import json
    strok = json.dumps(python_var, sort_keys = True, indent=4)
    #return strok.replace("\\\\","\\")
    return strok

def getFileSyntax(id_lang):
    id_nospace = id_lang.lower().replace(" ","-") 
    return "./syntaxes/syntax.%s.json" % id_nospace 

def getFileSnippet(id_lang):
    id_nospace = id_lang.lower().replace(" ","-") 
    return "./snippets/snippet.%s.json" % id_nospace 

def getFileConfig(id_lang):
    id_nospace = id_lang.lower().replace(" ","-") 
    return "./cnfg.%s.json" % id_nospace 

def getScopeName(id_lang):
    id_nospace = id_lang.lower().replace(" ","-") 
    return "robodk.%s" % id_nospace 

def matchRegex(string):
    if string.startswith("\\"):
        return string
    
    return "(?i)\\b(" + string.replace(" ", "|") +")\\b"
    
    
def repo_begin_end(repo, begin, end, name, match_type):
    repository_i = {}
    repository_i['begin'] = begin
    repository_i['end'] = end
    repository_i['name'] = name
    repo[match_type] = {'patterns': [repository_i]}
    return repo

def repo_match(repo, match, name, match_type):
    repository_i = {}
    repository_i['match'] = match
    repository_i['name'] = name
    match_type_seed = match_type
    count = 0
    while match_type in repo:
        count += 1
        match_type = match_type_seed + str(count)
        
    repo[match_type] = {'patterns': [repository_i]}
    return repo



def update_config(id_lang, config_i):
    file_config = getFileConfig(id_lang) 
    file_str = ToJSON(config_i)
    with open("../" + file_config, "w") as fid:
        fid.write(file_str)

def update_syntax(id_lang, repository_i):
    # For each language: Auto generate patterns (syntax file)
        syntax_i = {}
        file_syntax = getFileSyntax(id_lang) 
        patterns_i = []
        for key in repository_i.keys():
            for i in range(len(repository_i[key]['patterns'])):
                if 'match' in repository_i[key]['patterns'][i].keys():
                    repository_i[key]['patterns'][i]['match'] = matchRegex(repository_i[key]['patterns'][i]['match'])
                
            patterns_i.append({"include":"#"+key})

        syntax_i["name"] = id_lang
        syntax_i["scopeName"] = getScopeName(id_lang) 
        syntax_i["patterns"] = patterns_i
        syntax_i["repository"] = repository_i
        file_str = ToJSON(syntax_i)
        #print(file_str)
        with open("../" + file_syntax, "w") as fid:
            fid.write(file_str)



# Set default color names
# (look for scopes in dark_vs.json)
name_comment = "comment"
name_string = "string"
name_numeric = "constant.numeric.c"
name_control = "keyword.control"
name_movements = "entity.name.function.preprocessor.c" #"keyword"
name_builtInTypes = "storage.type.c"
name_builtInFcn = "entity.name.function.c"
name_builtInVar = "constant.language"
name_operator = "keyword.operator"


# Set default configuration:
default_config = {
    "comments": {
        "lineComment": ";"    
    },
    "brackets": [
        ["{", "}"],
        ["[", "]"],
        ["(", ")"]
    ],
    "autoClosingPairs": [
        ["{", "}"],
        ["[", "]"],
        ["(", ")"],
        ["\"", "\""],
        ["'", "'"]
    ],
    "surroundingPairs": [
        ["{", "}"],
        ["[", "]"],
        ["(", ")"],
        ["\"", "\""],
        ["'", "'"]
    ]
}



def update_themes_all():
    global language_i
    #global repository
    #global config_i
    languages = []

    import os, glob, codecs
    import copy
    #os.chdir(".")


    # Bypass pylint errors
    language_i = {}

    # Iterate through all theme files
    theme_files = glob.glob("./theme_*.py")
    for file in theme_files:
        # Execute the file
        print("\nRunning theme: " + file + " ...")
        file_text = codecs.open(file, "r", "utf-8").read()
        exec(file_text, globals())
        print("Done with " + file)

        # Add the language to the full list of languages
        language_i_copy = copy.deepcopy(language_i)
        languages.append(language_i_copy)
        print("Len = %i" % len(languages))
        

    print("\n\nUpdating configuration file (%i languages) ..." % len(languages))
    package = {}
    package["languages"] = languages
    grammars = []
    snippets = []

    # Auto generate grammars and snippets
    for i in range(len(languages)):
        language_i = languages[i]
        id_lang = language_i["id"]   
        scope_name = getScopeName(id_lang) 
        file_syntax = getFileSyntax(id_lang) 
        file_snippet = getFileSnippet(id_lang) 

        grammar_i = {}
        snippets_i = {}
        
        grammar_i["language"] = id_lang
        grammar_i["scopeName"] = scope_name
        grammar_i["path"] = file_syntax
        snippets_i["language"] = id_lang
        snippets_i["path"] = file_snippet    

        grammars.append(grammar_i)
        snippets.append(snippets_i)

    package["grammars"] = grammars
    package["snippets"] = snippets

    str_package_contributes = ToJSON(package)

    with open("../package.json", "w") as fout:
        with open("../package_model.json") as fin:
            for line in fin:
                fout.write(line.replace("###contributes###", str_package_contributes))
                
    print("Done")



if __name__ == "__main__":
    update_themes_all()
    import time
    print("\nClosing in 1 second...")
    time.sleep(1)



















