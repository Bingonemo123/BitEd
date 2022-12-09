<h1 align="center">K For Knowledge</h1>
<p align="center">
  <img src="src/Logo.png" style="width:325px";>
</p>

[Project Vision](https://github.com/Bingonemo123/BitEd/blob/main/Vision.md)

## Milestones

### Essentials

- [ ] Home Page
  - [ ] Header
    - [ ] Logo on left
    - [ ] Search bar on middle left
      - [ ] Visual Side
      - [ ] Engine Side
    - [ ] Show Profile Balance Number on middle right
    - [ ] `Login/Sign Up` Button on right
      - [ ] Display Username (email) if Logged in
      - [ ] Link Username to Profile Page
  - [ ] Left Side Bar
    - [ ] `Create Questions` Button &#8594; Question creating Page
    - [ ] Tags and Fields List
      - [ ] Logic - Selecting one of elements from list changes body
      - [ ]  *
  - [ ]  Body
    - [ ]  Scrolling and Loading Content
      - [ ]  4 `Tests Tile` with small description of Test on each row
        - [ ]  On Tiles `Title of Test`
        - [ ]  on Tiles `Number` of Questions
        - [ ]  on Tiles 5 Main `Tags` (Main means most Abstract)
        - [ ]  on Tiles `Expected Reward` just number
      - [ ]  Clicking on Test &#8594; Goes to Test Set-Up Page of selected Test
- [ ]  Sign In/Up Page
  - [ ]  Middle Body
    - [ ]  Tile: Login
      - [ ]  Username or email  Field
      - [ ]  Password Field
      - [ ]  Forgot Password Link
      - [ ]  Create account Link
- [ ]  Create Account Page
  - [ ]  Middle Body
    - [ ]  Tile: Create Account
      - [ ]  Email Field
      - [ ]  Password Field
      - [ ]  Repeat Password Field
      - [ ]  Submit Button
- [ ]  Forgot Password Page
  - [ ]  Middle Body
    - [ ]  Enter your Email &#8594; sed email link to change password
    - [ ]  Submit Button
- [ ]  Change Password Field
  - [ ]  Password Field
  - [ ]  Repeat Password Field
  - [ ]  Submit
- [ ]  Test Set-Up Page
  - [ ]  Display `Test Title`
  - [ ]  Display `Number of Questions`
  - [ ]  Display `Tags` of Tests
  - [ ]  Switch Button `Public vs Private` Sector
    - [ ]  Logic Behind Switch
  - [ ]  Text Near Switch explaining Difference between Public and Private Sectors
  - [ ]  Switch Button Between `Exam and Training` Modes
    - [ ]  Logic Behind Switch
  - [ ]   Text Near Switch explaining Difference between Exam and Training Switch
  - [ ]   Display `Expected Reward` for Test
  - [ ]   Display `Expected Receiving  Time` for Reward
  - [ ]   `Start` Button
    - [ ]   Linking to Test Writing Page
- [ ]  Test Writing Page
  - [ ]  Header
    - [ ]  Display `Current Number of Question` out of total Question Number ( ex. 23 from 40 )
  - [ ]  Footer
    - [ ]  Display `Time Left` if Exam Mode
    - [ ]  Display `Previous and Next` Buttons
    - [ ]  Display `Submit` Button
  - [ ]  Body
    - [ ]  `Question Statement` - Text Containing Problem that user must answer.
    - [ ]  `Multiple Choice Answers` - also Text, can be selected only one. (Radio Type Input)
      - [ ]  Highlight Correct answer after Input Submitted
    - [ ]  `Explanation` - Showed after Answer Submitted, Contains Text.
  - [ ]  Logic
    - [ ]  After Pressing on `Previous and Next` Button Body shows next or previous Question. If First Question previous button does nothing. If Last Question next Question ask in prompt if user wants to exits. If yes - Goes to Results Page. If No - exits prompt and does nothing.
    - [ ]  If One of `Multiple Choice Answers` selected and Pressed `Submit` button - If Test in Exam Mode, goes to Next Question or asks prompt (discrowned above) if last Question, else Test in Training Mode shows correct answer and Explanation. If None of Answers selected `Submit` button does nothing.
- [ ]  Results Page
  - [ ]  Header
    - [ ]  Logo On Left
      - [ ]  Link To Home Page
  - [ ]  Body
    - [ ]  Display `Percentage of Correctly Answered`
    - [ ]  Display `Expected Reward` changed after
    - [ ]  Display `Expected Receiving  Time` changed after
    - [ ]  Display `Number of Users` Already Finished The Test
- [ ]  Question Creating Page
  - [ ]  Header
    - [ ]  Logo On Left
      - [ ]  Link To Home Page
  - [ ]  Body
    - [ ]  Question Statement  Input Field (max 3,000 characters)
    - [ ]  `Create Answer Option` Button (First One is Always correct one, Answers are shuffled randomly)
      - [ ]  Creates Answer Input Field (max 150 characters)
    - [ ]  Explanation Input Field  (max 10,000 characters)
    - [ ]  Tag Input Field ( each Tag max 150 characters) {`:` - subtags, `;` - separate tags from each other}
  - [ ]  Footer
    - [ ]  `Submit` Button
      - [ ]  Prompt Opens with text "Review 5 Question to Submit your Question."
      - [ ]  Goes To Test Review Page and Saves Question
      - [ ]  Question is not Submitted and only saved if Deposit Cost is higher than users balance.
    - [ ]  Text That Warns User, that he must review 5 Question in order to Question Be Submitted.
    - [ ]  Display `Deposit Cost`
- [ ]  Test Review Page
  - [ ]  Same as Test Writing Page in addition:
  - [ ]  + Footer
    - [ ]  Select From:
  
      - question is correct
      - questions is too easy
      - question is duplicate
      - question is not tagged correctly
      - question is incorrect

    - [ ]  After selecting from above `Submit Review` button.
      - [ ]  Goes to next Question or If last in Review Queue goes to Home page and prompts "you successfully submitted Question, which is under review right now"
    - [ ]  User must answer Review Question as all other usual Questions, before he can submit review.
  
- [ ]  Profile Page
  - [ ]  Change Password Button
  - [ ]  Question History
  - [ ]  Show Balance Details
  - [ ]  `Log out` Button

### Step II - Monetization

- [ ]  Add advertisements
- [ ]  Add option to Buy Points on balance

### Step III - Additional Features

- [ ]  `Edit` Button on Question Review Page
- [ ]  `Save` Button on Question Create Page
- [ ]  Report Question or Give Feedback while writing Tests
- [ ]  Search Users also at Homepage
- [ ]  Comment section For Question Review
- [ ]  Mark Question and Follow Comments on that Question
- [ ]  Login/Sigh Up With Google, github, Facebook
- [ ]  Develope rest API
