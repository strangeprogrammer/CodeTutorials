# HOW TO CREATE A TUTORIAL

## PREPARATION

NOTE: The directory **./** used throughout this document references the directory containing this file.

All URL considerations are already taken care of for you. You do not have to manipulate URLs nor PATHs in order to allow a client access to a tutorial, since the process is automatic. However, you may want to run the following when you are done creating your tutorial, and after sourcing **devtools.sh**:

```bash
openaccess [TUTORIAL_NAME]
```

Once the tutorial has been created successfully, it should be available at the URL [http://localhost/CodeTutorials/tutorials/tutorial_name/](http://localhost/CodeTutorials/tutorials/tutorial_name/).

You should probably acquaint yourself with Django's template system before reading through the rest of the guide since the tutorials are run through it before being pushed to the client's browser.

#### USEFUL TERMS
Code Form: A form-like construction that the client can interact with to edit code, reset the code to its original state, submit code, and get results of said submission back.

#### EXAMPLE
An example tutorial has been provided in the folder **./templates/tutorials/example-tutorial/**. You should either remove or 'chmod a-r' it in production.

#### EXTERNAL DOCUMENTATION
Documentation for **client/codeClient.js**, **client/boxSetup.js**, **client/CodeBox.html**, and **client/CodeRunner.html** is available under **CodeTutorials/djangobox/src/client/doc/**.

## CREATION STEPS

#### STEP 1:
Start by creating a folder under **./templates/tutorials/** with a slug for a name (string of only letters, numbers, hyphens, and underscores). Then, copy the contents of the example tutorial folder into this new one. This new copy will be modified throughout the rest of this guide. Finally, enter this new directory.

#### STEP 2:
Open the file **./main.html** in a text editor and go to comment 3 (starts with '{# 3:' and ends with '#}'). The following paragraph communicates a little about its postceding script tags.

The first script tag following the comment links to a file called **codeClient.js**. This file is responsible for allowing the browser to send code and STDIN via POST requests to be run by the server. The second script tag links to a file called **boxSetup.js**. This file acts as a coordinator between **codeClient.js** and CodeMirror, and performs some setup operations. Its constructors return objects representing code forms. If you need more fine-grained control over communication with the server, such as using your own event handlers when the browser gets a response, you may want to create your own wrapper over **codeClient.js** instead of including **boxSetup.js**.

In comments 4 through 7, you will find that 3 constructors from the file **boxSetup.js** are being invoked: 'cbox', 'pybox', and 'rbox'. Each takes a URL to submit the code and STDIN to, as well as an HTML 'id' attriute to which it is bound (this will be used later when templates for the code forms are included).

If you wish to create your own code form, be sure to invoke a constructor from the file **boxSetup.js** in window.onload. 

#### STEP 3:
As illustrated by comments 8 through 10, anywhere that you wish to include a code form wihin the main text of your tutorial, you should instead create a new file and include it at that point in **./main.html** using Django's template system, passing in the HTML **id** (declared earlier) that the new code form will be associated with. This is so that the constructors used earlier will be able to identify the HTML elements that they are to act upon.

#### STEP 4:
Open the file **./boxa.html**. If you have created any files that you need to include to create a code form, model them after this one, for example. The file should be extended from **client/CodeBox.html**, or **client/CodeRunner.html** if you would like some finer-grained control (though you will have to add some container code around its inclusion in **./main.html** as a result).

If you are extending these new files from **CodeBox.html**, then the template blocks that you can use in these new files are **preamble**, **presetcode**, **presetSTDIN**, and **codelang**, and **postamble**. Fill in these blocks with HTML that you would like to be within the same container element but before the code form, the preset code, the preset STDIN, the language of the code that is to be run, and HTML that you would like to be within the same container element but after the code form (respectively).

Note that the block **presetSTDIN** must contain exact whitespacing to work properly. The block **codelang** is requried to be filled by one of 'C', 'R', or 'python', though it is whitespace-agnostic.

## SECURITY CONCERNS
Currently, uploading tutorials should only be done by administrators after the tutorial in question has been properly screened (though, certainly, anyone could be a writer of such a tutorial). At the time of this writing, this is the safest and easiest way to manage tutorial uploads.