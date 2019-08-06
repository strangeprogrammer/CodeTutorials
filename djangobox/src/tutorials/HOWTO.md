# HOW TO CREATE A TUTORIAL

## PREPARATION
All URL considerations are already taken care of for you. You do not have to manipulate URLs, PATHs, nor file permissions in order to allow a client access to a tutorial, since the process is automatic.

You should probably acquaint yourself with Django's template system before reading through the rest of the guide since the tutorials are run through it before being pushed to the client's browser.

## EXAMPLE
An example tutorial has been provided in the folder **./templates/tutorials/example-tutorial**. The following steps will be much more understandable if you have this reference on hand to consult when needed (though you should either remove or 'chmod a-r' it in production).

## Creation Steps

#### STEP 1:
Start by creating a folder under **templates/tutorials** with a slug for a name (string of only letters, numbers, hyphens, and underscores). Then, create your primary HTML file within that directory, and call it **main.html**.

#### STEP 2:
You will have to load Django's **static** module into **main.html** in order to include some useful resources. Then, you can fill the file with the HTML content of the tutorial webpage.

#### STEP 3:
Some of the resources provided by this project out-of-the-box are within various static or template files. The template files **templates/client/CodeRunner.html** and **templates/client/CodeBox.js** (preference toward **CodeBox.js**) are used to create a standard form-like structure used to transfer POST data to the server. The static files **static/client/codeClient.js** and **static/client/boxSetup.js** (preference toward **boxSetup.js** unless you need fine-control) are used to push runnable code to the server, after which the results will be returned and displayed to the user.

These files and their interfaces are the standard basis for creating webpages that interact with the server. Documentation for them is located in **src/client/doc**.

If you are content using the default options, you should include **static/client/boxSetup.js** and create some objects with the 'boxSetup' constructor (passing in a URL and an HTML **id** to be used later).

#### STEP 4:
Anywhere that you wish to include a code editor, you should instead create a new file and include it at that point in the original file using the template system, passing in the HTML **id** (declared earlier) that the new editor will be associated with.

#### STEP 5:
In any new files that you have created, fill them in with code that extends that file from **client/CodeBox.html**. The blocks that you can use in these new files are **preamble**, **presetcode**, **presetSTDIN**, and **codelang**, and **postamble**. The block **presetSTDIN** must contain the exact whitespacing to work properly. The blocks **preamble** and **postamble** are also sensitive to this.

#### STEP 6:
Only the block **codelang** is requried to be filled by one of 'C', 'R', or 'python'. The block **presetcode** may optionally contain code that will be preloaded with the webpage. The block **presetSTDIN** may optionally contain code that will be preloaded with the webpage.

## SECURITY CONCERNS
Currently, uploading tutorials should only be done by administrators after the tutorial in question has been properly screened (though, certainly, anyone could be a writer of such a tutorial). At the time of this writing, this is both the safest and easiest way to manage tutorial uploads.