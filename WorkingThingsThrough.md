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
