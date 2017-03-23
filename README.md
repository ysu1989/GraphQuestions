## GraphQuestions: A Characteristic-rich Question Answering Dataset
GraphQuestions is a characteristic-rich dataset for factoid question answering described in the paper "[On Generating Characteristic-rich Question Sets for QA Evaluation](http://cs.ucsb.edu/~ysu/papers/emnlp16_graphquestions.pdf)" - EMNLP'16.

### Introduction

Natural language question answering (QA), i.e., finding direct answers for natural language questions, is undergoing active development. Questions in real life often present rich _characteristics_, constituting dimensions along which question difficulty varies. The aim of this project is to explore how to construct characteristic-rich QA dataset in a systematic way, and provide the community with a dataset with rich and explicitly specified question characteristics. A dataset like this enables fine-grained evaluation of QA systems, i.e., developers can know exactly on what kind of questions their systems are failing, and improve accordingly.

We present GraphQuestions, a QA dataset consisting of a set of _factoid questions with logical forms and ground-truth answers_. The current release (v1.0) of the dataset contains 5,166 questions, which are constructed based on Freebase, a large-scale knowledge base. An array of question characteristics are formalized, and every question has an explict specification of characteristics:

* **Structure Complexity**: the number of relations involved in a question
* **Function**: Addtional functions like counting or superlatives, e.g., "_How many children of Ned Stark were born in Winterfell?_"
* **Commonness**: How common a question is, e.g., "_where was Obama born?_" is more common than "_what is the tilt of axis of Polestar?_"
* **Paraphrasing**: Different natural language expressions of the same question
* **Answer Cardinality**: The number of answers to a question

### Example

Here are some example questions and their characteristics (refer to the [paper](http://cs.ucsb.edu/~ysu/papers/emnlp16_graphquestions.pdf) and the [appendix](http://cs.ucsb.edu/~ysu/papers/emnlp16_graphquestions_appendix.pdf) for the definition and distribution of question characteristics). Topic entities are bold-faced. Note how the topic entities and the whole questions are paraphrased:

| Question | Domain | Answer | # of Relations | Function | Commonness | # of Answers |
| --------------------- | :-------: | :-------: | :-: | :------: | :----: | :-: |
| - Find terrorist organizations involved in **September 11 attacks**. <br> - Who did **September 11 attacks**?  <br> - The **nine eleven** were carried out with the involvement of what terrorist organizations? | Terrorism | alQaeda | 1 | none | -16.67 | 1 |
| - For **Eddard Stark**'s children, how many of them were born in **Winterfell**? <br> - In **Winterfell**, how many children of **Eddard Stark** were born?  <br> - How many children of **Ned Stark** were born in **Winterfell**?  | Fictional Universe | 3 | 2 | count | -23.34 | 1 |
| - In which month does the average rainfall of **New York City** exceed **86** mm? <br> - Rainfall averages more than **86** mm in **New York City** during which months?  <br> - List the calendar months when **NYC** averages in excess of **86** millimeters of rain?  | Travel | March, August <br> ... | 3 | comparative | -37.84 | 7 |

### Reference

Please refer to the following paper for more details about the dataset. If you use this dataset in your work, please cite:

```
@InProceedings {su2016graphquestions,
    author    = "Su, Yu and Sun, Huan and Sadler, Brian and Srivatsa, Mudhakar and G{\" u}r, Izzeddin and Yan, Zenghui and Yan, Xifeng",
    title     = "On Generating Characteristic-rich Question Sets for {QA} Evaluation",
    booktitle = "Empirical Methods in Natural Language Processing (EMNLP)",
    year      = "2016",
    address   = "Austin, Texas, USA",
    month     = "nov",
    publisher = "Association for Computational Linguistics"
}
```

### Usage

The dataset works the best when the knowledge backend of a QA system is Freebase, because the provided answers are from Freebase. Nevertheless, it can still serve as a useful resource to QA systems based on other knowledge backend like DBpedia or the Web. Also, the dataset can be used to study or learn question paraphrasing.

To set up a database to store and query Freebase, we refer users to the [FastRDFStore](https://github.com/Microsoft/FastRDFStore/) project or the [Sempre](https://github.com/percyliang/sempre) project.

Use the standard training/testing split if you would like to compare with other methods.

### Evaluation

We provide a standard evaluation script which will evaluate the overall performance based on your result file as well as the breakdown performance by question characteristics. Once you get your result file correctly formatted (refer to provided example result files for formatting), you can easily run the evaluation script, e.g.,

```
python evaluate.py ./freebase13/results/sempre.res
```
