# Homework 1 report

Sequence of completed commands:

```bash
# creating 'HW1' branch
git clone https://github.com/screemix/ITMO_ScientificPython_2024
git branch HW1
git checkout HW1

# adding new files with the corresponding texts in the editor
nano hw1.txt
nano test_revert.txt
nano test_revert_merge.txt

# Staging, commiting and pushing updated files to the 'HW1' branch
git add hw1.txt test_revert.txt test_revert_merge.txt 
git commit -m 'added hw1.txt and test_revert/*.txt files'
git push origin -u HW1

# creating 'testing' branch
git branch testing

# modifying hw1.txt file (on the branch 'HW1') through editor
nano hw1.txt

# Staging, commiting and pushing updated hw1.txt file to the 'HW1' branch
git add hw1.txt
git commit -m 'modified hw1.txt'
git push origin -u HW1

# switching to the 'testing' branch
git checkout testing

# modifying test_revert.txt file (on the branch 'testing') through editor
nano test_revert.txt

# Staging, commiting and pushing updated test_revert.txt file to the 'testing' branch
git add test_revert.txt
git commit -m 'modified test_revert.txt'
git push origin -u testing

# switching to the 'HW1' branch and merge it with the 'testing' one
git checkout HW1
git merge testing

# updating HW1 in the origin
git push origin -u HW1

```

Oops! We forgot to add some changes to the 'testing' branch before merging, so we would like to revert the merge:

```bash
# reverting merge to introduce some new changes on the 'testing' branch and merge again
git revert -m 1 HEAD

# introducing changes on the 'testing' branch
git checkout testing
nano test_revert_merge.tx


# staging and commiting 
git add test_revert_merge.txt
git commit -m 'modified test_revert_merge.txt'

# merging with HW1
git checkout HW1
git merge testing 


```

However, after reverting there is a lack of changes in the 'test_revert.txt' on 'HW1' branch. It happened in this way as during the second merge git try to determine closest common ancestor. And, as the first merge still in the git's history tree, the closest common ancestor would be the commit ```ee04c4408deb5b36ea3baea2a6e61f290c1bf236``` (```modified test_revert_merge.txt```):

```bash
* commit 4f0dbb48b7f1eba3e0c9b71c274bfb62932f143a
| Author: screemix <chepurova@bk.ru>
| Date:   Mon Mar 4 13:23:23 2024 +0300
| 
|     Revert "Revert "Merge branch 'testing' into HW-1""
|     
|     This reverts commit 0cd05bcd195b1175311539611d10da935fb29ee2.
|   
*   commit bcc6e7a65702670dcc3704a32fd23bb910e0e659
|\  Merge: 0cd05bc ee04c44
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:18:27 2024 +0300
| | 
| |     Merge branch 'testing' into HW1 with changes in test_revert_merge.txt file
| | 
| * commit ee04c4408deb5b36ea3baea2a6e61f290c1bf236 (testing)
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:18:12 2024 +0300
| | 
| |     modified test_revert_merge.txt
| | 
* | commit 0cd05bcd195b1175311539611d10da935fb29ee2
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:15:55 2024 +0300
| | 
| |     Revert "Merge branch 'testing' into HW0"
| |     
| |     This reverts commit 04d281508f01a57429dee4a668892ef71cfccc1f, reversing
| |     changes made to afcf95285df1c0bf881238c5859303a7b9a5d49b.
| | 
* | commit 04d281508f01a57429dee4a668892ef71cfccc1f
|\| Merge: afcf952 cbbb9fb
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:13:44 2024 +0300
| | 
| |     Merge branch 'testing' into HW1
| | 
| * commit cbbb9fb0cb4851748a03dfe79fc561c8faaba06a (origin/testing)
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:12:54 2024 +0300
| | 
| |     modified test_revert.txt
| | 
* | commit afcf95285df1c0bf881238c5859303a7b9a5d49b
|/  Author: screemix <chepurova@bk.ru>
|   Date:   Mon Mar 4 13:11:37 2024 +0300
|   
|       modified hw1.txt

```

Therefore, to merge 'HW1' and 'testing' branch git calculate diff between commits ```ee04c4408deb5b36ea3baea2a6e61f290c1bf236``` and ```0cd05bcd195b1175311539611d10da935fb29ee2```. Then, git creates the merge commits with those two ancestors, not including ```cbbb9fb0cb4851748a03dfe79fc561c8faaba06a``` (```modified test_revert.txt```) as it was already in the history tree of 'HW1' branch. 

To restore lost changes in ```test_revert.txt```, we can perform reverting the reverting commit:

```bash
# reverting commit "Revert "Merge branch 'testing' into HW0"
git revert 0cd05bcd195b1175311539611d10da935fb29ee2
```

Now the tree looks like this:

```bash=
* commit 4f0dbb48b7f1eba3e0c9b71c274bfb62932f143a (HEAD -> HW1)
| Author: screemix <chepurova@bk.ru>
| Date:   Mon Mar 4 13:23:23 2024 +0300
| 
|     Revert "Revert "Merge branch 'testing' into HW-1""
|     
|     This reverts commit 0cd05bcd195b1175311539611d10da935fb29ee2.
|   
*   commit bcc6e7a65702670dcc3704a32fd23bb910e0e659
|\  Merge: 0cd05bc ee04c44
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:18:27 2024 +0300
| | 
| |     Merge branch 'testing' into HW1 with changes in test_revert_merge.txt file
| | 
| * commit ee04c4408deb5b36ea3baea2a6e61f290c1bf236 (testing)
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:18:12 2024 +0300
| | 
| |     modified test_revert_merge.txt
| | 
* | commit 0cd05bcd195b1175311539611d10da935fb29ee2
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:15:55 2024 +0300
| | 
| |     Revert "Merge branch 'testing' into HW0"
| |     
| |     This reverts commit 04d281508f01a57429dee4a668892ef71cfccc1f, reversing
| |     changes made to afcf95285df1c0bf881238c5859303a7b9a5d49b.
| | 
* | commit 04d281508f01a57429dee4a668892ef71cfccc1f (origin/HW1)
|\| Merge: afcf952 cbbb9fb
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:13:44 2024 +0300
| | 
| |     Merge branch 'testing' into HW1
| | 
| * commit cbbb9fb0cb4851748a03dfe79fc561c8faaba06a (origin/testing)
| | Author: screemix <chepurova@bk.ru>
| | Date:   Mon Mar 4 13:12:54 2024 +0300
| | 
| |     modified test_revert.txt
| | 
* | commit afcf95285df1c0bf881238c5859303a7b9a5d49b
|/  Author: screemix <chepurova@bk.ru>
|   Date:   Mon Mar 4 13:11:37 2024 +0300
|   
|       modified hw1.txt
| 
* commit 4033eb47692f3260e9abaeeda1432c5ba0ce3552
| Author: screemix <chepurova@bk.ru>
| Date:   Mon Mar 4 13:08:52 2024 +0300
| 
|     added hw1.txt and test_revert/*.txt files
| 
* commit 723b8d4c6f63cc2a6cc3773a73015eeefd28bded (origin/main, origin/HEAD, main)
  Author: Chepurova Alla <43718473+screemix@users.noreply.github.com>
  Date:   Mon Mar 4 13:05:05 2024 +0300

```

Hooray! Now we have all the changes in the 'HW1' branch as we reverted the reverting - in this wey we preserved the changes in ```test_revert.txt``` made during the first merge in the tree and changes in ```test_revert_merge.txt``` made during the second merge.


Final steps:

```bash
# pushing changes to the remote
git push origin -u HW1

# I forgot to put the files in the HW1 directory, so I've done it after the tasks
mkdir HW1
mv *.txt HW1
git add .
git commit -m 'moved *.txt files to the HW1 dir'
git push origin -u HW1

```

Then, I deleted 'testing' branch and created pull request from 'HW1' to the 'main' branch.

## Alternative way
I also tried to perform cherry-picking the lost commit after the second merge. Example sequence of steps:

```bash=
# creating a new branch from 'HW1' with the lost changes
git branch HW1-fix
git checkout HW1-fix

# adding needed changes from 'modified test_revert.txt' commit
git cherry-pick cbbb9fb0cb4851748a03dfe79fc561c8faaba06a

# merging HW1 and HW1-fix
git checkout HW1
git merge HW1-fix

```
Hooray, all the needed changes persist in the 'HW1' branch!