# Quiz Development Tutorial
*A fair amount of the HTML and javascript in the "Multiple Choice Questions portion of the tutorial was written by Dilip HM @ quora.com.*

- Below is a tutorial which shows users how to make quizzes with multiple choice questions and/or a text editor.
- In order for the Text editor portion of this tutorial to work correctly CodeTutorials/djangobox/src/docker/docker_wrapper/runContainer.sh installation* **must be complete**.
- Common templates and important details will be provided. 

--------------------------------------------------------------------------------------------------------------------------------------

## Multiple Choice Questions
- Multiple choice questions will consist of radio buttons.
- All of the questions should be placed in a "form block" as shown below:

        <form name="quiz">        

            ... (question 1 block)
            ... (question 2 block)
            ... (question 3 block)
            ... (question n block)

        </form>
        
        
### Multiple Choice HTML Template: 
- Below is the reccomended HTML template for a quiz with one multiple choice question.
- To add more questions all one would have to do is copy and paste everything inbetween the form tags.
- Once that is complete the user should need to modify the question #, question, <input> name,  and answers (answers are located in "Required Javascript Template" portion of the tutorial).

        <form name="quiz">
            <p>
            <b>Question 1.
            <br>He -------------------- it.<br></b>        <!-- Question -->

            <blockquote>
                <input type="radio" name="q1" value="don't like">don't like<br>
                <input type="radio" name="q1" value="doesn't like">doesn't like<br>
                <input type="radio" name="q1" value="doesn't likes">doesn't likes<br>
            </blockquote>

            <p><b>
        </form>


### Required Javascript Template
- Below is the reccomended Javascript template for a quiz with one multiple choice question.
- It should be added under the html code but inside of the html tags.
- When adding multiple choice questions to this template the following variables need to be modified
        * numQues
        * answers (array)
        * the user would also need to add the new answer to the answers array for each question.
                - In this example the following would be added after the line '  answers[0] = "doesn't like";  '             
                        answers[1]= "your answer"; 
                        ...
                        answers[n]= "your last answer";
        * the getScore function should not need to be modified as long as the above "Required Javascript Template" directions are followed correctly.

        <script>

            var numQues = 1;
            var numChoi = 3;
            var answers = new Array(1);
            answers[0] = "doesn't like";

            <!-- Added Questions Answers Here -->

            function getScore(form) {  <!--Score Calculation function-->

                var score = 0;
                var currElt;
                var currSelection;
                
                for (i=0; i<numQues; i++) {
                    currElt = i*numChoi;
                    answered=false;

                    for (j=0; j<numChoi; j++) {
                        currSelection = form.elements[currElt + j];

                        if (currSelection.checked) {
                            answered=true;

                            if (currSelection.value == answers[i]) {
                                score++;
                                break;
                            }
                        }
                    }

                if (answered === false){
                    alert("Do answer all the questions, Please") ;
                    return false;
                }
            }

            var scoreper = Math.round(score/numQues*100);
            form.percentage.value = scoreper + "%";
            form.mark.value=score;

            }
        </script>


--------------------------------------------------------------------------------------------------------------------------------------

## Text Editor which can also compile and run code inputted by user


### Template


### Required HTML tags for running code.


### Form registering for codeRunner.js.

--------------------------------------------------------------------------------------------------------------------------------------

## Subscripts/Superscripts -> Markdown?


--------------------------------------------------------------------------------------------------------------------------------------

## Adding quiz to server


--------------------------------------------------------------------------------------------------------------------------------------
