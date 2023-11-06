package project;

import java.awt.Color;
import game.Direction;
import game.Drawable;
import naturesimulator.Action;
import naturesimulator.LocalInformation;
import naturesimulator.NatureSimulator;
import ui.GridPanel;

/**
 * Class representing the general structure/properties of a Creature.
 * This class will be extended and overrided by Herbivore and Plant classes later.
 */

public class Creature implements Drawable{
	/**
	 * @field x The x-coordinate of the creature.
	 * @field y The y-coordinate of the creature.
	 * @field health The health of the creature.
	 */
	private int x;
	private int y;
	private double health;
	
	/**
	 * Constructs the creature by given parameters.
	 * 
	 * @param x The x-coordinate of the creature.
	 * @param y The y-coordinate of the creature.
	 */
	
	public Creature(int x,int y) {
		this.x=x;
		this.y=y;
	}
	
	/**
	 * @return The x-coordinate of the creature.
	 */
	
	public int getX(){
		return this.x;
	}
	
	/**
	 * @return The y-coordinate of the creature.
	 */
	
	public int getY(){
		return this.y;
	}
	
	/**
	 * Sets the x-coordinate of the creature into the given parameter value.
	 * 
	 * @param x The new x-coordinate of the creature.
	 */
	
	public void setX(int x) {
		this.x=x;
	}
	
	/**
	 * Sets the y-coordinate of the creature into the given parameter value.
	 * 
	 * @param y The new y-coordinate of the creature.
	 */
	
	public void setY(int y) {
		this.y=y;
	}
	
	/**
	 * The brain of the creature.
	 * The creature decides the best action by considering its surrounding and health conditions.
	 * 
	 * 
	 * @param information The parameter that is created inside the NatureSimulator class contains information about the environment of the creature.
	 * @return The action to be implemented by the creature.
	 */
	
	public Action chooseAction(LocalInformation information){
		return null;
	}
	
	/**
	 * Implements the move action via given direction parameter.
	 * The method makes necessary changes in the properties of the creature which are its health and coordinates.
	 * 
	 * 
	 * @param direction The direction of the move action.
	 */
	
	public void move(Direction direction) {
		
	}
	
	/**
	 * Implements the reproduction action via given direction parameter.
	 * The method makes necessary changes in the properties of the creature which is its health.
	 * The method also arranges the properties of the creature reproduced which are its health and coordinates. Eventually, returns the new creature.
	 * @param direction The direction of the reproduce action.
	 * @return Returns the new creature reproduced.
	 */
	
	public Creature reproduce(Direction direction) {
		return null;
	}
	
	/**
	 * Implements the attack action on the creature which is given as parameter.
	 * The method makes necessary changes in the properties of the creature which are its health and coordinates.
	 * The method also arranges the properties of the creature being attacked that is to set its health into zero so that it could be removed.
	 * @param creature The creature being attacked.
	 */
	
	public void attack(Creature creature) {
		
	}
	
	/**
	 * Implements the stay action.
	 * The method makes necessary changes in the properties of the creature which is solely its health.
	 */
	
	public void stay() {
		
	}
	
	/**
	 * 
	 * @return The health of the creature.
	 */
	
	public double getHealth() {
		return this.health;
	}
	
	/**
	 * Sets the health of the creature into the given parameter value.
	 * 
	 * @param newHealth The new health value of the creature.
	 */
	
	public void setHealth(double newHealth) {
		this.health=newHealth;
	}
	
	/**
     * Method that is called when an object needs to be drawn on the grid panel.
     * A class implementing this method should draw itself on the given panel.
     * @param panel grid panel to draw on
     */
	
	@Override
	public void draw(GridPanel panel) {
		// TODO Auto-generated method stub
	}
}
