## GIT WORKFLOW for Making changes

For Simplicity we all download Github desktop

1. first create a folder anywhere in your want the project to be in
2. Open github desktop click on the top left corner with current repository
3. you will see a add dropdown button click it and press "clone repository"
4. paste https://github.com/weiwen-bot/esd-budget-app into the URL textbox and choose the path where you created the folder. Then click clone
5. you should observe that you have all the files inside your local machine
6. Then click the current branch in the github desktop
7. You will then create a new branch based on the dev branch (New branch will be the name of the stuff you are working on)

## Working in your branch

1. Ensure you are in your own branch NOT "dev" OR "main"
2. Once your in your own branch that you have created you can start editing your code.

## Making a commit to save your work

1. Once you finish a function or want to save
2. go to github desktop and click commit
3. Push origin

## Writing a commit message

1. Writing a message shouldnt be long but should contain enough information

## Types for Header

- feat - When adding new feature, function
- fix - Making a change to fix something
- docs - Making a change on documentation Readme
- style - style change css
- config - Making changes to dockerfile or yaml

## Message example

- feat(service api): create user
- Description: This commit adds a new feature that creates a new user

- fix(service api): address issue for when user are created without name
- Description: This commit fix the bug where the function can take empty message. The fix will now check for empty message and return error

## When you want to push all working changes to dev once you are done with your features

1. Commit all changes in your own branch first
2. Push to origin and fetch origin
3. Go to Dev branch and fetch origin first than and push origin. Go back to your own branch
4. Click your own branch and the button below "Choose a branch to merge into 'your own branch' "
5. Select dev branch (This will merge all latest commits done to dev to your own branch)
6. fix any merge conflicts if any if unsure can ask in the group for help
7. Push origin and fetch origin
8. Now you can send pull request to the dev
9. Preview pull request
10. Select dev instead of main
11. you will be redirect to the github page.
12. Press create pull request
13. Inform the group someone will review the Pull request and merge it
14. Person completing the merge request will delete branch on the github online page
15. Also delete the branch on your github desktop (After the Pull request)
16. To start new features create new branch from dev branch and repeat.

# General rule of thumb

1. Before merge committing any code to dev remember to fetch origin for latest updates
2. Write short and clear commits so its easier to track what has been done.
3. If unsure of workflow please communicate in the group
4. Perform commits frequently

# signature

Chengkhee
Shane
Gui Quan
Yuan Zhi