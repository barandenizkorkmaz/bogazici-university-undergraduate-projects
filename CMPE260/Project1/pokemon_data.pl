
% pokemon_stats(Pokemon, Types, HealthPoint, Attack, Defense).
pokemon_stats(bulbasaur, [grass, poison], 45, 49, 49).
pokemon_stats(ivysaur, [grass, poison], 60, 62, 63).
pokemon_stats(venusaur, [grass, poison], 80, 100, 123).
pokemon_stats(charmander, [fire], 39, 52, 43).
pokemon_stats(charmeleon, [fire], 58, 64, 58).
pokemon_stats(charizard, [fire, flying], 78, 104, 78).
pokemon_stats(squirtle, [water], 44, 48, 65).
pokemon_stats(wartortle, [water], 59, 63, 80).
pokemon_stats(blastoise, [water], 79, 103, 120).
pokemon_stats(caterpie, [bug], 45, 30, 35).
pokemon_stats(metapod, [bug], 50, 20, 55).
pokemon_stats(butterfree, [bug, flying], 60, 45, 50).
pokemon_stats(pidgey, [normal, flying], 40, 45, 40).
pokemon_stats(pidgeotto, [normal, flying], 63, 60, 55).
pokemon_stats(pidgeot, [normal, flying], 83, 80, 80).
pokemon_stats(ekans, [poison], 35, 60, 44).
pokemon_stats(arbok, [poison], 60, 95, 69).
pokemon_stats(pikachu, [electric], 35, 55, 40).
pokemon_stats(raichu, [electric], 60, 85, 50).
pokemon_stats(vulpix, [fire, ice], 38, 41, 40).
pokemon_stats(ninetales, [fire, ice], 73, 67, 75).
pokemon_stats(jigglypuff, [normal, fairy], 115, 45, 20).
pokemon_stats(wigglytuff, [normal, fairy], 140, 70, 45).
pokemon_stats(zubat, [poison, flying], 40, 45, 35).
pokemon_stats(golbat, [poison, flying], 75, 80, 70).
pokemon_stats(meowth, [normal, dark], 40, 35, 35).
pokemon_stats(persian, [normal, dark], 65, 60, 60).
pokemon_stats(psyduck, [water], 50, 52, 48).
pokemon_stats(golduck, [water], 80, 82, 78).
pokemon_stats(abra, [psychic], 25, 20, 15).
pokemon_stats(kadabra, [psychic], 40, 35, 30).
pokemon_stats(alakazam, [psychic], 55, 50, 65).
pokemon_stats(machop, [fighting], 70, 80, 50).
pokemon_stats(machoke, [fighting], 80, 100, 70).
pokemon_stats(machamp, [fighting], 90, 130, 80).
pokemon_stats(geodude, [rock, ground], 40, 80, 100).
pokemon_stats(graveler, [rock, ground], 55, 95, 115).
pokemon_stats(golem, [rock, ground], 80, 120, 130).
pokemon_stats(grimer, [poison], 80, 80, 50).
pokemon_stats(muk, [poison], 105, 105, 75).
pokemon_stats(shellder, [water], 30, 65, 100).
pokemon_stats(cloyster, [water, ice], 50, 95, 180).
pokemon_stats(gastly, [ghost, poison], 30, 35, 30).
pokemon_stats(haunter, [ghost, poison], 45, 50, 45).
pokemon_stats(gengar, [ghost, poison], 60, 65, 80).
pokemon_stats(onix, [rock, ground], 35, 45, 160).
pokemon_stats(drowzee, [psychic], 60, 48, 45).
pokemon_stats(hypno, [psychic], 85, 73, 70).
pokemon_stats(exeggcute, [grass, psychic], 60, 40, 80).
pokemon_stats(exeggutor, [grass, psychic], 95, 105, 85).
pokemon_stats(lickitung, [normal], 90, 55, 75).
pokemon_stats(koffing, [poison], 40, 65, 95).
pokemon_stats(weezing, [poison], 65, 90, 120).
pokemon_stats(horsea, [water], 30, 40, 70).
pokemon_stats(seadra, [water], 55, 65, 95).
pokemon_stats(staryu, [water], 30, 45, 55).
pokemon_stats(starmie, [water, psychic], 60, 75, 85).
pokemon_stats(magmar, [fire], 65, 95, 57).
pokemon_stats(magikarp, [water], 20, 10, 55).
pokemon_stats(gyarados, [water, flying], 95, 155, 109).
pokemon_stats(lapras, [water, ice], 130, 85, 80).
pokemon_stats(eevee, [normal], 55, 55, 50).
pokemon_stats(articuno, [ice, flying], 90, 85, 100).
pokemon_stats(zapdos, [electric, flying], 90, 90, 85).
pokemon_stats(moltres, [fire, flying], 90, 100, 90).
pokemon_stats(dratini, [dragon], 41, 64, 45).
pokemon_stats(dragonair, [dragon], 61, 84, 65).
pokemon_stats(dragonite, [dragon, flying], 91, 134, 95).
pokemon_stats(mewtwo, [psychic], 106, 150, 70).
pokemon_stats(mew, [psychic], 100, 100, 100).


% pokemon_evolution(Pokemon, EvolvedPokemon, MinRequiredLevel).
pokemon_evolution(bulbasaur, ivysaur, 16).
pokemon_evolution(ivysaur, venusaur, 32).
pokemon_evolution(charmander, charmeleon, 16).
pokemon_evolution(charmeleon, charizard, 36).
pokemon_evolution(squirtle, wartortle, 16).
pokemon_evolution(wartortle, blastoise, 36).
pokemon_evolution(caterpie, metapod, 7).
pokemon_evolution(metapod, butterfree, 10).
pokemon_evolution(pidgey, pidgeotto, 18).
pokemon_evolution(pidgeotto, pidgeot, 36).
pokemon_evolution(ekans, arbok, 22).
pokemon_evolution(zubat, golbat, 22).
pokemon_evolution(meowth, persian, 28).
pokemon_evolution(psyduck, golduck, 33).
pokemon_evolution(abra, kadabra, 16).
pokemon_evolution(machop, machoke, 28).
pokemon_evolution(geodude, graveler, 25).
pokemon_evolution(grimer, muk, 38).
pokemon_evolution(gastly, haunter, 25).
pokemon_evolution(drowzee, hypno, 26).
pokemon_evolution(koffing, weezing, 35).
pokemon_evolution(horsea, seadra, 32).
pokemon_evolution(magikarp, gyarados, 20).
pokemon_evolution(dratini, dragonair, 30).
pokemon_evolution(dragonair, dragonite, 55).



% pokemon_types(PokemonTypes).
pokemon_types([normal, fire, water, electric, grass, ice, fighting, poison, ground, flying, psychic, bug, rock, ghost, dragon, dark, steel, fairy]).

% type_chart_attack(AttackingType, TypeMultipliers).
type_chart_attack(normal, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 1.0, 1.0, 0.5, 1.0]).
type_chart_attack(fire, [1.0, 0.5, 0.5, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 1.0, 2.0, 1.0]).
type_chart_attack(water, [1.0, 2.0, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0]).
type_chart_attack(electric, [1.0, 1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0]).
type_chart_attack(grass, [1.0, 0.5, 2.0, 1.0, 0.5, 1.0, 1.0, 0.5, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 0.5, 1.0, 0.5, 1.0]).
type_chart_attack(ice, [1.0, 0.5, 0.5, 1.0, 2.0, 0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0]).
type_chart_attack(fighting, [2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 2.0, 0.0, 1.0, 2.0, 2.0, 0.5]).
type_chart_attack(poison, [1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 0.0, 2.0]).
type_chart_attack(ground, [1.0, 2.0, 1.0, 2.0, 0.5, 1.0, 1.0, 2.0, 1.0, 0.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0]).
type_chart_attack(flying, [1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0]).
type_chart_attack(psychic, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.5, 1.0]).
type_chart_attack(bug, [1.0, 0.5, 1.0, 1.0, 2.0, 1.0, 0.5, 0.5, 1.0, 0.5, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0, 0.5, 0.5]).
type_chart_attack(rock, [1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0]).
type_chart_attack(ghost, [0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 1.0]).
type_chart_attack(dragon, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 0.0]).
type_chart_attack(dark, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5]).
type_chart_attack(steel, [1.0, 0.5, 0.5, 0.5, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0]).
type_chart_attack(fairy, [1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 0.5, 1.0]).


% pokemon_trainer(PokemonTrainer, PokemonTeam, PokemonLevels
pokemon_trainer(ash, [pikachu, ivysaur, charmeleon, squirtle], [45, 15, 28, 50]).
pokemon_trainer(misty, [psyduck, staryu, starmie, seadra], [10, 15, 48, 45]).
pokemon_trainer(brock, [onix, geodude, golbat, machop], [18, 33, 42, 33]).
pokemon_trainer(team_rocket, [meowth, ekans, gyarados, weezing], [15, 30, 29, 35]).