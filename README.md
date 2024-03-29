This code generates and scores a random hand of cribbage. As a brief refresher of cribbage rules:

-The game involves two phases every hand, commonly known as pegging and scoring. This program only deals with the scoring phase, which is significantly easier to implement and only involves one player's hand

-In a 4 player game, which this program was based on, each hand begins by dealing 5 cards, after which each player must discard one to a new hand known as the crib or kitty which is played by the dealer

-After these cards are discarded, another card is flipped from the top of the deck and can be used for scoring in every player's hand

My main interest was the final point: how a hand is scored after one card is chosen for removal and another is randomly added. Because the card is discarded before the new one is flipped, players must think strategically about how the flipped card may influence their potential points. This program uses a sort of retroactive analysis by looking at what could have been scored if the player had discarded each of the 5 initial cards dealt. I used this to compare my decision making to the actual outcome, to build my strategy for a real game. I then ran a simulation of thousands of hands to see if there were any trends in what cards are most valuable to keep, and found mixed results.

Finally, a refresher on cribbage scoring rules, and how I implemented these:

-Duplicates: Pairs are worth 2 points, 3 of a kind 6, and 4 of a kind 12. By far the easiest to implement, I simply took a count of each value in the hand and returned the appropriate score

-Runs: Consecutive cards of at least length 3 are called runs, and are scored points equal to the length of the run. For example, 3-4-5 is worth 3 points, and 10-J-Q-K is worth 4. Double runs are runs with at least one element repeated, and are scored as two distinct runs: 3-4-4-5 scores 6 points, for example, and 3-4-4-5-5 scores 12 (not counting the points from the pairs or 15s). This one required slightly more work, and I'm curious to explore how I could refine the logic. After converting the face cards back into numerical values (for example, Jack -> 11), I remove all duplicates and sort the hand, then iterate through to check if the sequence is consecutively increasing. If it is, and is greater or equal to length 3, then I check if any of the duplicated elements are in the run, which is used to find a multiplier for the score of the run

-Fifteens: Any combination of cards that adds up to exactly 15 is worth 2 points. Face cards were again converted to numerical values, but in a slightly different way: for the purposes of scoring 15s, all face cards are counted as 10 (aces are worth 1). After doing this, I was able to use a function from itertools to find all possible combinations in the hand that add to 15.

-Flush: If all 4 cards in the hand are the same suit, 4 points are scored. If the flipped card is also the same suit, it is worth an additional point. An important point is that 3 cards in the hand being the same suit as the top card does not count as a flush, so the code could not just simply check if the count of any one suit is equal to 4 or more

-Right Jack: Finally, if a player has a jack in his hand that is the same suit as the top card, 1 point is scored
