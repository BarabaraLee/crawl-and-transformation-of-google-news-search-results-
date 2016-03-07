Task: In each title of the google news search results for 'IOWA and REPUBLICAN and VISIT', replace the candidate's name with the most popular girl's name in the year which is the same as the candidate's birth year. To finish the task, two steps must be performed sequentially.
Author: Linjun Li
Company: Virginia Tech

STEP 1
——————————————————————————————————————————————————————————————————————————————————————————————————————
Produce a summary of the result of searching google news for “IOWA and REPUBLICAN and VISIT”.

Scripts: gsearch.py (slightly modified from https://github.com/meibenjin/GoogleSearchCrawler)

Input arguments:
1) 'IOWA REPUBLICAN VISIT'

Notes: 
1) Expected number of news can be changed by resetting expect_num=100 in line-199.
2) The searching result with 'IOWA REPUBLICAN VISIT' as input is the same as the searching result with 'IOWA and REPUBLICAN and VISIT' using the google news webpage in web browser.
3) The summary of result includes 'url', 'title' and 'content' for each piece of news.
4) The excecutable user_agents should be included in the same folder where the script is saved.
5) We need to use '>title.txt' to save the summary result.

To use the script, run:
python gsearch.py [Key Words] > [file name of summary]
Example: python gsearch.py 'IOWA REPUBLICAN VISIT' > titles.txt

STEP 2
——————————————————————————————————————————————————————————————————————————————————————————————————————
Extract the titles from the titles.txt file produced in STEP1, replace the candidate's name with the  most popular girl's name in the year (which is the same as the candidate's birth year).

Script: ChangeNames.py (hand coded by Linjun Li)

Notes: 
1) There's no input argument required, but the following files should be saved in appropriate directory:
	a) 1915-2014.csv
	b) titles.txt (this file name can be different if STEP1 produced a file with another name).
2) The directory which includes the above two files should be specified in line-88 of this script.
3) There are 16 Republican candidate has their names changed (from wikipedia: https://en.wikipedia.org/wiki/Republican_Party_presidential_candidates,_2016), excluding Rick Perry, who withdrew before the primaries.

To use the script, run:
python ChangeNames.py
