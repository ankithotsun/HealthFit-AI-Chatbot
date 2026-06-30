# CHAPTER 19: NLP METHODOLOGY

This chapter details the Natural Language Processing (NLP) methodology implemented in **HealthFit AI**, explaining the mathematical principles and algorithms driving intent classification, entity extraction, and dialog state updates.

## 19.1 Preprocessing Pipeline

The text preprocessing pipeline prepares raw text queries for machine learning classification and keyword matching.

```
Raw Query ---> Spelling Correction (RapidFuzz >= 90%)
                 |
                 v
         [Split Pipeline]
         /              \
        /                \
       v                  v
preprocess_classifier   preprocess_keywords
- Lowercase             - Contraction Expansion
- Strip Punctuation     - Lowercase
- Keep Stopwords        - Strip Punctuation
- No Lemmatizing        - Stopword Removal Preserving Negations
                        - Lemmatization (WordNet Lemmatizer)
                        - Synonym Normalization (Concept Mapping)
```

1. **Fuzzy Spelling Correction**:
   Uses **RapidFuzz** to correct spelling. First, it checks a target vocabulary of fitness terms. If a token is misspelled, it evaluates the Levenshtein distance ratio. Similarity is computed as:
   $$\text{Ratio}(s_1, s_2) = \frac{|s_1| + |s_2| - \text{LevenshteinDistance}(s_1, s_2)}{|s_1| + |s_2|} \times 100$$
   If $\text{Ratio} \ge 90.0\%$, the misspelled token is replaced by the correct term.
2. **Contraction Expansion**:
   Converts conversational shorthand (e.g., *"i'm"*, *"can't"*, *"don't"*) into standard forms (e.g., *"i am"*, *"cannot"*, *"do not"*).
3. **Stopword Filtering**:
   Removes low-information words (e.g., *"the"*, *"is"*, *"a"*). Crucially, negation terms like `not`, `no`, `never` are preserved to maintain sentence sentiment.
4. **WordNet Lemmatizer**:
   Uses the NLTK WordNet lexicon to reduce words to their base form (lemma). For example:
   - *"exercises"* $\rightarrow$ *"exercise"*
   - *"running"* $\rightarrow$ *"run"*
   - *"healthier"* $\rightarrow$ *"healthy"*
5. **Synonym Concept Normalization**:
   To group words with similar meanings, WordNet synsets are used to map synonyms to a set of core fitness concepts:
   - `fat`: *{adipose, overweight, obese, corpulence, flab}*
   - `slim`: *{slender, thin, skinny, lean, fit}*
   - `muscle`: *{muscular, brawn, sinew, strength}*
   - `bulk`: *{bulk, bulking, mass, size, volume}*
   - `gain`: *{gain, increase, grow, add}*
   
   *Collision Protection*: Core words like `mass`, `strength`, and `body` are blacklisted from synonym expansion to prevent incorrect mappings (e.g., *"Body Mass Index"* expanding to *"body bulk index"*, which would trigger the muscle gain intent).

## 19.2 TF-IDF & Logistic Regression

### 1. TF-IDF (Term Frequency - Inverse Document Frequency)
TF-IDF converts preprocessed text patterns into numerical feature vectors.
* **Term Frequency ($TF$)**: Log-scaled term frequency is configured as:
  $$TF(t, d) = 1 + \log(f_{t,d}) \quad \text{if } f_{t,d} > 0 \text{ else } 0$$
  where $f_{t,d}$ is the frequency of term $t$ in document (pattern) $d$.
* **Inverse Document Frequency ($IDF$)**: Measures how common a word is across the dataset:
  $$IDF(t, D) = \log\left(\frac{1 + N}{1 + DF(t)}\right) + 1$$
  where $N$ is the total number of patterns, and $DF(t)$ is the number of patterns containing term $t$.
* **TF-IDF Weight**: The final feature weight is computed as:
  $$TF\text{-}IDF(t, d, D) = TF(t, d) \times IDF(t, D)$$
  Both unigrams and bigrams ($\text{ngram\_range}=(1, 2)$) are vectorized up to a vocabulary cap of $5,000$ features.

### 2. Multi-Class Logistic Regression (Multinomial)
The classification model is a multinomial Logistic Regression trained with inverse regularization strength $C=1.0$ to prevent overconfident outputs on out-of-scope queries.
The probability that a given query vector $\mathbf{x}$ belongs to intent class $k$ is calculated using the Softmax function:
$$P(Y = k \mid \mathbf{x}) = \frac{e^{\mathbf{w}_k^T \mathbf{x} + b_k}}{\sum_{j=1}^{K} e^{\mathbf{w}_j^T \mathbf{x} + b_j}}$$
where $\mathbf{w}_k$ and $b_k$ represent the weight vector and bias term for class $k$, and $K=34$ is the total number of core intent classes.

## 19.3 Hybrid Boosting & Contextual Memory

### 1. Keyword Boosting
To incorporate domain-specific knowledge, a rule-based **Keyword Boosting Map** is applied.
If a query contains a keyword linked to a specific class (e.g., the word *"protein"* in the query is linked to the intent `protein_sources`), that class's raw probability score is boosted:
$$P'(Y = k \mid \mathbf{x}) = P(Y = k \mid \mathbf{x}) + 1.5$$
The boosted probabilities are then re-normalized:
$$P_{\text{boosted}}(Y = k \mid \mathbf{x}) = \frac{P'(Y = k \mid \mathbf{x})}{\sum_{j=1}^{K} P'(Y = j \mid \mathbf{x})}$$
This hybrid architecture ensures the chatbot remains accurate and context-aware even with brief, keyword-heavy user queries.

### 2. Multi-Intent Processing
If the primary intent's confidence is high and a secondary intent's boosted probability satisfies $P_{\text{boosted}}(Y = s \mid \mathbf{x}) \ge 0.38$, both intents are returned. The system then merges the respective templates, separating them with a transition paragraph:
```
[Transition]: "I noticed you are asking about multiple topics! Here is some personalized advice on both:"
```

### 3. Contextual Inheritance (Follow-up Resolution)
If a user submits a follow-up query (e.g., *"why"*, *"explain it"*, *"elaborate"*), the system bypasses standard classification. It queries the `chat_history` table for the active session, retrieves the last successfully classified intent (within the last 3 turns), and inherits it:
$$\text{Intent}_{\text{current}} = \text{Intent}_{\text{previous}} \quad \text{with } \text{Confidence} = 1.0$$
This maintains conversational continuity without requiring complex semantic state models.
