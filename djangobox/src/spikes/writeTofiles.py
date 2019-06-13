# Daniel Darcy
# In order for this to work correctly the lookup variables must be changed accordingly.
# When migrating this to actual system the 'lookup' variable for each function will probably need to be changed
# USER MUST NOT INPUT: PARENTHESES, COLON, SEMI-COLON, QUOTES, %, ONLY LETTERS AND NUMBERS

import io

# addView function modfies views.py
def addView(pathname):
    lineNumber1=0
    addedBlock = '\ndef '+ pathname + '(request, *args, **kwargs):\n\treturn render(request, "' + pathname + '.html", {})\n'
    lookup = 'return render(request, "JSONDialogV2.html", {\'timeout\': (CONT_GRACE + CONT_TIMEOUT) * 1000})'
    with open('spikes/views.py', 'r') as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                lineNumber1 = num

    with open('spikes/views.py', 'r') as myFile:	#Reopen and save as data
        viewsData = myFile.readlines()
    viewsData[lineNumber1-1] = viewsData[lineNumber1-1] + addedBlock
    with open('spikes/views.py', 'w') as myFile:		#Reopen AGAIN as write
        myFile.writelines(viewsData)		#Rewrite whole thing with new modified data

    return lineNumber1


# addURL function modfies urls.py
def addURL(pathname):
    lineNumber2=0
    addedBlock = '\t' + pathname + ',\n'
    lookup = '58ufhd763'	#Had to write a 'key' in comments of urls.py for line number purposes
    with open('spikes/urls.py', 'r') as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                lineNumber2 = num

    with open('spikes/urls.py', 'r') as myFile:	#Reopen and save as data
        urlData = myFile.readlines()
    urlData[lineNumber2-1] = urlData[lineNumber2-1] + addedBlock
    with open('spikes/urls.py', 'w') as myFile:		#Reopen AGAIN as write
        myFile.writelines(urlData)		#Rewrite whole thing with new modified data

    return lineNumber2


# importFromViews function modfies urls.py
def importFromViews(pathname):
    lineNumber3=0
    addedBlock = '\tpath(\'' + pathname + '/\', ' + pathname + ', name = \'' + pathname + '\'),\n'
    lookup = 'path(\'JSONDialogV2/\', JSONDialogV2,	name = \'JSONDialogV2\'),'
    with open('spikes/urls.py', 'r') as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                lineNumber3 = num

    with open('spikes/urls.py', 'r') as myFile:	#Reopen and save as data
        urlData = myFile.readlines()
    urlData[lineNumber3-1] = urlData[lineNumber3-1] + addedBlock
    with open('spikes/urls.py', 'w') as myFile:		#Reopen AGAIN as write
        myFile.writelines(urlData)		#Rewrite whole thing with new modified data

    return lineNumber3


def addHtmlPage(pathname, htmlData):
    with open('spikes/templates/'+ pathname +'.html', 'w+') as htmlFile:
        htmlFile.writelines(htmlData)
    addView(pathname)
    addURL(pathname)
    importFromViews(pathname)
    return 0


# Main - TESTS
#addHtmlPage('Coding Tutorial Test', 'Helloo Worldd')




# Need to add user input for pathname and way to retrieve that info - HTML request?, form?
