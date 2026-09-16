---
type: concept
updated: 2026-09-16
status: stable
sources: [CLAUDE.md, ETAT.md]
---

# Les deux ordres

**Il y a deux séquences dans ce projet et elles vont en sens contraire. Les
confondre est l'erreur la plus fréquente d'une session qui arrive froide.**

## Ce que ça veut dire ici

**L'ordre d'exécution** — ce que fait la chaîne une fois construite, étapes 00
à 10 : triage des données → extraction → codage du signal → contrôles → rapport
d'IC → régimes → taxonomie → présélection de combinaisons → arbitrage →
stratégie → backtest.

**L'ordre de construction** — dans quel ordre on fabrique ces étapes :
**l'inverse**. L'évaluation avant la production. Le juge avant l'accusé. C'est
l'ordre que suit `ETAT.md`, phases 01 à 15.

Autrement dit : **l'étape 04 de l'exécution (le rapport d'IC) se construit en
phase 03**, bien avant **l'étape 02 (le codage du signal), qui se construit en
phase 08**.

## Le test qui tranche

> Si tu te retrouves à écrire un signal alors que `ETAT.md` annonce la phase 03,
> tu as confondu les deux ordres — **arrête-toi**.

## Ce que ça ne veut pas dire

- « Phase 03 » et « étape 03 » ne désignent pas la même chose et ne se
  correspondent pas. Quand un document dit « phase », il parle de construction ;
  quand il dit « étape », d'exécution. Le wiki suit la même convention.
- L'ordre de construction n'est pas une préférence méthodologique : c'est ce qui
  rend l'invariant I applicable (*le LLM propose, le code déterministe tranche*).
  Un juge écrit après l'accusé est un juge qu'on a ajusté.

## Où c'est fixé

`CLAUDE.md` § Les deux ordres · `ETAT.md`

## Voir aussi

[[concepts/porte]] · [[phases/phase-03-harnais-ic]] · [[hot]]
