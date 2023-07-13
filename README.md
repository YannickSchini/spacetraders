# SpaceTraders

## Next steps

Here are my next priorities, in no particular order:
- The code is also quite silent so far, without any logging. I should add some basic logging at least.
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

## Structure of the repository

### Exploration folder

This folder will contain tutorial results and other temporary scripts. Basically this’ll be used as a training ground/API Exploration ground, before going on with a cleaner implementation.

## Code Structure and other thoughts

Seeing how there are weekly server resets, and that they require to re-create agents, I guess I'll include them in my "domain model". I was on the fence about it, but seeing how registering new agents will be a regular task, I might as well code it up nicely instead of relying on a script.
We'll store the token in a local file for convenience.
