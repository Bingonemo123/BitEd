# Vision :eyes:

## This File contains our vision for the Final Product. If you have any questions, please pull a request in this file or contact us

The Process of testifying student knowledge can be divided into four parts:

1. Creation of Questions
2. Verification of Questions
3. Answering Questions
4. Checking Answers

First of all, we need to define what exactly questions are questions.
`Question` is a multiple-choice question, created by a teacher, lecturer, professional, or just a Knowledgeable person. Creator of `Question` knows the answer to the question in advance.The Creator also develops wrong answers to multiple-choice questions. Collection of a statement of the question, correct answer and wrong answers is called `Question`.
`Questions` can be further divided into two types: `Training Questions` and `Test Questions`. Types of `Questions` are discussed in the 3rd section.

### 1. Creation of Questions

In an ideal system, everybody can create questions. It would be done through a website or a mobile application. `Question` would be uploaded on Blockchain and would wait for verification. It would be in interest of Question creator:

1. that `Question` be not too easy to answer.
2. that `Question` be properly stated and understandable.  
3. that `Question` be distinct from already existing `Questions`.
4. that `Question` be tagged correctly.
5. and most importantly that `Question's` answer set as correct by question creator, truly be correct.  

If `Question` doesn't satisfy  2, 3, and 5, it would be accepted in verification process and wouldn't be implemented into Blockchain.

**Far Vision** - There would be Question creator studio software, which would be able to create `Question` templates and upload it on Blockchain. `Question` templates would contain variable parts of `Question` and would be able to be customized automatically based on Student. For example - `Question` template could contain `Question` statement:
> A train leaves {Cairo, Madrid} at {leaving_time}, averaging {first_train_speed} mph.
Another train headed in the same direction leaves {Cairo, Madrid} at {second_train_leaving_time} am, averaging {second_train_speed} mph.
How many hours after the second train leaves will it overtake the first train?

variables `Cairo`, `Madrid`, `leaving_time`, `first_train_speed`, `second_train_leaving_time`, `second_train_speed` will be randomly generated based on question creator rules by the time student must see the question. So, that student sees:

>A train leaves Cairo at 3:00 am, averaging 30 mph.
Another train headed in the same direction leaves Cairo at 6:00 am, averaging 60 mph.
How many hours after the second train leaves will it overtake the first train?

Rules, that if `Cairo` was chosen in first place, second variable also must be `Cairo` and that `second_train_speed` must be greater than `first_train_speed`, should be provided by question creator.
With Question creator studio software, Question creators can automate the process of creating `Questions`.

**A more distant Vision** - Questions would be created by AI, which would be able to create questions based on Scientific Papers.

### 2. Verification of Questions

After a Question is submitted, it should be verified by the community. To encourage the community to verify questions, we would ask Question creators to check 5 someone else `Questions` for every their own submitted `Question`. Also, we would ask Question creators to stake some amount of `Tokens` to back  `Question`. If the `Question` that Question creator submitted doesn't satisfy verification criteria, it would be rejected and Question creator will lose the stake, a process known as slashing. This is done to discourage people from overflowing the Pool of `Questions` that are not yet verified with dummy `Questions`.

By the time of verification, verifier should check:

1. If `Question` is correct.
2. If `Question` is not too easy.
3. If `Question` is distinct from already existing `Questions`.
4. If `Question` is tagged correctly.
5. If `Question` is properly stated and understandable.

If `Question` doesn't satisfy one of these criteria, the verifier should report a problem. If `Question` doesn't satisfy 3 criteria, the verifier should indicate to original `Question`.If `Question` doesn't satisfy 4 criteria, the verifier should indicate new corrected tagging. By correcting tagging, the verifier creates a new `Question`, where the author of the original `Question` is referenced as coauthor. Correcting tagging can increase the chance of `Question` being accepted. Verification of new `Question` with corrected tagging and original `Question` is done independently. So that `Question` with updated tagging may be rejected, while the original `Question` is accepted and the author of the original `Question` does not lose any of the stakes.

Editing of `Question` by the verifier is done in the same way, as correcting tagging. By editing `Question` verifier creates a new `Question`, where the original author is also referenced. For the reason that editors are creating new `Questions`, they also should back edited `Questions` with `Tokens`.

Acceptance of `Questions` is done in an election manner. `Question` must pass some threshold votes to be accepted. If there is a dispute about whether the `Question` is worthy or not, it would be passed for verification to more experienced verifiers and a wider audience. This process will continue until the dispute is resolved. Experienced verifiers, that have more proof of their education on their account, will have more voting power. Correlation between voting power and experience is done so that no small number of experienced verifiers can dominate the election.

After `Question` is accepted and the process of answering `Questions` is started, `Question` is still in the verification stage. Post-acceptance verification of `Question` is done in the same way as pre-acceptance verification of `Question`, but students can report a problem with `Question` during answering.Post-acceptance verification is a permanent process and is done until `Question` exists on Blockchain.

#### Acceptance vs Rejection

To avoid unsensible acceptance/rejection of `Questions` by verifiers, we ask them to answer `Question` before voting. If `Question` is not properly stated and understandable, statistics will show at the end of the voting process, that on average every answer was chosen with the same quantity (the number of choices for every possible answer was the same) or it had some kind of bimodal distribution. A low rate of passability, especially among experts who have more proof of their education, will be a sign of a bad `Question`. If `Question` is too easy, passability will also reflect that.

Voting will require a small bounty (<span>\$</span>0.035 for example) to stake while choosing between acceptance and rejection. If verifiers are choosing rejection, they are also required to choose the reason for rejection. Bounty is accumulated and stored until `Question` is verified. Then stored bounty is distributed among conscientious verifiers. So if `Question` is accepted, the bounty will be distributed among verifiers, who voted for acceptance and they, who voted for rejection will lose their bounty.

### 3. Answering Questions

`Question` can be either `Training Question` or `Test Question`. The main purpose of `Training Question` is to teach students about new topics. After answering them, students can see if they are correct or not. They can see explanations to correct and incorrect answers, provided by the Question creator. `Training Questions` can be assigned to students by university or school for homework. They will have a relatively smaller reward for students compared to `Test Questions`. Because there is no proof that students at home had answered `Training Question` themselves, they will be rewarded less.

On the other hand, `Test Questions` are answered in a controlled environment. Students will not be able to see correct answers or explanations and the only feedback for them will be test scores. Because `Test Questions` are answered in universities and there is proof that students have answered `Questions` themselves, they will be rewarded more than during `Training Questions`.

By analyzing the correlation between students' answers to `Training Questions` and `Test Questions`, rewards on `Test Questions` can be adjusted. If a student has a high score on `Training Questions`, but performed poorly on `Test Questions`, that student will be rewarded less, than a student who has the same scores on `Test Questions`, and less in `Training Questions`, but in correlation with his `Test Questions` score. This is done to discourage students from faking `Training Questions`.

### 4. Checking Answers

Answer checking is mainly needed for `Test Questions`. After  `Test Question` is answered, it should be checked by the verifier. Verifier should check:

1. that Student's answer is correct.
2. that Student's credentials are valid.
3. that video, provided by the Testing Facility, doesn't contain any wrongdoing.

The process of checking answers is done in the same way as the process of verifying `Question`, discussed in section 2.

Video can contain how the student was checked for the presence of electronic devices and the process of actual writing.
