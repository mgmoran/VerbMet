# VerbMet
Automatic Verbal Metaphor Identification 

VerbMet is intended as general resource for the identification and parsing of figurative verb usage. It is based on a specific intuition about verbal metaphor: that it indicates sort of semantic “mismatch” between a verb and (at least) one of its arguments. We know that verbs tend to exhibit selectional preferences for attributes of their arguments - i.e. certain verbs require a +concrete, or a +animate subject or object; when one or more arguments does not meet the verb's selectional preferences, it is likely that the verb is paraticipating in a metaphorical usage.

When an intransitive verb is used metaphorically, we almost always see a subject-verb mismatch:

*Evening fell.*

But we may also see mismatches between verb and adjuncts: 

*We were swimming in cash.*

For transitive verbs, there are more possibilities. There might be a mismatch of subject and verb: 

*The wind whistled.*

Or there might be a mismatch of verb and object: 

*‘Tis the season to spread cheer.*

Or it might be one of any possible adjuncts: 

*She carried me to safety.*

Clearly, the locus of semantic mismatch varies; in fact, we believe that it varies *systematically* depending upon the verb. 

In other words, the intuition is that verbs tend to exhibit selectional preferences not only for the attributes of their arguments, but also for *where a semantic mismatch is most likely to occur*.

VerbMet thus comprises two separate but related goals:
  1) classification of individual verb usage in context as literal or figurative, using annotated data and existing resources 
  on typical verb selectional preferences (VerbNet, FrameNet, WordNet)
  
  2) learning the selectional preferences of individual verbs re: their metaphorical usage.
  
The second goal aids the first in that it reduces the amount of work a machine-learning algorithm needs to do to detect figurative verb usage if we can isolate where the mismatch is most likely to occur. But we believe that understanding the selectional preferences of a given verb with respect to its most likely metaphorical usage has numerous other potentially useful applications. First of all, it may contribute to a more robust verb typology and semantics. We also believe it can improve figurative language generation.

At present, VerbMet is engineered to work on data already tagged with main verbs *and their corresponding arguments*. We use PropBank.

--------

7/18/19

The next iteration of this project involves feature-extraction of verbs in context using BERT.


 

