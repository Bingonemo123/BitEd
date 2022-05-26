# Vision :eyes:

## This File contains our  vision for Final Product. If you have any questions, please pull request in this file or contact us

Process of testifying student knowledge can be divided into four parts:

1. Creation of Questions
2. Verification of Questions
3. Answering Questions
4. Checking of Questions

First of all, we need to define what exactly questions are questions.
`Question` is a multiple choice question, created by a teacher, lecture, professional or just Knowledgeable person. Creator of `Question` knows the answer to the question in advance. Creator also develops wrong answers to multiple choice questions. Collection of statement of question, correct answer and wrong answers is called `Question`.

### 1. Creation of Questions

In ideal system, everybody can create questions. It would be done through a website or a mobile application. `Question` would be uploaded on Blockchain and would wait for verification. It would be in interest of Question creator:

1. that `Question` be not too easy to answer.
2. that `Question` be properly stated and understandable.  
3. that `Question` be distinct from already existing `Questions`.
4. that `Question` be tagged correctly.
5. and most importantly that `Question's` answer set as correct by question creator, truly be correct.  

If `Question` doesn't satisfy  2, 3 and 5, it would be accepted in verification process and wouldn't be implemented into Blockchain.

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

After Question is submitted, it should be verified by community. To encourage community to verify questions, we would aks Question creators to check 5 someone else `Questions` for every his own submitted `Question`. Also, we would ask Question creators to stake some amount of `Tokens` to back  `Question`. If `Question` that Question creator submitted doesn't satisfy verification criteria, it would be rejected and Question creator will lose the stake, process known as slashing. This is done to discourage people from overflowing Pool of `Questions` that are not yet verified with dummy `Questions`.

By the time of verification, verifier should check:

1. If `Question` is correct.
2. If `Question` is not too easy.
3. If `Question` is distinct from already existing `Questions`.
4. If `Question` is tagged correctly.
5. If `Question` be properly stated and understandable.

If `Question` doesn't satisfy one of these criteria, verifier should report problem. If `Question` doesn't satisfy 3 criteria, verifier should indicate to original `Question`.If `Question` doesn't satisfy 4 criteria, verifier should indicate new corrected tagging. By correcting tagging, verifier creates new `Question`, where author of original `Question` is referenced as coauthor. Correcting tagging can increase the chance of `Question` being accepted. Verification of new `Question` with corrected tagging and original `Question` is done independently. So that `Question` with updated tagging may be rejected, while original `Question` is accepted and author of original `Question` not losing any of stakes.

Editing of `Question` by verifier is done in same way, as correcting tagging. By editing `Question` verifier creates new `Question`, where original author is also referenced. For the reason that editors are creating new `Questions` , they also should back edited `Questions` with `Tokens`.

After `Question` is accepted and process of answering `Questions` is started, `Question` is still in verification stage. Post-acceptance verification of `Question` is done in same way as pre-acceptance verification of `Question`, but students can report problem with `Question` during answering.
Post-acceptance verification is permanent process and is done until `Question` exists on Blockchain.

#### Rejection vs Acceptance
