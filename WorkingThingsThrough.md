# WorkingThingsThrough

What do I need to implement?

Well the darkness does not exist.  
I am thinking of a grid where the cells contain a value for brightness or darkness.  
So, we need a grid that spans the size of the map.  
I also need to have the player throw items.  
So some way of handling that is needed as well.  
The items should increase the brightness of the grid cells near it.  
The enemy, if it passes by, should reduce the brightness of the cells.

...

Okay, so now basic potions exist, the shadows exist.  
Next thing I believe would be the moving camera, so it follows the player around.  
After that, then I believe modifying the map file to have enemy spawns and the like.  
Cannot think of much else as of right now.  
Good luck future me.

...

Now we got a camera, and that works nice.  
So, I can get to work on some different things now.  
I would like the potions to work better.  
I want particles, I want the potions to be more than a green circle.  
I want there to be something to show where a potion landed.  
Basically showing the results of throwing the potions.  
I think particles first would be best.

...

We now have basic particles.  
And the potions are more as I want them.  
I suppose there are two things I can work on next.  
One of them is the enemies.  
I want maybe three kinds of enemies.  
One that just beelines towards the player if it sees them.  
One that targets the exploded potions to remove them.  
And something else, I do not know, figure it out.
The other thing is sprites.  
By that I mean make things actually look nicer than just SQUARE or CIRCLE.  
I feel like the enemies should be done first as that is actual gameplay.  
A thing to think about is that I want the exploded potions to have health.  
So when enemies get near them, they get damaged, but so do the potions.  
Eventually they would disappear.

So, starting with the enemies.  
I said three enemies, lets go with that.  
We will have, lets say Stalkers, the ones that go straight for the player if seen.  
Next is, Consumers, enemies that target lights found, or just roam if no lights are found.
If the player is found then target the player.
But lights are a priority.  
Finally, I will have, Darklings, these spawn in large groups and stick together.
If a light is found, then they charge straight towards it.
If the player is found, then charge straight towards them.

When it comes to the enemies, they all feel quite similar, the Stalkers and the Darklings are pretty much the same.  
They just look different.  
I suppose if the stats of the potions are taken into account.  
So if there is something like area damage, then that counters the Darklings well, but direct/hitting damage does well
against the Stalkers.  
The Consumers I want to be large and slow, imposing feeling, but not a danger if there is a light nearby as they will be
targeted first.

...

I created the new Stalker enemy.
Was not too difficult, it was quite similar to that of the basic enemy.
But now it exists.  
I have yet to do the other two enemies.  
I think I want to work on damaging the enemies and the player next.  
Mainly because that is actually gameplay related and the two new enemies are not really.  
Well, they are, but not complete necessary for a demo.

I also want to change the mapdata files a bit.
Add some extra data, such as rooms and enemies.  
A map consists of tiles for the walls, and rooms can be collections of empty tiles.  
Enemies can exist within rooms, and they cannot leave, but they can roam around within them.  
This allows me to prevent enemies from roaming too much.  
The mapdata files can also contain information about the placement of enemies and which rooms they reside in.

Finally, I also want to add in upgrades.  
I have thought of four.
An upgrade to:  
-- the direct damage caused by the potions, if they directly hit an enemy before exploding.  
-- the light damage by the light radius of an exploded potion.  
-- the radius of the light cast by an exploded potion.  
-- the distance a potion can be thrown.  
The actual implementation of these should not be too difficult as the values that govern those are in variables.  
So it is simply a matter of, if collide with upgrade, increment value.  
It will probably be a little more difficult than that, but ehh.

I also want to add in a boss, something like the basilisk demo I created.  
Stripped down, but with the essence of it.  
I do not know if this will happen, bit I like the idea of it.

So in summary:  
Implement damage.
That is direct damage and indirect damage.  
If time persists, add enemy spawns to the mapdata.  
If time continues to persist, add rooms to the map data and make enemies subscribe to a room.  
Then add in upgrades or the two missing enemies, either or, does not matter too much.  
Finally, I want a boss.

...

Enemies can now be damaged, and killed.  
The player can also be damaged, although not killed, yet.
Evil laughter.  
The mapdata file has been upgraded to allow for rooms and enemy spawns.  
Although interacting with rooms themselves has not been implemented.

So, what next?  
Well, I want the stalker to stay in its room, bad stalker, too much stalking.   
If it leaves the room by following the player, then it will beeline towards the closest tile in that room.  
I do not really care if it cannot get there.
Sorry stalkers.

Once the stalkers are confined to their rooms, then I want the upgrades to be worked on.  
The map data should include the upgrades and their locations.  
I do not think that this would take that much time.
Hopefully...

After upgrades, then I think creating some sprites and beautifying the game would be a good idea.  
Small sound effects and more particles.  
It is kind of bland as it is.  
Sprites could include, potion unexploded and exploded, the player and the upgrades.  
Beautifying could include making the floor more than just once colour, and the walls not pink.  
Although the wall colour has grown on me a little.  
Also a bunch of particles when the stalker dies.  
It is kind of flat how it just, disappears.

I also want a title screen and a way to replay without reloading the page.  
If time persists, then work on the boss or the other two enemies.  
These are not a priority at all.

I forgot about the player dying.  
If the player dies, then just slap some text on the screen saying so.  
A simple health bar can also be made, figure that out future me.  
If we have a title screen, then send there after death.

So, what next?  
-- Confine stalkers to their rooms.  
-- Implement upgrades.  
-- Add upgrades to the map data.    
-- Player can die.  
-- Beautify the game.

Maybe...
-- Title screen.  
-- Replay button.  
-- Boss monster.  
-- The other enemies.

...

My thoughts are a bit jumbled, so I will do this a little earlier than usual.

I have confined the stalkers to their rooms, if they are outside by more than one tile, then they just stay still.  
If the player is in the same room, then the stalker can see them regardless of the distance.  
Not exactly what I said before, but I like this.

The mapdata file has been upgraded to include upgrades.  
These upgrades can now exist within the game world and be collected.

So, next...  
Well the player still cannot die.  
That needs to be fixed.  
There is also a lack of a clear objective.  
A simple one is to kill all the enemies.  
I can slap a counter on the screen to show how many are left.  
Another one is to collect all the upgrades.  
A clear-cut one is to kill a final boss, but that requires implementing, and there is not a super amount of time to do
that.

A very basic hud can be made to show this information, alongside health and cooldown for throwing potions.

If the player is killed, one of two things can happen, restart the game immediately.  
Or have a title screen to return to.  
I like the idea of a title screen, but that will take more time, so for now, immediate restart.

Beautification should still happen.  
I have not forgotten.  
This will include simple sound effects for most actions.  
Throwing potion, potion exploding, enemy dying, potion fizzling out (maybe), the like.  
Also more particles.  
When enemies die, when potions fizzle out.  
I also want the exploded potion light to disappear slowly, not straight away.  
Should not be the most difficult...

So, to make things simple:  
-- Allow the player to be killed.  
-- Restart the game when this happens.  
-- Create a basic hud/ui.  
-- Beautification.  
-- Boss monster.  
-- More beautification.

...

The player can now die.  
Their immortality has been removed.  
The game allows time for a death animation and then restarts.

I also created a very basic ui, showing the health, potion cooldown and remaining enemies and upgrades left.  
It is not the bets of things, but it is there at least.

What to do next?  
Well the beautification.  
Add more particles to everything.  
Add the shrinking light sources when the potions run out and the player dies.  
Add in sound effects.

If there is time, although I doubt this, attempt to create the boss monster.

Oh, and potentially make a map for the submission.

Ahh, and make an end screen thingy, for when all enemies are dead and upgrades collected.

Summary:  
-- Beautification.  
---- Particles.  
---- Shrinking lights.  
---- Sound effects.  
-- End screen.  
-- Boss monster.

...

Okay, so last entry for this sprint.

I have added shrinking lights, they look quite cool I think.  
When the player dies, their light shrinks.  
When the exploded potions wear out, their light shrinks.  
They also explode with some particles, I think this looks cool as well.  
The more particles the better.

A bunch of things can do with more particles.  
-- Unexploded potions flying through the air.  
-- Unexploded potions hitting an enemy.  
-- Player death.  
-- Collecting an upgrade.  
Those are the main ones I can think of right now.

I want to implement the basic enemy rendering code into the stalker.  
I like it, and it is better than purple circle.

Things could do with sprites to make it cleaner.  
-- The potions that are thrown, and on the ui.  
-- The exploded potion on the floor.  
-- The upgrades.

Actually, whilst I am thinking about it, give the upgrades light sources.

Sound effects will give things a bit more flare as well.
Some simple ones.  
-- When a potion is thrown.  
-- When a potion hits something.  
-- When you collect an upgrade.  
-- When you take damage.  
-- When you die.  
-- When an enemy dies.

And maybe some others, I cannot think of anything right now.

So in summary:
-- More particles.  
-- Change rendering code in stalker to be that of basic enemy.  
-- Add some sound effects.

See above entry for extra stuff to do.  
I am pretty sure that I will not have time for the boss, but ehh.  
I have put a lot of work into this, and am proud of where it is.

...
