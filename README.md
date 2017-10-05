# QA-System
Implemented a QA System.  This is the code for the NLPCC-ICCPOL shared task "Open Domain Question Answering."

The tasks comprises two parts: `kbqa` and `dbqa`, the former is to implement a QA system given a Knowledge Base, while the latter requires to select the sentences as answers from the question's given document.

For the `dbqa` task, we encode the question with a LSTM layer and the answer with another LSTM layer, then calculate the angle between these two vectors. If the answer and the question are paired, we hope these two vectors are of the same direction, otherwise let them be perpendicular to each other. Finally, for a new pair of question and answer, classify them based on the angle of their hidden representation.  We use `Keras` with `Theano` backend to run LSTM.

For the `kbqa` task, we used baseline program to identify all mentions in the corpus, then use some hand-crafted rules to identify entities in a given question. After this, we use `mention2id.py` to find all possible ids of the current mention. Finally, calculate the similarity between current problem and all possible ids and attributes of these ids to give the most probable answer. For the similarity between two string, two different methods are averaged: word vector and edit distance.

It turns out that our algorithm's performance on the `dbqa` task is poor, achieved an MRR of 0.295793 only. But for the `kbqa` task, an F1-score of 0.5362 is achieved, which is well enough.

The poor performance for `dbqa` might be due to our lacking experience in parameter tuning for LSTM. In our experiments, sometimes the loss goes to Nan and this might be implying a too large learning rate or improper optimizer. The performance is likely to be much better if we've trained LSTM well.

=============== Update =================

Uploaded file `nlpcc-iccpol-2016.kbqa.kb.mention2id` to [here](https://pan.baidu.com/s/1kUI1OHL).
