% baran deniz korkmaz
% 2015400183
% compiling: yes
% complete: yes

:- [pokemon_data].
:- use_module(library(lists)).

%The find_pokemon_evolution predicate returns the evolved form of a pokemon if possible.
%The predicate takes the MinRequiredLevel value by pokemon_evolution predicate, then it
%checks whether the level of the pokemon is sufficient to get evolved. Then it recursively
%calls for the new form of the pokemon. This procedure occures repetitively until no evolution is possible.
%The final form of the pokemon is the last pokemon passed into recursion. When the recursion stops, the predicate
%returns the EnemyPokemon that is the last Pokemon tried to evolve.
find_pokemon_evolution(PokemonLevel,Pokemon,EvolvedPokemon):-
	(pokemon_evolution(Pokemon,EvolvedPokemonTmp,MinRequiredLevel),
	PokemonLevel>=MinRequiredLevel,
	find_pokemon_evolution(PokemonLevel,EvolvedPokemonTmp,EvolvedPokemon),!);
    EvolvedPokemon=Pokemon.

%The pokemon_level_stats predicate takes the standard values of HP,Att,Def of a pokemon by
%pokemon_stats predicate. Then necessary computations are carried out and the predicate returns
%the values.
pokemon_level_stats(PokemonLevel, Pokemon, PokemonHp, PokemonAttack, PokemonDefense) :- 
	pokemon_stats(Pokemon, _, PokemonHpTmp, PokemonAttackTmp, PokemonDefenseTmp),
	PokemonHp is PokemonHpTmp+(2*PokemonLevel),
	PokemonAttack is PokemonAttackTmp+PokemonLevel,
	PokemonDefense is PokemonDefenseTmp+PokemonLevel.

%The single_type_multiplier predicate is used to find single-type advantage/disadvantage multiplier. The predicate
%uses type_chart_attack predicate for taking a multiplier list when the AttackerType is given or it enables us to
%search for any AttackerType of a given multiplier. Then by pokemon_types predicate, every type is taken in order.
%Finally, the predicate calls for matchFunction where the process continues.
single_type_multiplier(AttackerType,DefenderType,Multiplier) :-
	type_chart_attack(AttackerType,MultiplierList),
	pokemon_types(TypeList),
	matchFunction(TypeList,DefenderType,MultiplierList,Multiplier).

%matchFunction predicate enables us to traverse the TypeList and if the current element is equivalent to the
%DefenderType, it stops and the recursion returns the Multiplier if the AttackerType is given. If the AttackerType
%is given and Multiplier is requested, the matchFunction will check for every AttackerType and will return the 
%corresponding Multiplier value.
matchFunction([DefenderType|_],DefenderType,[Multiplier|_],Multiplier).
matchFunction([HeadType|TypeList],DefenderType,[HeadMultiplier|MultiplierList],Multiplier) :-
	matchFunction(TypeList,DefenderType,MultiplierList,Multiplier).

%type_multiplier predicate is used to find double-type advantage/disadvantage. The predicate takes the DefenderTypes
%in the DefenderTypeList, and calls the single_type_multiplier for each DefenderType. Then the Multiplier value is
%found by multiplication of the returned Multipliers from the single_type_multiplier calls.
type_multiplier(AttackerType,DefenderTypeList,Multiplier) :-
	nth0(0,DefenderTypeList,DefenderType1,_),
	nth0(1,DefenderTypeList,DefenderType2,_),
	single_type_multiplier(AttackerType,DefenderType1,MultiplierTmp1),
	single_type_multiplier(AttackerType,DefenderType2,MultiplierTmp2),
	Multiplier is (MultiplierTmp1*MultiplierTmp2),!.

%pokemon_type_multiplier predicate implements 4 cases in one. The predicate finds the type list of given pokemons
%(both attacker and defender) and then according to their lengths, makes necessary directions.
pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, Multiplier):-
 pokemon_stats(AttackerPokemon,AttackerTypeList,_,_,_),
 pokemon_stats(DefenderPokemon,DefenderTypeList,_,_,_),
 length(AttackerTypeList,AttackerTypeListLength),
 length(DefenderTypeList,DefenderTypeListLength),
 ((AttackerTypeListLength=1,DefenderTypeListLength=1,findMultiplier11(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier));
 	(AttackerTypeListLength=1,DefenderTypeListLength=2,findMultiplier12(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier));
 	(AttackerTypeListLength=2,DefenderTypeListLength=1,findMultiplier21(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier));
 	(AttackerTypeListLength=2,DefenderTypeListLength=2,findMultiplier22(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier))).

%Returns the multiplier if the lengths of AttackerTypeList and DefenderTypeList both are 1. A single_type_multiplier
%would return the multiplier, since both pokemons have only one type.
findMultiplier11(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier):-
	nth0(0,AttackerTypeList,AttackerType,_),
    nth0(0,DefenderTypeList,DefenderType,_),
    single_type_multiplier(AttackerType,DefenderType,Multiplier).

%Returns the multiplier if the length of AttackerTypeList is 1 and the length DefenderTypeList is 2. 
%A type_multiplier would return the multiplier, since the attacker pokemon has one type, and
%the defender pokemon has double-type.
findMultiplier12(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier):-
	nth0(0,AttackerTypeList,AttackerType,_),
 	type_multiplier(AttackerType,DefenderTypeList,Multiplier).

%Returns the multiplier if the length of AttackerTypeList is 2 and the length DefenderTypeList is 1.
%Two single_multiplier would return two multipliers, since the attacker pokemon has double-type, and
%the defender pokemon has one type. The Multiplier value is the maximum of these.
findMultiplier21(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier):-
	nth0(0,AttackerTypeList,AttackerTypeOf1,_),
 	nth0(1,AttackerTypeList,AttackerTypeOf2,_),
 	nth0(0,DefenderTypeList,DefenderType,_),
 	single_type_multiplier(AttackerTypeOf1, DefenderType, Multiplier1),
 	single_type_multiplier(AttackerTypeOf2, DefenderType, Multiplier2),
 	Multiplier is max(Multiplier1,Multiplier2).

%Returns the multiplier if the lengths of AttackerTypeList and DefenderTypeList both are 2.
%Two type_multiplier would return two multipliers, since the attacker pokemon has one type, and
%the defender pokemon has double-type. The Multiplier value is the maximum of these.
findMultiplier22(AttackerPokemon,AttackerTypeList,DefenderPokemon,DefenderTypeList,Multiplier):-
	nth0(0,AttackerTypeList,AttackerTypeOf1,_),
 	nth0(1,AttackerTypeList,AttackerTypeOf2,_),
	type_multiplier(AttackerTypeOf1,DefenderTypeList,Multiplier1),
 	type_multiplier(AttackerTypeOf2,DefenderTypeList,Multiplier2),
 	Multiplier is max(Multiplier1,Multiplier2).

%pokemon_attack predicate returns the damage given by the attacker pokemon into a defender pokemon.
%In order to be able to calculate the Damage value, the attack value of the attacker pokemon and the
%defense value of the defender pokemon in corresponding pokemon levels are returned by 
%pokemon_level_stats predicate. By pokemon_type_multiplier, the Multiplier value has been returned.
%Then the Damage value is calculated according to the formula. 
pokemon_attack(AttackerPokemon,AttackerPokemonLevel,DefenderPokemon,DefenderPokemonLevel,Damage) :-
	pokemon_type_multiplier(AttackerPokemon,DefenderPokemon,Multiplier),
	pokemon_level_stats(AttackerPokemonLevel, AttackerPokemon, AttackerPokemonHp, AttackerPokemonAttack, AttackerPokemonDefense),
    pokemon_level_stats(DefenderPokemonLevel, DefenderPokemon, DefenderPokemonHp, DefenderPokemonAttack, DefenderPokemonDefense),
	Damage is ((0.5 * AttackerPokemonLevel * (AttackerPokemonAttack / DefenderPokemonDefense) * Multiplier) +1),!.
 
%The pokemon_fight predicate simulates a fight between two pokemons with given levels.
%The predicate gets the properties of the pokemon at a given level by pokemon_level_stats predicate.
%Plus, the predicate gets the damage given by both pokemons by pokemon_attack predicate.
%Then, start_fight predicate returns two lists that includes the hp values of both pokemons round by round,
%and another list that holds the round numbers. 
pokemon_fight(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,Pokemon1Hp,Pokemon2Hp,Rounds) :-
	pokemon_attack(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,DamageOf1),
	pokemon_attack(Pokemon2,Pokemon2Level,Pokemon1,Pokemon1Level,DamageOf2),
	pokemon_level_stats(Pokemon1Level,Pokemon1,Pokemon1InitialHp,_,_),
	pokemon_level_stats(Pokemon2Level,Pokemon2,Pokemon2InitialHp,_,_),
	RoundTemp=0,
	start_fight(Pokemon1HpList,Pokemon2HpList,DamageOf1,DamageOf2,Pokemon1InitialHp,Pokemon2InitialHp,RoundList,RoundTemp),
	min_list(Pokemon1HpList, Pokemon1HpMin),
	min_list(Pokemon2HpList,Pokemon2HpMin),
	max_list(RoundList,RoundMax),
	Pokemon1Hp is Pokemon1HpMin,
	Pokemon2Hp is Pokemon2HpMin,
	Rounds is RoundMax.

%start_fight predicate stops when one of the health points decreases below 0.
start_fight([],[],_,_,X,Y,[],_) :- (X<0;Y<0).
	
%At each round the lists are updated accordingly by the following predicate.
start_fight([Head1|Pokemon1HpList],[Head2|Pokemon2HpList],DamageOf1,DamageOf2,Pokemon1TempHp,Pokemon2TempHp,[Head3|RoundList],RoundTemp) :-
	Head1 is Pokemon1TempHp-DamageOf2,
	Head2 is Pokemon2TempHp-DamageOf1,
	Head3 is RoundTemp+1,
	start_fight(Pokemon1HpList,Pokemon2HpList,DamageOf1,DamageOf2,Head1,Head2,RoundList,Head3),!.

%pokemon_tournament predicate takes the pokemons and the levels of the pokemons of each trainer by
%pokemon_trainer predicate. Then dual_arena predicate simulates fight between each pokemon of the trainer.
%The dual_arena predicate returns the WinnerTrainerList.
pokemon_tournament(PokemonTrainer1,PokemonTrainer2,WinnerTrainerList) :-
	pokemon_trainer(PokemonTrainer1,PokemonListTrainer1,PokemonLevelsList1),
	pokemon_trainer(PokemonTrainer2,PokemonListTrainer2,PokemonLevelsList2),
	duel_arena(PokemonTrainer1,PokemonTrainer2,PokemonListTrainer1,PokemonLevelsList1,PokemonListTrainer2,PokemonLevelsList2,WinnerTrainerList),!.

%dual_arena predicate stops when the lists of pokemons and their levels owned by each trainer
%becomes empty. That is every pokemon is processed accordingly.
duel_arena(_,_,[],[],[],[],[]).

%The following predicate first evolves the pokemons and then simulates a fight between each pokemon. Then
%puts the winner Trainer into the WinnerTrainerList accordingly. Then it calls itself. This loop is carried
%out until each list becomes empty, that is each pokemon of the trainer has been fought.
duel_arena(PokemonTrainer1,PokemonTrainer2,[Head1|PokemonListTrainer1],[Head2|PokemonLevelsList1], [Head3|PokemonListTrainer2], [Head4|PokemonLevelsList2], [Head|Tail]) :-
	find_pokemon_evolution(Head2,Head1,EvolvedPokemon1),
	find_pokemon_evolution(Head4,Head3,EvolvedPokemon2),
	pokemon_fight(EvolvedPokemon1,Head2,EvolvedPokemon2,Head4,Pokemon1Hp,Pokemon2Hp,Rounds),
	((Pokemon1Hp>=Pokemon2Hp,Head=PokemonTrainer1,!);(Head=PokemonTrainer2)),
	duel_arena(PokemonTrainer1, PokemonTrainer2, PokemonListTrainer1, PokemonLevelsList1, PokemonListTrainer2,PokemonLevelsList2, Tail).

%The best_pokemon predicate takes the list of all pokemons by findall function.
%Then it calls find_best_pokemon predicate which returns the HP values of each
%attacker pokemon (the pokemon which fights against EnemyPokemon). Then the predicate
%takes the max Hp value and its index. The BestPokemon is at the same index in the
%PokeList.
best_pokemon(EnemyPokemon,LevelCap,RemainingHP,BestPokemon):-
	findall(Pokemon,pokemon_stats(Pokemon,_,_,_,_),PokeList),
	find_best_pokemon(PokeList,EnemyPokemon,LevelCap,CandidateBestPokemonsHpList),
	max_member(RemainingHP,CandidateBestPokemonsHpList),
	nth0(N,CandidateBestPokemonsHpList,RemainingHP,_),
	nth0(N,PokeList,BestPokemon,_).

%find_best_pokemon predicate stops when the PokeList and CandidateBestPokemonsHpList becomes empty.
%That is each pokemon is processed.
find_best_pokemon([],_,_,[]).

%The following predicate takes each pokemon in the PokeList and it puts the remaining Hp of the
%attacker pokemon after a fight against the EnemyPokemon. This procedure goes until every Pokemon is
%processed.
find_best_pokemon([Head1|PokeList],EnemyPokemon,LevelCap,[Head2|CandidateBestPokemonsHpList]) :-
	pokemon_fight(Head1,LevelCap,EnemyPokemon,LevelCap,Head2,_,_),
	find_best_pokemon(PokeList,EnemyPokemon,LevelCap,CandidateBestPokemonsHpList).

%The best_pokemon_team predicate returns the best team against a given Trainer.
%The pokemon_trainer predicate returns the list of pokemon and pokemon levels of the
%opponent trainer. Then by find_best_pokemon_team predicate we return the best team
%against the opponent trainer.
best_pokemon_team(OpponentTrainer,PokemonTeam) :-
	pokemon_trainer(OpponentTrainer,OpponentTrainerPokeList,OpponentTrainerPokeLevelsList),
	find_best_pokemon_team(OpponentTrainerPokeList,OpponentTrainerPokeLevelsList,PokemonTeam).

%The recursion of the find_best_pokemon_team predicate stops when the lists becomes empty, that is
%each pokemon of the opponent trainer has been processed.
find_best_pokemon_team([],[],[]).

%The following predicate evolves the current pokemon of the opponent trainer and finds the best pokemon
%against the final form of the pokemon of the opponent. Then the predicate puts the best pokemon
%against that opponent, and calls the next pokemon of the opponent trainer if exists.
find_best_pokemon_team([Head1|OpponentTrainerPokeList],[Head2|OpponentTrainerPokeLevelsList],[Head3|PokemonTeam]):-
	find_pokemon_evolution(Head2,Head1,Head1Tmp),
	best_pokemon(Head1Tmp,Head2,_,Head3),
	find_best_pokemon_team(OpponentTrainerPokeList,OpponentTrainerPokeLevelsList,PokemonTeam).

%This predicate finds every Pokemon from InitialPokemonList that are at least one of the types from
%TypeList. For every pokemon, if the Pokemon is a member of the InitialPokemonList and pokemon_types_2 predicate returns true,
%the Pokemon will be put into the PokemonList list. 
pokemon_types(TypeList,InitialPokemonList,PokemonList) :-
	findall(Pokemon, (member(Pokemon,InitialPokemonList), pokemon_types_2(TypeList,Pokemon)), PokemonList).

%pokemon_types_2 predicate analyzes for each pokemon if the TypeList contains a member of
%the PokemonTypeList that is returned by the pokemon_stats predicate.
pokemon_types_2([H|TypeListTail], Pokemon) :-
	pokemon_stats(Pokemon, PokemonTypeList,_,_,_),
	((member(H,PokemonTypeList),!); pokemon_types_2(TypeListTail,Pokemon)).


%The generate_pokemon_team predicate checks the Criterion first and returns the list of pokemon_stats
%satisfying the condition that the list will not include any pokemon disliked, and will include the pokemons
%of liked type. Then the predicate sorts according to the first elements of each lists, notice that the lists
%includes the hp,att,or def points according to the criterion. The reason is to enable sort with 4 params. 
%Then the eliminate_first_elem returns the list of lists without the lists including the first element. (Removal
%of the first element that is used for the sort). Then get_pokemon_team predicate allows us to get first count 
%elements.
generate_pokemon_team(LikedTypes,DislikedTypes,Criterion,Count,PokemonTeam) :-
	((Criterion='h',
		findall([PokeHp,PokemonName,PokeHp,PokeAtt,PokeDef],
			(pokemon_stats(PokemonName,PokeTypeList,PokeHp,PokeAtt,PokeDef),
				isMember(PokeTypeList,LikedTypes),notMember(PokeTypeList,DislikedTypes)),PokemonTeamTmp));
		(Criterion='a',
		findall([PokeAtt,PokemonName,PokeHp,PokeAtt,PokeDef],
			(pokemon_stats(PokemonName,PokeTypeList,PokeHp,PokeAtt,PokeDef),
				isMember(PokeTypeList,LikedTypes),notMember(PokeTypeList,DislikedTypes)),PokemonTeamTmp));
		(Criterion='d',
		findall([PokeDef,PokemonName,PokeHp,PokeAtt,PokeDef],
			(pokemon_stats(PokemonName,PokeTypeList,PokeHp,PokeAtt,PokeDef),
				isMember(PokeTypeList,LikedTypes),notMember(PokeTypeList,DislikedTypes)),PokemonTeamTmp))),
	sort(0,@>=,PokemonTeamTmp,SortedList),
	eliminate_first_elem(SortedList,PokemonTeamPrev),
	get_pokemon_team(Count,PokemonTeamPrev,PokemonTeam).
	

%Used to check if the type of the given pokemon is in the liked types.
isMember(PokeTypeList,LikedTypes) :-
    length(PokeTypeList,PokeTypeListLength),
    ((PokeTypeListLength=1,
        nth0(0,PokeTypeList,PokeType),
            member(PokeType,LikedTypes),!);
        (PokeTypeListLength=2,
            nth0(0,PokeTypeList,PokeType1),
            nth0(1,PokeTypeList,PokeType2),
            (member(PokeType1,LikedTypes);member(PokeType2,LikedTypes)))).

%Used to check if the type of the given pokemon is in the liked types.
notMember(PokeTypeList,DislikedTypes) :-
    length(PokeTypeList,PokeTypeListLength),
    ((PokeTypeListLength=1, nth0(0,PokeTypeList,PokeType),
            \+member(PokeType,DislikedTypes),!);
        (PokeTypeListLength=2,
            nth0(0,PokeTypeList,PokeType1),
            nth0(1,PokeTypeList,PokeType2),
            \+member(PokeType1,DislikedTypes),
            \+member(PokeType2,DislikedTypes))).


%get_pokemon_team predicates allows us to get the final for of the pokemon team list.
%The predicates returns the first count elements of the list.
get_pokemon_team(N, _, Xs) :- N =< 0, !, N =:= 0, Xs = [].
get_pokemon_team(_, [], []).
get_pokemon_team(N, [X|Xs], [X|Ys]) :- M is N-1, get_pokemon_team(M, Xs, Ys).

%This predicates allows us to eliminate the first elements of the lists of the list.
eliminate_first_elem([],_).
eliminate_first_elem([[H|T]|PokemonTeamPrev],[T|PokemonTeam]):-
	eliminate_first_elem(PokemonTeamPrev,PokemonTeam).
