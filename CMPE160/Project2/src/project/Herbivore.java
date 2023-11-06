package project;
import java.util.*;
import java.awt.Color;
import game.Direction;
import game.Drawable;
import naturesimulator.Action;
import naturesimulator.LocalInformation;
import ui.GridPanel;

/**
 * Class representing the general structure/properties of a Herbivore.
 * 
 */

public class Herbivore extends Creature {
	/**
	 * @field maxHealth The maximum limit of the health of the Herbivore.
	 */
	private double maxHealth=20.0;
	
	/**
	 * Constructs the Herbivore by given parameters.
	 * Constructor sets the health of the Herbivore into its initial value that is 10.0 .
	 * 
	 * @param x The x-coordinate of the Herbivore.
	 * @param y The y-coordinate of the Herbivore.
	 */
	
	public Herbivore(int x, int y) {
		// TODO Auto-generated constructor stub
		super(x,y);
		this.setHealth(10.0);
	}
	
	/**
	 * The brain of the Herbivore.
	 * The Herbivore decides the best action by considering its surrounding and health conditions.
	 * 
	 * 
	 * @param information The parameter that is created inside the NatureSimulator class contains information about the environment of the Herbivore.
	 * @return The action to be implemented by the Herbivore.
	 */
	
	public Action chooseAction(LocalInformation information) {
		Action actionToBeSelected;
		List<Direction> list=information.getFreeDirections();
		if(this.getHealth()==maxHealth && information.getFreeDirections().size()!=0) {
			Direction directionOfAction=LocalInformation.getRandomDirection(information.getFreeDirections());
			actionToBeSelected=new Action(Action.Type.REPRODUCE,directionOfAction);
		}
		else if((this.getHealth()<maxHealth) &&
				(((information.getFreeDirections().size()==0) &&
				(information.getCreatureLeft() instanceof Plant) ||
				 (information.getCreatureRight() instanceof Plant) ||
		    	 (information.getCreatureUp() instanceof Plant) ||
				 (information.getCreatureDown() instanceof Plant))
				|| 
				((information.getFreeDirections().size()!=0) &&
						(information.getCreatureLeft() instanceof Plant) ||
						 (information.getCreatureRight() instanceof Plant) ||
				    	 (information.getCreatureUp() instanceof Plant) ||
						 (information.getCreatureDown() instanceof Plant)))
				) {
			List<Direction> availableDirections=new ArrayList<>();
			if(information.getCreatureLeft() instanceof Plant) {
				availableDirections.add(Direction.LEFT);
			}
			if(information.getCreatureRight() instanceof Plant) {
				availableDirections.add(Direction.RIGHT);
			}
			if(information.getCreatureUp() instanceof Plant) {
				availableDirections.add(Direction.UP);
			}
			if(information.getCreatureDown() instanceof Plant) {
				availableDirections.add(Direction.DOWN);
			}
			Direction directionOfAction=LocalInformation.getRandomDirection(availableDirections);
			actionToBeSelected=new Action(Action.Type.ATTACK,directionOfAction);
		}
		
		else if(this.getHealth()>1.0 && information.getFreeDirections().size()!=0) {
			Direction directionOfAction=LocalInformation.getRandomDirection(information.getFreeDirections());
			actionToBeSelected=new Action(Action.Type.MOVE,directionOfAction);
		}
		else {
			actionToBeSelected=new Action(Action.Type.STAY);
		}
		return actionToBeSelected;
	}
	
	/**
	 * Implements the reproduction action via given direction parameter.
	 * The method makes necessary changes in the properties of the Herbivore which is its health.
	 * The method also arranges the properties of the Herbivore reproduced which are its health and coordinates. Eventually, returns the new creature.
	 * @param direction The direction of the reproduce action.
	 * @return Returns the new Herbivore reproduced.
	 */
	
	public Creature reproduce(Direction direction) {
		int newX;
		int newY;
		if (direction == Direction.UP) {
            newX=this.getX();
			newY=this.getY()-1;
        } else if (direction == Direction.DOWN) {
        	newX=this.getX();
			newY=this.getY()+1;
        } else if (direction == Direction.LEFT) {
        	newX=this.getX()-1;
			newY=this.getY();
        } else {
        	newX=this.getX()+1;
			newY=this.getY();
        }
		Herbivore newCreature=new Herbivore(newX,newY);
		newCreature.setHealth(this.getHealth()*0.2);
		this.setHealth(this.getHealth()*0.4);
		return newCreature;
	}
	
	/**
	 * Implements the attack action on the creature which is given as parameter.
	 * The method makes necessary changes in the properties of the Herbivore which are its health and coordinates.
	 * The method also arranges the properties of the creature being attacked (a Plant) that is to set its health into zero so that it could be removed.
	 * @param creature The creature being attacked (a Plant).
	 */
	
	public void attack(Creature creature) {
		double newHealth=Math.min(this.getHealth()+creature.getHealth(),this.maxHealth);
		creature.setHealth(0.0);
		int attackedCreatureX=creature.getX();
		int attackedCreatureY=creature.getY();
		this.setX(attackedCreatureX);
		this.setY(attackedCreatureY);
		this.setHealth(newHealth);
	}
	
	/**
	 * Implements the move action via given direction parameter.
	 * The method makes necessary changes in the properties of the Herbivore which are its health and coordinates.
	 * 
	 * 
	 * @param direction The direction of the move action.
	 */
	
	public void move(Direction direction) {
		int newX;
		int newY;
		if (direction == Direction.UP) {
            newX=this.getX();
			newY=this.getY()-1;
        } else if (direction == Direction.DOWN) {
        	newX=this.getX();
			newY=this.getY()+1;
        } else if (direction == Direction.LEFT) {
        	newX=this.getX()-1;
			newY=this.getY();
        } else {
        	newX=this.getX()+1;
			newY=this.getY();
        }
		this.setX(newX);
		this.setY(newY);
		double currentHealth=this.getHealth();
		double nextHealth=Math.max(currentHealth-1.0, 0.0);
		this.setHealth(nextHealth);
	}
	
	/**
	 * Implements the stay action.
	 * The method makes necessary changes in the properties of the Herbivore which is solely its health.
	 */
	
	public void stay() {
		double currentHealth=this.getHealth();
		double nextHealth=Math.max(currentHealth-0.1, 0.0);
		this.setHealth(nextHealth);
	}
	
	/**
     * Method that is called when an object needs to be drawn on the grid panel.
     * A class implementing this method should draw itself on the given panel.
     * In this case, since the method will be drawing a Herbivore, it's overridden so that the method can draw Herbivores coloured by red.
     * 
     * @param panel grid panel to draw on
     */
	
	public void draw(GridPanel panel) {
		// TODO Auto-generated method stub
		panel.drawSquare(this.getX(), this.getY(), Color.RED);
	}
}
