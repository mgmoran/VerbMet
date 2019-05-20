# VerbMet
Automatic Verbal Metaphor Identification 

VerbMet is intended to be a general resource for the identification and parsing of figurative verb usage. It is based on a specific intuition about verbal metaphor: that it indicates sort of semantic “mismatch” between a verb and (at least) one of its arguments. We know that verbs tend to exhibit selectional preferences for attributes of their arguments - i.e. certain verbs require a +concrete, or a +animate subject or object; when one or more arguments does not meet the verb's selectional preferences, it is likely that the verb is paraticipating in a metaphorical usage.

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

Clearly the locus of semantic mismatch varies; in fact, we believe that it varies *systematically* depending upon the verb. 

In other words, our intuition is that verbs tend to exhibit selectional preferences not only for the attributes of their arguments, but also for *where a semantic mismatch is most likely to occur* if it is used metaphorically. 

VerbMet is thus a two-step project: 
  1) to use existing resources on verb behavior and selectional preferences (VerbNet, PropBank, WordNet) to improve the
  automatic identification of a particular verb usage as figurative or literal, and
  
  2) to gather enough data of the literal and figurative usages of particular verbs to predict what kind of argument
  mismatch a verb selects for.
  
 
We believe that understanding the selectional-preferences of a given verb with respect to its most likely metaphorical usage will contribute to a more robust verb typology and semantics. Furthermore, we may be able to reduce the amount of work a machine-learning algorithm needs to do to detect figurative verb usage if we can isolate where the mismatch is most likely to occur.
