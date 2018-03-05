LDA (Litent Dirichlet Allocation):
LDA looks at each document as a bag of words, and performs 'Random gibbs sampling' to assign each word to a topic. After several iterations, it outputs a document-topic distribution that gives the probability distribution of all topics in each document. It also outputs a topic distribution containing the probability distribution of the words present in each topic.
Disadvantages:
1. Have to know number of topics in prior.
2. In LDA, the algorithm works separately on each document, while you want the algorithm to carry forward the work it has done on the previous documents to the next.

HDP (Hierarchical Dirichlet Process):
HDP uses a dirichlet process to perform the clustering problem. It hierarchically solves the problem in order to find the optimal number of topics for the data. It forms a hierarchy tree of topics internally. The root of this tree composes of a topic which contains the most generic words used across the data. The tree branches out at every step to give more and more specific topics. This branching basically continues till you reach a level where all the topics in that level are as specific as possible without being too specific, thereby also giving us the best number of topics. The number of leaves of this tree is the optimal number of topics. And the leaves are the topics we should be looking at. Similar to LDA, HDP provides with a document-topic distribution as well as the topic distribution.
Advantages:
1. No need of knowing the number of topics in prior. Also,
2. Carry forwards work, and thus usually performs better than LDA.


Duplication Removal:
Original input data is in the Timewise folder. As each .csv file had duplicates in the, duplication removal was performed on the data.
1. Aparna/check_duplicates.py : To remove duplicates. Also to check which are the duplicate IDs in input paper ids files and csv files.
The new timewise data with all duplicates removed is in the Removed_duplicates_timewise folder.


Re-run LDA:
1. code/create_lda_files.py : Creates .dat and vocab files for all years, needed to run LDA. Input: Removed_duplicates_timewise, Output: code/DataFiles_full
2. Running LDA (command) in code/lda-c : ./lda est 0.1 [topic_no] settings.txt [path_to_dat_file] random [output_path+file_to_save_in]
(Output currently saved in code/lda-c/Removed_duplicates_results)
3. ResearchFall16/Topic-modeling-analysis/create_doc_id.py : Creates '_docID.txt' files containing the paper IDs. Input: Removed_duplicates_timewise, Output: ResearchFall16/Aparna_Final_Results/Paper_IDs
4. ResearchFall16/Topic-modeling-analysis/docs.py : To output document-topic distribution from LDA (Output currently in Aparna_Final_Results/Golden)
5. ResearchFall16/Topic-modeling-analysis/topic.py : To output topic distribution from LDA ((Output currently in Aparna_Final_Results/Golden)

Running LDA pipeline : 1 -> 2 for all years for all topic numbers -> 3 for all years -> 4 and 5, for all years for all topic numbers


Analyze optimal no. for LDA:
Idea is that an optimal topic number will give a document-topic distribution such that a document will predominantly be composed of one topic. (Explain further)
final.gamma file contains the information for document-topic distribution.
code/lda-c/Removed_duplicates_results/find_optimal_lda.py : First converts the gamma file to probability. One option is - for each document, check the topic with highest probability. Then perform average over the differences of the highest topic with all other topics. Perform average over all documents. This basically gives an average of how dominantly a topic is present in a document. Higher the score the better.
The second option is to perform standard deviation over the values for a topic and then average it out over all documents. This sismilarly aims to evaluate the same idea. Higher the score the better.
The other options to perform maximum likelihood or perplexity score requires the lda model to be tested after training, which is not done in thi sproject. Each year is trained separately and thus these scores can't be used. Instead, checking intuitively this way is the chosen method.


Backlinking HDP:
1. HPC_data/code/hdp/hdp-faster/main.cpp : Modified file to output '.doc.states' file which contains the doc-topic distribution information.
2. HPC_data/code/hdp/hdp-faster/print_doc_distribution.py : To output document-topic distribution from HDP (Output currently in HPC_data/code/hdp/hdp-faster/Aparna_Results)
Algo:
3. HPC_data/code/hdp/hdp-faster/print_topics.py : To output topic distribution from HDP (Output currently in HPC_data/code/hdp/hdp-faster/Aparna_Results)
Algo:


Re-run HDP:
1. Running HDP (command) in HPC_data/code/hdp/hdp-faster : ./hdp --train_data [path_to_dat_file] --directory [path_to_output_directory]
(Output currently in HPC_data/code/hdp/hdp-faster/Aparna_Results)
2. HPC_data/code/hdp/hdp-faster/print_doc_distribution.py : To output document-topic distribution from HDP (Output currently in HPC_data/code/hdp/hdp-faster/Aparna_Results)
3. HPC_data/code/hdp/hdp-faster/print_topics.py : To output topic distribution from HDP (Output currently in HPC_data/code/hdp/hdp-faster/Aparna_Results)
