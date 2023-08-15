# SpaceTraders

## Next steps

Here are my next priorities, in no particular order:
- Decouple our tests from our domain (see Chapter 5 of Cosmic Python) to allow future refactoring of our domain without too much impact on tests: the last entity our tests are still coupled to is the Waypoint. We introduced the System entity that should help us decouple it. We can now add a factory method returning an InMemorySystemRepository, and a method that adds a waypoint to a system, similar to what was done for the contracts.
- Let's keep going forward in the tutorial, adding the buying of a ship, mining of the ore, etc.

## General presentation of the repository

This repository contains the code I’ll use to try out [SpaceTraders.io](https://spacetraders.io/).
Having read [the excellent Cosmic Python book](https://www.cosmicpython.com/) recently, my plan is to use this game as a testing ground for the principles of the book.
This is also a very good opportunity to try to apply a minimal approach: only code up the minimal amount of stuff to do what I need to do.
This should allow me to move more swiftly and avoid premature optimisation, which is something I tend to do too much.

I’ll use Python exclusively.

## Contributing, PRs, licences, etc.

As this is a learning project for me, I’ll focus on coding everything here myself and won’t accept PR.
You are welcome to copy and use my code for whatever purpose you want.

## CI

I don't have a proper, automated CI (yet), but I do have the repo setup in a way that lets me run the following commands easily and often:
- `mypy --strict .`
- `ruff .`
- `pytest tests/unit`
- `pytest -s tests/integration`
