# The Fairytale School of MFL: Intervention Identifier

## Concept

The Fairytale School of MFL is monitoring its students' achievements in language-learning closely and want to target areas for development as their Year 10 pupils move into their final GCSE year of examinations. 

They need a programme that can track student data based on their achievement in each module taught throughout the GCSE programme, combined with data from the mock GCSE examination results, and inform them of the modules of study that need to be revisited for further consolidation as well as specific examination skills where pupils need most practice. 

This programme is designed for the user (teachers at the school) to input student data, calculate a median percentage of achievement per module and exam skill, update the worksheets with the recorded data, and identify the primary module and skill to target for intervention sessions. 

Given the large amount of data teachers can acquire due to class sizes and quantity of assessments, this programme is designed to provide an instantaneous way for teachers to know where they need to target their focus when approaching exam study for their pupils, without the need for analysing streams of data manually. 

This can be adapted to be used by class for individual teachers' personal approach based on their students' data, or by a Head of Department to assess the overall consensus based on a whole cohort of students' results, thereby meeting a variety of needs within a Modern Foreign Languages department. 

## How to use the programme

As explained, the Intervention Identifier is designed to identify the specific areas of intervention required for a class of Year 10 pupils studying Modern Foreign Languages moving into their final year of GCSE examination studies. 

When the programme loads, the user (a teacher), is asked to input the student data acquired at the end of the academic year. 
This data needs to be in the format of: student name, target grade, module 1 data, module 2 data, module 3 data, module 4 data, module 5 data, reading mock data, listening mock data, writing mock data, speaking mock data. 

Once the data is entered, the programme does the following:
* Inputs the data into the linked Google Sheet.
* Calculates the average percentage of all accumulated data by column.
* Updates the separate median data Google Sheet.
* Identifies the lowest value of data by both module and exam skill separately. 
* Identifies the module and exam skill targeted by name.
* Updates the separate foci Google sheet.
* Prints to the terminal for the user to see: the module of study to be re-taught/revised, and the exam skill to be practiced.

## Logic Path Flow Chart

The programme needs to follow a specific path of logic in order to accurately read and calculate the data required by the user. For this, I have created the flow chart as seen below: 

<img src = "assets/images/programme_flow_chart.JPG">

## Features

### Existing Features