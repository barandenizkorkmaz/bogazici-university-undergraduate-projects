package project;

import java.awt.Color;
import java.util.Random;

import game.Direction;
import naturesimulator.Action;
import naturesimulator.LocalInformation;
import ui.GridPanel;

/**
 * Class representing the general structure/properties of a Plant.
 */

public class Plant extends Creature{
	/**
	 * @field maxHealth The maximum limit of the health of the Herbivore.
	 */
	private double maxHealth=1.0;
	
	/**
	 * Constructs the Plant by given parameters.
	 * Constructor sets the health of the Plant into its initial value that is 0.5 .
	 * 
	 * @param x The x-coordinate of the Plant.
	 * @param y The y-coordinate of the Plant.
	 */
	
	public Plant(int x, int y) {
		// TODO Auto-generated constructor stub
		super(x,y);
		this.setHealth(0.5);
	}
	
	/**
	 * The brain of the Plant.
	 * The Plant decides the best action by considering its surrounding and health conditions.
	 * 
	 * 
	 * @param information The parameter that is created inside the NatureSimulator class contains information about the environment of the Plant.
	 * @return The action to be implemented by the Plant.
	 */
	
	public Action chooseAction(LocalInformation information) {
		if(this.getHealth()>=0.75 && information.getFreeDirections().size()!=0) {
			Direction directionOfAction=LocalInformation.getRandomDirection(information.getFreeDirections());
			Action actionToBeSelected=new Action(Action.Type.REPRODUCE,directionOfAction);
			return actionToBeSelected;
		}
		else {
			return new Action(Action.Type.STAY);
		}
	}
	
	/**
	 * Implements the reproduction action via given direction parameter.
	 * The method makes necessary changes in the properties of the Plant which is its health.
	 * The method also arranges the properties of the Plant reproduced which are its health and coordinates. Eventually, returns the new creature.
	 * @param direction The direction of the reproduce action.
	 * @return Returns the new Plant reproduced.
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
		Plant newCreature=new Plant(newX,newY);
		newCreature.setHealth(this.getHealth()*0.1);
		this.setHealth(this.getHealth()*0.7);
		return newCreature;
	}
	
	/**
	 * Implements the stay action.
	 * The method makes necessary changes in the properties of the Plant which is solely its health.
	 */
	
	public void stay() {
		double currentHealth=this.getHealth();
		double nextHealth=Math.min(currentHealth+0.05, maxHealth);
		this.setHealth(nextHealth);
	}
	
	/**
     * Method that is called when an object needs to be drawn on the grid panel.
     * A class implementing this method should draw itself on the given panel.
     * In this case, since the method will be drawing a Plant, it's overridden so that the method can draw Herbivores coloured by green.
     * 
     * @param panel grid panel to draw on
     */
	
	public void draw(GridPanel panel) {
		// TODO Auto-generated method stub
		panel.drawSquare(this.getX(), this.getY(), Color.GREEN);
	}
}
